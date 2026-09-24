# SMS Alert System

Architecture:
Existing ML Model → Predicted Magnitude → Coordinates → Affected Radius → Risk Classification → Registered Users → Risk SMS → Twilio → Alert History → Dashboard.

Development uses SIMULATION_MODE=true so no real SMS is sent.

Project configuration risk bands:
- < 4.0: Low Risk
- 4.0–4.9: Moderate Risk
- 5.0–5.9: High Risk
- 6.0–6.9: Very High Risk
- >= 7.0: Critical Risk

These thresholds are project configuration values, not universal earthquake-impact standards.
