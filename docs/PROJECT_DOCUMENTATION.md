# Project Documentation

## Project
Machine Learning-Based Earthquake Magnitude Prediction

## Candidate Data Sources
USGS Earthquake Catalog, Kaggle Earthquake Database, IRIS Seismic Data, NOAA Earthquake Database, Global Earthquake Model (GEM).

## Features
Latitude, Longitude, Depth, Time and seismic measurements.

## Target
Earthquake magnitude.

## Application
The trained prediction output is passed to the risk and SMS alert layer. Registered users are matched by geographic radius. Streamlit provides the dashboard and Twilio provides optional SMS delivery.

## Development
Use SIMULATION_MODE=true while testing. Never commit .env or real Twilio credentials.

## Results
Populate reports/model_results_template.csv only after running the five models on the same held-out test set.
