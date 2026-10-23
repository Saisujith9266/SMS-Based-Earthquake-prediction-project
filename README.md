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

## Extended end-to-end features

The Streamlit application now includes a trained-model prediction option, a manual magnitude mode for safely testing the alert workflow, recipient registration with SMS/email preferences, notification history, and a one-time SMS test action. SMTP email is implemented in `services/email_service.py`; configure it locally through environment variables.

### Dataset and model training

From `src/sms_alert_system`, activate your virtual environment and install `requirements.txt`. Then run:

```bash
python download_usgs_dataset.py --start 2015-01-01 --end 2025-01-01 --min-magnitude 2.5
python train_model.py
streamlit run app.py
```

The downloader saves the public USGS catalog to `data/usgs_earthquakes.csv`. Training compares Linear Regression, Decision Tree, Random Forest, and Extra Trees on a held-out test split, writes `model_metrics.csv`, and saves `models/magnitude_model.joblib`. Report the actual generated metrics; do not copy illustrative metrics into the final research paper.

### SMS and email configuration

Copy `.env.example` to `.env` and set Twilio credentials locally. For email, set `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_APP_PASSWORD`, and `SMTP_FROM_EMAIL`. For Gmail, use a Google App Password where supported, not your normal account password. Never commit `.env`, credentials, real recipient contact details, or database files.

Keep `SIMULATION_MODE=true` while testing. Only disable it when you intentionally want to send real external messages to recipients who consented to receive them. SMS delivery depends on Twilio account, sender-number, country, and destination restrictions.

### Important research limitation

This academic prototype estimates a magnitude from structured catalog fields. It does not predict the exact time or location of future earthquakes and must not be presented as an official earthquake early-warning service. Geographic radius and magnitude bands are project-configurable demonstration rules.
