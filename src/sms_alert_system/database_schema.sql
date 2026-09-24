CREATE DATABASE IF NOT EXISTS earthquake_alerts;
USE earthquake_alerts;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    mobile_number VARCHAR(20) NOT NULL UNIQUE,
    latitude DOUBLE NOT NULL,
    longitude DOUBLE NOT NULL,
    address VARCHAR(255),
    alerts_enabled BOOLEAN DEFAULT TRUE,
    risk_levels_json TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS earthquake_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id VARCHAR(100) NOT NULL UNIQUE,
    latitude DOUBLE NOT NULL,
    longitude DOUBLE NOT NULL,
    depth_km DOUBLE NOT NULL,
    predicted_magnitude DOUBLE NOT NULL,
    event_time VARCHAR(80) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS risk_alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id VARCHAR(100) NOT NULL UNIQUE,
    prediction_id INT NOT NULL,
    risk_level VARCHAR(30) NOT NULL,
    affected_radius_km DOUBLE NOT NULL,
    users_in_area INT DEFAULT 0,
    sms_sent INT DEFAULT 0,
    successful INT DEFAULT 0,
    failed INT DEFAULT 0,
    simulation_mode BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prediction_id) REFERENCES earthquake_predictions(id)
);

CREATE TABLE IF NOT EXISTS sms_alert_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id VARCHAR(100) NOT NULL,
    user_id INT NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    risk_level VARCHAR(30) NOT NULL,
    message TEXT NOT NULL,
    delivery_status VARCHAR(30) NOT NULL,
    provider_message_id VARCHAR(100),
    error_message TEXT,
    attempt_count INT DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
