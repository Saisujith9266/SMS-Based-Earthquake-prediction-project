# Machine Learning-Based Earthquake Magnitude Prediction

A B.Tech project for predicting earthquake magnitude from historical seismic parameters and extending the prediction workflow with risk classification, affected-area matching, and SMS notifications.

## Project Scope

**Earthquake Dataset → Data Cleaning → Missing-Value Handling → Feature Selection → Normalization → Train/Test Split → ML Model → Predicted Magnitude → Risk Classification → Alert/Dashboard**

The proposed ML comparison contains Linear Regression, Decision Tree Regressor, Random Forest Regressor, XGBoost, and Artificial Neural Network (ANN).

Evaluation metrics: MAE, MSE, RMSE, and R² Score.

The application layer includes a Streamlit dashboard and an SMS alert module using Twilio. The alert package is a post-prediction layer connected to the trained model output.

## Repository Structure

```text
data/
docs/
reports/
results/
src/
.gitignore
LICENSE
README.md
```

## Dataset Sources

- USGS Earthquake Catalog
- Kaggle Earthquake Database
- IRIS Seismic Data
- NOAA Earthquake Database
- Global Earthquake Model (GEM)

Document the exact dataset, collection period, geographic coverage, record count, preprocessing settings, split, seed, and hyperparameters before final submission.

## Input Features

- Latitude
- Longitude
- Depth
- Time
- Seismic measurements

Target: **earthquake magnitude**.

## SMS Alert Layer

The included `src/sms_alert_system` package provides risk classification, affected-area matching, registered users, SMS generation, Twilio integration, alert history, Streamlit dashboard, and simulation mode.

Example project risk bands:

| Magnitude | Risk |
|---|---|
| < 4.0 | Low Risk |
| 4.0–4.9 | Moderate Risk |
| 5.0–5.9 | High Risk |
| 6.0–6.9 | Very High Risk |
| ≥ 7.0 | Critical Risk |

These are project configuration thresholds, not universal earthquake-impact standards.

## Run the SMS/Dashboard Module

From `src/sms_alert_system`:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Windows Git Bash:

```bash
source .venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env
```

Keep `SIMULATION_MODE=true` during development.

Then:

```bash
python seed_demo.py
python simulate_alert.py
streamlit run app.py
```

## Results

The final MAE/MSE/RMSE/R² values must come from completed experiments. Do not fabricate results. Populate `reports/model_results_template.csv` and `results/` after running the five models on the same held-out test set.

## Team

- Rahul (2420090043)
- Sai Sujith (2420030280)
- Nikhileash (2420030596)
- Sumanth Reddy (2420030782)

Department of Computer Science and Engineering, Koneru Lakshmaiah Education Foundation.
