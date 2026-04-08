import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Enable CORS for frontend integration

# ── Load Model ────────────────────────────────
model_path = "xgboost_model.pkl"
if not os.path.exists(model_path):
    model_path = "../xgboost_model.pkl"

try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    print("✓ Model loaded successfully")
except Exception as e:
    model = None
    print("Warning: xgboost_model.pkl not found! Ensure it is placed in the same directory or parent directory.")

# ── Helper: parse & validate incoming JSON ────
def get_input_features(data):
    required = [
        "temperature", "rainfall", "humidity", "occupancy",
        "timetable_factor", "day_of_week", "month", "day_of_year", "is_weekend"
    ]
    missing = [f for f in required if f not in data]
    if missing:
        return None, f"Missing fields: {missing}"
    try:
        row = {f: float(data[f]) for f in required}
    except (ValueError, TypeError) as e:
        return None, f"Invalid value: {e}"
    return pd.DataFrame([row]), None

# ── Route: /predict ───────────────────────────
@app.route("/predict", methods=["POST"])
def predict():
    if not model: return jsonify({"error": "Model not loaded"}), 500
    data = request.get_json()
    if not data: return jsonify({"error": "No JSON body received"}), 400
    features, error = get_input_features(data)
    if error: return jsonify({"error": error}), 400

    predicted_litres = float(model.predict(features)[0])
    return jsonify({
        "status": "ok",
        "predicted_usage_L": round(predicted_litres, 2),
        "predicted_usage_m3": round(predicted_litres / 1000, 4)
    })

# ── Route: /crisis ────────────────────────────
@app.route("/crisis", methods=["POST"])
def crisis():
    if not model: return jsonify({"error": "Model not loaded"}), 500
    data = request.get_json()
    if not data: return jsonify({"error": "No JSON body received"}), 400
    features, error = get_input_features(data)
    if error: return jsonify({"error": error}), 400

    capacity = float(data.get("daily_capacity_L", 15000))
    predicted_litres = float(model.predict(features)[0])
    usage_ratio = predicted_litres / capacity

    # Output: risk level (Low / Medium / High)
    if usage_ratio < 0.70:
        level = "Low"
    elif usage_ratio < 0.90:
        level = "Medium"
    else:
        level = "High"

    return jsonify({
        "status": "ok",
        "crisis_level": level,
        "predicted_usage_L": round(predicted_litres, 2),
        "daily_capacity_L": capacity,
        "usage_percent": round(usage_ratio * 100, 1)
    })

# ── Route: /carbon ────────────────────────────
@app.route("/carbon", methods=["POST"])
def carbon():
    if not model: return jsonify({"error": "Model not loaded"}), 500
    data = request.get_json()
    if not data: return jsonify({"error": "No JSON body received"}), 400
    features, error = get_input_features(data)
    if error: return jsonify({"error": error}), 400

    predicted_litres = float(model.predict(features)[0])
    predicted_m3 = predicted_litres / 1000

    # Emission and energy factors
    emission_factor = 0.344 # kg CO2 per m3
    energy_factor = 0.5     # kWh per m3
    
    carbon_kg = predicted_m3 * emission_factor
    energy_kwh = predicted_m3 * energy_factor

    return jsonify({
        "status": "ok",
        "predicted_usage_L": round(predicted_litres, 2),
        "carbon_footprint_kg_co2": round(carbon_kg, 4),
        "energy_consumption_kwh": round(energy_kwh, 4)
    })

# ── Route: /optimize ──────────────────────────
@app.route("/optimize", methods=["POST"])
def optimize():
    if not model: return jsonify({"error": "Model not loaded"}), 500
    data = request.get_json()
    if not data: return jsonify({"error": "No JSON body received"}), 400
    features, error = get_input_features(data)
    if error: return jsonify({"error": error}), 400

    predicted_litres = float(model.predict(features)[0])
    
    if predicted_litres > 13000:
        suggestion = "Reduce usage by 15%. Strict conservation required."
    elif predicted_litres > 10000:
        suggestion = "Pump water at 6–8 AM to optimize energy costs."
    else:
        suggestion = "Maintain current stable water usage."

    return jsonify({
        "status": "ok",
        "predicted_usage_L": round(predicted_litres, 2),
        "suggestion": suggestion
    })

# ── Route: /insights ──────────────────────────
@app.route("/insights", methods=["GET"])
def insights():
    try:
        # Try finding the dataset in current or parent folder
        dataset_paths = [
            "hydrolytix_dataset.csv", 
            "final_dataset.csv", 
            "../hydrolytix_dataset.csv", 
            "../final_dataset.csv"
        ]
        
        df = None
        for path in dataset_paths:
            if os.path.exists(path):
                df = pd.read_csv(path)
                break
                
        if df is None:
            return jsonify({"error": "Dataset not found. Please place it in the folder."}), 404

        peak_idx = df['water_usage'].idxmax()
        peak_day = str(df.loc[peak_idx, 'date'])
        highest_usage = float(df.loc[peak_idx, 'water_usage'])
        avg_usage = float(df['water_usage'].mean())

        # For Chart.js visualizations (take last 30 entries)
        df_recent = df.tail(30)
        dates = df_recent['date'].tolist()
        usage = df_recent['water_usage'].tolist()
        temps = df_recent['temperature'].tolist()

        return jsonify({
            "status": "ok",
            "peak_usage_day": peak_day,
            "highest_usage": highest_usage,
            "average_usage": round(avg_usage, 2),
            "chart_data": {
                "dates": dates,
                "water_usage": usage,
                "temperature": temps
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
