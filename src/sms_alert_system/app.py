import re
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
import requests
import streamlit as st
from services.config import settings
from services.db import init_db,create_user,list_users,get_alert_history
from services.alert_service import process_prediction
from services.validation import validate_phone

st.set_page_config(page_title="SEISMOALERT | Earthquake Risk",page_icon="🌍",layout="wide")
init_db()
st.title("🌍 SEISMOALERT — Earthquake Prediction & Alert System")
st.caption("Academic research prototype. This is not an official early-warning service and cannot predict exact earthquake time/location.")
st.sidebar.header("Alert configuration")
radius_km=st.sidebar.number_input("Affected radius (km)",1.0,1000.0,float(settings.DEFAULT_RADIUS_KM),1.0)
simulation_mode=st.sidebar.toggle("Simulation mode (no real messages)",value=settings.SIMULATION_MODE)
st.sidebar.info("Keep simulation enabled until SMS/email credentials are configured and a test recipient has consented.")

def get_model_prediction(lat,lon,depth,event_time):
    path=Path("models/magnitude_model.joblib")
    if not path.exists(): return None,"Model not trained. Run download_usgs_dataset.py then train_model.py."
    try:
        import joblib
        pack=joblib.load(path); dt=pd.to_datetime(event_time,utc=True)
        values={"latitude":lat,"longitude":lon,"depth":depth,"year":dt.year,"month":dt.month,"day":dt.day,"hour":dt.hour}
        pred=float(pack["model"].predict(pd.DataFrame([[values[k] for k in pack["features"]]],columns=pack["features"]))[0])
        return max(0.0,min(10.0,pred)),f"Model: {pack.get('model_name','trained regressor')}"
    except Exception as exc: return None,f"Could not load model: {exc}"

def send_test_sms(phone):
    from services.twilio_service import SMSService
    return SMSService(simulation_mode).send_sms(phone,"SEISMOALERT test message. This is a test only; no earthquake is being reported.")

tab1,tab2,tab3,tab4=st.tabs(["Predict & Alert","Register Recipients","Alert History","Dataset & Model"])
with tab1:
    st.subheader("Earthquake event details")
    c1,c2,c3=st.columns(3)
    lat=c1.number_input("Latitude",-90.0,90.0,17.3850,format="%.6f")
    lon=c2.number_input("Longitude",-180.0,180.0,78.4867,format="%.6f")
    depth=c3.number_input("Depth (km)",0.0,800.0,10.0)
    event_time=st.text_input("Event time (UTC ISO)",datetime.now(timezone.utc).replace(microsecond=0).isoformat())
    if st.button("Estimate magnitude with trained ML model"):
        pred,info=get_model_prediction(lat,lon,depth,event_time)
        if pred is None: st.warning(info)
        else:
            st.session_state["predicted_mag"]=pred; st.success(f"Estimated magnitude: {pred:.2f}. {info}")
    manual=st.checkbox("Use manual magnitude for testing the alert workflow",value=True)
    if manual:
        mag=st.number_input("Test magnitude",0.0,10.0,5.2,step=0.1)
    else:
        mag=st.session_state.get("predicted_mag")
        if mag is None: st.info("First estimate magnitude with the trained model."); mag=None
    if mag is not None and st.button("Classify risk and process notifications",type="primary"):
        result=process_prediction(latitude=lat,longitude=lon,depth_km=depth,predicted_magnitude=float(mag),
            event_time=event_time,radius_km=radius_km,simulation_mode=simulation_mode)
        st.session_state["last_result"]=result
    if "last_result" in st.session_state: st.json(st.session_state["last_result"])
    st.divider()
    st.subheader("Send a one-time SMS test")
    test_phone=st.text_input("Test mobile number in E.164 format",placeholder="+919876543210")
    if st.button("Send test SMS"):
        ok,msg=validate_phone(test_phone)
        if not ok: st.error(msg)
        else:
            result=send_test_sms(test_phone)
            (st.success if result["success"] else st.error)(str(result))

    st.subheader("Send a one-time email test")
    test_email=st.text_input("Test email address")
    if st.button("Send test email"):
        if not re.fullmatch(r"[^@\\s]+@[^@\\s]+\\.[^@\\s]+",test_email.strip()):
            st.error("Enter a valid email address.")
        else:
            from services.email_service import send_email
            result=send_email(test_email,"SEISMOALERT email test",
                "This is a test email only. No earthquake is being reported.",simulation_mode)
            (st.success if result["success"] else st.error)(str(result))

with tab2:
    with st.form("register_user"):
        name=st.text_input("Recipient name")
        phone=st.text_input("Mobile number (international format)",placeholder="+919876543210")
        email=st.text_input("Email address (optional)")
        address=st.text_input("Address / locality")
        c1,c2=st.columns(2)
        ulat=c1.number_input("Recipient latitude",-90.0,90.0,17.3850,format="%.6f")
        ulon=c2.number_input("Recipient longitude",-180.0,180.0,78.4867,format="%.6f")
        sms_enabled=st.checkbox("Enable SMS notifications",True)
        email_enabled=st.checkbox("Enable email notifications",False)
        selected=st.multiselect("Risk levels",["Low Risk","Moderate Risk","High Risk","Very High Risk","Critical Risk"],
            default=["Moderate Risk","High Risk","Very High Risk","Critical Risk"])
        submitted=st.form_submit_button("Register recipient")
    if submitted:
        ok,msg=validate_phone(phone) if sms_enabled else (True,"")
        if not ok: st.error(msg)
        elif not name.strip(): st.error("Name is required.")
        elif sms_enabled and not phone.strip(): st.error("Phone is required when SMS is enabled.")
        elif email_enabled and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+",email.strip()): st.error("Enter a valid email for email notifications.")
        elif not sms_enabled and not email_enabled: st.error("Enable at least one notification channel.")
        elif not selected: st.error("Select at least one risk level.")
        else:
            try:
                create_user(name,phone or "disabled-"+str(datetime.now().timestamp()),ulat,ulon,address,sms_enabled,selected,email,email_enabled)
                st.success("Recipient registered.")
            except Exception as exc: st.error("Registration failed. Mobile numbers must be unique. "+str(exc))
    st.dataframe(list_users(),use_container_width=True)

with tab3:
    alerts,sms,email=get_alert_history()
    st.subheader("Risk alerts"); st.dataframe(alerts,use_container_width=True)
    st.subheader("SMS history"); st.dataframe(sms,use_container_width=True)
    st.subheader("Email history"); st.dataframe(email,use_container_width=True)

with tab4:
    st.subheader("Download historical earthquake data")
    st.markdown("Dataset source: [USGS Earthquake Catalog API](https://earthquake.usgs.gov/fdsnws/event/1/).")
    st.code("python download_usgs_dataset.py --start 2015-01-01 --end 2025-01-01 --min-magnitude 2.5\npython train_model.py",language="bash")
    st.write("The downloaded CSV is saved to data/usgs_earthquakes.csv; the training script compares four regression baselines and saves the best held-out-MAE model.")
    if Path("model_metrics.csv").exists(): st.dataframe(pd.read_csv("model_metrics.csv"),use_container_width=True)
    if Path("data/usgs_earthquakes.csv").exists():
        df=pd.read_csv("data/usgs_earthquakes.csv")
        st.metric("Dataset rows",f"{len(df):,}")
        st.dataframe(df.head(20),use_container_width=True)
