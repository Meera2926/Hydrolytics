# ─────────────────────────────────────────────
#  Hydrolytix – Water Usage Prediction Model
#  Uses XGBoost to predict daily water_usage
# ─────────────────────────────────────────────

import pickle
import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ── 1. Load Data ──────────────────────────────
df = pd.read_csv("hydrolytix_dataset.csv", parse_dates=["date"])
print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns\n")

# ── 2. Feature Engineering ────────────────────
# Extract useful time-based features from the date column
df["day_of_week"] = df["date"].dt.dayofweek   # 0 = Monday, 6 = Sunday
df["month"]       = df["date"].dt.month
df["day_of_year"] = df["date"].dt.dayofyear
df["is_weekend"]  = (df["day_of_week"] >= 5).astype(int)  # 1 if Sat/Sun

# ── 3. Define Features (X) and Target (y) ────
FEATURES = [
    "temperature",
    "rainfall",
    "humidity",
    "occupancy",
    "timetable_factor",
    "day_of_week",
    "month",
    "day_of_year",
    "is_weekend",
]

X = df[FEATURES]
y = df["water_usage"]

print("Features used:")
for f in FEATURES:
    print(f"  • {f}")
print(f"\nTarget: water_usage\n")

# ── 4. Train / Test Split ─────────────────────
# 80% training, 20% testing — random_state fixes the split so results are reproducible
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Training samples : {len(X_train)}")
print(f"Testing  samples : {len(X_test)}\n")

# ── 5. Train XGBoost Model ────────────────────
model = XGBRegressor(
    n_estimators=200,       # number of trees
    max_depth=4,            # how deep each tree can grow
    learning_rate=0.1,      # how much each tree contributes
    subsample=0.8,          # fraction of data used per tree
    random_state=42,
    verbosity=0,
)

print("Training model...")
model.fit(X_train, y_train)
print("Training complete!\n")

# ── 6. Evaluate on Test Set ───────────────────
y_pred = model.predict(X_test)

mae  = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred) ** 0.5
r2   = r2_score(y_test, y_pred)

print("── Model Performance ──────────────────")
print(f"  MAE  (Mean Absolute Error) : {mae:,.0f} litres")
print(f"  RMSE (Root Mean Sq. Error) : {rmse:,.0f} litres")
print(f"  R²   (Explained Variance)  : {r2:.4f}")
print("───────────────────────────────────────\n")

# ── 7. Feature Importance ─────────────────────
importance = pd.Series(model.feature_importances_, index=FEATURES)
importance = importance.sort_values(ascending=False)

print("── Feature Importance ─────────────────")
for feat, score in importance.items():
    bar = "█" * int(score * 40)
    print(f"  {feat:<20} {bar} {score:.4f}")
print("───────────────────────────────────────\n")

# ── 8. Save Model ─────────────────────────────
MODEL_PATH = "xgboost_model.pkl"
with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)
print(f"Model saved to '{MODEL_PATH}'\n")

# ── 9. Quick Prediction Example ───────────────
print("── Sample Prediction ──────────────────")
sample = pd.DataFrame([{
    "temperature"      : 32.0,
    "rainfall"         : 0.0,
    "humidity"         : 65.0,
    "occupancy"        : 310,
    "timetable_factor" : 0.95,
    "day_of_week"      : 1,    # Tuesday
    "month"            : 7,
    "day_of_year"      : 192,
    "is_weekend"       : 0,
}])

prediction = model.predict(sample)[0]
print(f"  Input  → temp=32°C, occupancy=310, timetable=0.95")
print(f"  Output → Predicted water usage: {prediction:,.0f} litres")
print("───────────────────────────────────────")
