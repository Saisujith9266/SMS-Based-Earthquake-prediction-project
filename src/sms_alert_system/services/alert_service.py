import hashlib
from datetime import datetime
from services.db import create_prediction,alert_exists,create_alert,update_alert,get_enabled_users,add_sms_history
from services.geo import is_within_radius
from services.risk import classify_risk,get_message_template
from services.twilio_service import SMSService

def make_event_id(latitude,longitude,depth_km,magnitude,event_time):
    raw=f"{latitude:.6f}|{longitude:.6f}|{depth_km:.3f}|{magnitude:.3f}|{event_time}"
    return hashlib.sha256(raw.encode()).hexdigest()[:24]

def process_prediction(latitude,longitude,depth_km,predicted_magnitude,event_time,radius_km,simulation_mode=True):
    risk_level=classify_risk(float(predicted_magnitude)); event_id=make_event_id(latitude,longitude,depth_km,predicted_magnitude,event_time)
    if alert_exists(event_id): return {"event_id":event_id,"duplicate":True,"risk_level":risk_level,"magnitude":predicted_magnitude}
    prediction_id,_=create_prediction(event_id,latitude,longitude,depth_km,predicted_magnitude,event_time)
    alert_id=create_alert(event_id=event_id,prediction_id=prediction_id,risk_level=risk_level,affected_radius_km=radius_km,simulation_mode=simulation_mode)
    users=[u for u in get_enabled_users() if risk_level in u.risk_levels and is_within_radius(latitude,longitude,u.latitude,u.longitude,radius_km)]
    message=get_message_template(risk_level).format(location=f"{latitude:.4f}, {longitude:.4f}",magnitude=f"{predicted_magnitude:.1f}")
    sms=SMSService(simulation_mode); successful=failed=0
    for user in users:
        result=sms.send_sms(user.mobile_number,message); successful+=int(result["success"]); failed+=int(not result["success"])
        add_sms_history(event_id=event_id,user_id=user.id,phone_number=user.mobile_number,risk_level=risk_level,message=message,delivery_status="SIMULATED" if simulation_mode and result["success"] else ("SENT" if result["success"] else "FAILED"),provider_message_id=result.get("sid"),error_message=result.get("error"))
    update_alert(alert_id,users_in_area=len(users),sms_sent=len(users),successful=successful,failed=failed)
    return {"event_id":event_id,"magnitude":predicted_magnitude,"risk_level":risk_level,"radius_km":radius_km,"users_found":len(users),"sms_sent":len(users),"successful":successful,"failed":failed,"timestamp":datetime.utcnow().isoformat(),"simulation_mode":simulation_mode,"duplicate":False}
