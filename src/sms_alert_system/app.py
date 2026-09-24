import streamlit as st
from datetime import datetime
from services.config import settings
from services.db import init_db
from services.alert_service import process_prediction
from services.validation import validate_phone

st.set_page_config(page_title="Earthquake Risk SMS Alert", page_icon="🌍", layout="wide")
init_db()
st.title("🌍 Machine Learning-Based Earthquake Prediction & SMS Alert System")
st.caption("ML predictions are informational. They are NOT confirmed official earthquake warnings.")
st.sidebar.header("Configuration")
radius_km=st.sidebar.number_input("Affected radius (km)",1.0,1000.0,float(settings.DEFAULT_RADIUS_KM),1.0)
simulation_mode=st.sidebar.toggle("Simulation / Test SMS Mode",value=settings.SIMULATION_MODE)

tab1,tab2,tab3=st.tabs(["Predict & Alert","Users","Alert History"])
with tab1:
    lat=st.number_input("Latitude",-90.0,90.0,17.3850,format="%.6f")
    lon=st.number_input("Longitude",-180.0,180.0,78.4867,format="%.6f")
    depth=st.number_input("Depth (km)",0.0,1000.0,10.0)
    seismic=st.number_input("Seismic measurement",0.0,1000000.0,4.5)
    event_time=st.text_input("Event time (ISO)",datetime.utcnow().isoformat())
    predicted_mag=st.number_input("Predicted magnitude",0.0,10.0,5.2,step=0.1)
    if st.button("Classify Risk & Send SMS Alerts",type="primary"):
        result=process_prediction(latitude=lat,longitude=lon,depth_km=depth,predicted_magnitude=predicted_mag,event_time=event_time,radius_km=radius_km,simulation_mode=simulation_mode)
        st.session_state["last_result"]=result
    if "last_result" in st.session_state:
        st.json(st.session_state["last_result"])

with tab2:
    from services.db import create_user,list_users
    with st.form("register_user"):
        name=st.text_input("User name")
        phone=st.text_input("Mobile number",placeholder="+919876543210")
        address=st.text_input("Location / address")
        ulat=st.number_input("User latitude",-90.0,90.0,17.3850,format="%.6f")
        ulon=st.number_input("User longitude",-180.0,180.0,78.4867,format="%.6f")
        enabled=st.checkbox("Enable SMS alerts",True)
        selected=st.multiselect("Risk levels",["Low Risk","Moderate Risk","High Risk","Very High Risk","Critical Risk"],default=["Moderate Risk","High Risk","Very High Risk","Critical Risk"])
        submitted=st.form_submit_button("Register User")
    if submitted:
        ok,msg=validate_phone(phone)
        if not ok: st.error(msg)
        elif not name.strip(): st.error("Name is required.")
        elif not selected: st.error("Select at least one risk level.")
        else:
            try:
                create_user(name,phone,ulat,ulon,address,enabled,selected)
                st.success("User registered successfully.")
            except Exception as e:
                st.error("Could not register user: "+str(e))
    st.dataframe(list_users(),use_container_width=True)

with tab3:
    from services.db import get_alert_history
    alerts,sms=get_alert_history()
    st.subheader("Risk Alerts")
    st.dataframe(alerts,use_container_width=True)
    st.subheader("SMS Delivery History")
    st.dataframe(sms,use_container_width=True)
