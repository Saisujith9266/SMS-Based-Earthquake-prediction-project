from services.alert_service import process_prediction

def existing_ml_predict(latitude, longitude, depth_km, event_time, seismic_measurement):
    # Replace this demo return with your trained Scikit-learn/TensorFlow model.
    return 5.2

def predict_and_alert(latitude, longitude, depth_km, event_time,
                      seismic_measurement, radius_km=50, simulation_mode=True):
    magnitude = existing_ml_predict(latitude, longitude, depth_km, event_time, seismic_measurement)
    return process_prediction(
        latitude=latitude, longitude=longitude, depth_km=depth_km,
        predicted_magnitude=magnitude, event_time=event_time,
        radius_km=radius_km, simulation_mode=simulation_mode
    )
