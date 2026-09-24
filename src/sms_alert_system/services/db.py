import json
from datetime import datetime
from sqlalchemy import create_engine,Column,Integer,String,Float,Boolean,DateTime,Text,ForeignKey
from sqlalchemy.orm import declarative_base,sessionmaker
from services.config import settings

Base=declarative_base()
engine=create_engine(settings.DATABASE_URL,future=True)
SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False,future=True)

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True); name=Column(String(120),nullable=False)
    mobile_number=Column(String(20),unique=True,nullable=False); latitude=Column(Float,nullable=False); longitude=Column(Float,nullable=False)
    address=Column(String(255),default=""); alerts_enabled=Column(Boolean,default=True); risk_levels_json=Column(Text,nullable=False); created_at=Column(DateTime,default=datetime.utcnow)
    @property
    def risk_levels(self): return json.loads(self.risk_levels_json)

class EarthquakePrediction(Base):
    __tablename__="earthquake_predictions"
    id=Column(Integer,primary_key=True); event_id=Column(String(100),unique=True,nullable=False); latitude=Column(Float,nullable=False); longitude=Column(Float,nullable=False); depth_km=Column(Float,nullable=False); predicted_magnitude=Column(Float,nullable=False); event_time=Column(String(80),nullable=False); created_at=Column(DateTime,default=datetime.utcnow)

class RiskAlert(Base):
    __tablename__="risk_alerts"
    id=Column(Integer,primary_key=True); event_id=Column(String(100),unique=True,nullable=False); prediction_id=Column(Integer,ForeignKey("earthquake_predictions.id"),nullable=False); risk_level=Column(String(30),nullable=False); affected_radius_km=Column(Float,nullable=False); users_in_area=Column(Integer,default=0); sms_sent=Column(Integer,default=0); successful=Column(Integer,default=0); failed=Column(Integer,default=0); simulation_mode=Column(Boolean,default=True); created_at=Column(DateTime,default=datetime.utcnow)

class SMSAlertHistory(Base):
    __tablename__="sms_alert_history"
    id=Column(Integer,primary_key=True); event_id=Column(String(100),nullable=False); user_id=Column(Integer,ForeignKey("users.id"),nullable=False); phone_number=Column(String(20),nullable=False); risk_level=Column(String(30),nullable=False); message=Column(Text,nullable=False); delivery_status=Column(String(30),nullable=False); provider_message_id=Column(String(100),nullable=True); error_message=Column(Text,nullable=True); attempt_count=Column(Integer,default=1); created_at=Column(DateTime,default=datetime.utcnow)

def init_db(): Base.metadata.create_all(bind=engine)
def get_session(): return SessionLocal()
def create_user(name,phone,latitude,longitude,address,alerts_enabled,risk_levels):
    with get_session() as db:
        u=User(name=name.strip(),mobile_number=phone.strip(),latitude=latitude,longitude=longitude,address=address.strip(),alerts_enabled=alerts_enabled,risk_levels_json=json.dumps(risk_levels)); db.add(u); db.commit(); return u.id
def get_enabled_users():
    with get_session() as db: return db.query(User).filter(User.alerts_enabled==True).all()
def alert_exists(event_id):
    with get_session() as db: return db.query(RiskAlert).filter_by(event_id=event_id).first() is not None
def create_prediction(event_id,latitude,longitude,depth_km,magnitude,event_time):
    with get_session() as db:
        p=EarthquakePrediction(event_id=event_id,latitude=latitude,longitude=longitude,depth_km=depth_km,predicted_magnitude=magnitude,event_time=event_time); db.add(p); db.commit(); return p.id,True
def create_alert(**kwargs):
    with get_session() as db:
        a=RiskAlert(**kwargs); db.add(a); db.commit(); return a.id
def update_alert(alert_id,**kwargs):
    with get_session() as db:
        a=db.query(RiskAlert).filter_by(id=alert_id).first()
        for k,v in kwargs.items(): setattr(a,k,v)
        db.commit()
def add_sms_history(**kwargs):
    with get_session() as db:
        h=SMSAlertHistory(**kwargs); db.add(h); db.commit()
def list_users():
    import pandas as pd
    with get_session() as db:
        rows=db.query(User).order_by(User.id.desc()).all()
        return pd.DataFrame([{"ID":u.id,"Name":u.name,"Mobile":u.mobile_number,"Latitude":u.latitude,"Longitude":u.longitude,"Address":u.address,"SMS Enabled":u.alerts_enabled,"Risk Levels":", ".join(u.risk_levels)} for u in rows])
def get_alert_history():
    import pandas as pd
    with get_session() as db:
        alerts=db.query(RiskAlert).order_by(RiskAlert.id.desc()).all(); sms=db.query(SMSAlertHistory).order_by(SMSAlertHistory.id.desc()).all()
        return pd.DataFrame([{"Event ID":a.event_id,"Risk":a.risk_level,"Radius km":a.affected_radius_km,"Users":a.users_in_area,"SMS Sent":a.sms_sent,"Successful":a.successful,"Failed":a.failed,"Simulation":a.simulation_mode,"Timestamp":a.created_at} for a in alerts]),pd.DataFrame([{"Event ID":x.event_id,"User ID":x.user_id,"Phone":x.phone_number,"Risk":x.risk_level,"Status":x.delivery_status,"Provider SID":x.provider_message_id,"Error":x.error_message,"Timestamp":x.created_at} for x in sms])
