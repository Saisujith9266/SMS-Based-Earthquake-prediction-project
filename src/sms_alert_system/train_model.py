"""Train baseline regressors on a downloaded USGS CSV and save metrics/model.

Run download_usgs_dataset.py first. This is a research baseline, not an operational
earthquake forecasting model; event catalog features are not sufficient to predict
when/where future earthquakes will occur.
"""
from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

DATA = Path("data/usgs_earthquakes.csv")
MODEL_DIR = Path("models")
FEATURES = ["latitude", "longitude", "depth", "year", "month", "day", "hour"]

def main():
    if not DATA.exists():
        raise SystemExit("Dataset not found. Run: python download_usgs_dataset.py")
    df = pd.read_csv(DATA)
    required = ["time", "latitude", "longitude", "depth", "mag"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise SystemExit(f"Dataset is missing required columns: {missing}")
    df = df[required].copy()
    df["time"] = pd.to_datetime(df["time"], errors="coerce", utc=True)
    for col in ["latitude", "longitude", "depth", "mag"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna().drop_duplicates()
    df = df[df["mag"].between(-1, 10) & df["depth"].between(-10, 800)]
    for col in ["year", "month", "day", "hour"]:
        df[col] = getattr(df["time"].dt, col)
    X, y = df[FEATURES], df["mag"]
    if len(df) < 100:
        raise SystemExit(f"Only {len(df)} usable records; download a larger dataset.")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    models = {
        "LinearRegression": LinearRegression(),
        "DecisionTree": DecisionTreeRegressor(max_depth=12, random_state=42),
        "RandomForest": RandomForestRegressor(n_estimators=200, min_samples_leaf=2, n_jobs=-1, random_state=42),
        "ExtraTrees": ExtraTreesRegressor(n_estimators=200, min_samples_leaf=2, n_jobs=-1, random_state=42),
    }
    rows, best_name, best_model, best_mae = [], None, None, float("inf")
    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        mse = mean_squared_error(y_test, pred)
        row = {"model": name, "MAE": mean_absolute_error(y_test, pred), "MSE": mse,
               "RMSE": float(np.sqrt(mse)), "R2": r2_score(y_test, pred)}
        rows.append(row)
        print(row)
        if row["MAE"] < best_mae:
            best_name, best_model, best_mae = name, model, row["MAE"]
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": best_model, "features": FEATURES, "model_name": best_name}, MODEL_DIR / "magnitude_model.joblib")
    pd.DataFrame(rows).to_csv("model_metrics.csv", index=False)
    (MODEL_DIR / "training_metadata.json").write_text(json.dumps({
        "source": "USGS Earthquake Catalog API", "records_used": len(df),
        "test_size": 0.2, "random_state": 42, "selected_model": best_name,
        "features": FEATURES, "target": "mag"
    }, indent=2))
    print(f"Best model by held-out MAE: {best_name}")
    print("Saved models/magnitude_model.joblib and model_metrics.csv")
if __name__ == "__main__":
    main()
