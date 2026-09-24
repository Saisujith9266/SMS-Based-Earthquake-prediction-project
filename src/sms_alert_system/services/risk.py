from dataclasses import dataclass
from typing import List

@dataclass
class RiskBand:
    name: str
    min_magnitude: float
    max_magnitude: float | None
    message: str

RISK_BANDS: List[RiskBand] = [
    RiskBand("Low Risk", 0.0, 4.0, "Earthquake Alert: A low-risk earthquake event has been detected near your area. Predicted magnitude: {magnitude}. Please stay informed."),
    RiskBand("Moderate Risk", 4.0, 5.0, "Earthquake Alert: Moderate seismic activity detected near {location}. Predicted magnitude: {magnitude}. Stay alert and follow local safety instructions."),
    RiskBand("High Risk", 5.0, 6.0, "URGENT EARTHQUAKE ALERT: High-risk earthquake detected near {location}. Predicted magnitude: {magnitude}. Move to a safe location and follow emergency instructions."),
    RiskBand("Very High Risk", 6.0, 7.0, "EMERGENCY EARTHQUAKE WARNING: Very high-risk earthquake detected near {location}. Predicted magnitude: {magnitude}. Take immediate safety precautions and follow official emergency instructions."),
    RiskBand("Critical Risk", 7.0, None, "CRITICAL EARTHQUAKE ALERT: Severe earthquake activity detected near {location}. Predicted magnitude: {magnitude}. Take immediate protective action and follow official emergency instructions.")
]

def classify_risk(magnitude: float) -> str:
    if magnitude < 0:
        raise ValueError("Magnitude cannot be negative.")
    for band in RISK_BANDS:
        if band.max_magnitude is None and magnitude >= band.min_magnitude:
            return band.name
        if band.min_magnitude <= magnitude < band.max_magnitude:
            return band.name
    raise ValueError("Could not classify magnitude.")

def get_message_template(risk_level: str) -> str:
    for band in RISK_BANDS:
        if band.name == risk_level:
            return band.message
    raise KeyError(risk_level)
