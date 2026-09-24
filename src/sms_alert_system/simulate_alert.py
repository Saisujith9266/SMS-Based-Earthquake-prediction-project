from services.db import init_db
from services.alert_service import process_prediction

init_db()
result = process_prediction(
    latitude=17.3850,
    longitude=78.4867,
    depth_km=10.0,
    predicted_magnitude=5.2,
    event_time="2026-09-21T19:00:00",
    radius_km=50,
    simulation_mode=True
)
print(result)
print("Simulation complete. No real SMS was sent.")
