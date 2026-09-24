# Integrate with Existing Earthquake ML Project

1. Copy the `services/` folder into the existing project.
2. Install `requirements.txt`.
3. Copy `.env.example` to `.env`.
4. Keep `SIMULATION_MODE=true` during testing.
5. After the existing model computes `predicted_magnitude`, call `process_prediction(...)`.
6. Display the returned alert result in the Streamlit dashboard.
7. Only after simulation testing succeeds should live Twilio mode be enabled.

The alert package is a post-prediction layer and does not replace the ML preprocessing/model pipeline.