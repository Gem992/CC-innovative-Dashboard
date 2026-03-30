"""
ML Model – Agent 3
Linear Regression for temperature prediction + Isolation Forest for anomaly detection.
Models are trained once on startup and reused for every inference call.
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "lr_model.pkl")
ANOMALY_MODEL_PATH = os.path.join(os.path.dirname(__file__), "iso_forest.pkl")


# ── Training data ──────────────────────────────────────────────────────────

def _generate_training_data(n: int = 500):
    """
    Synthetic training data:
      X = hour_of_day (0–23)
      y = expected temperature with a sinusoidal diurnal pattern + noise
    """
    np.random.seed(42)
    hours = np.random.uniform(0, 24, n)
    # Temperature peaks around 14:00, lowest around 04:00
    temp = 22 + 8 * np.sin((hours - 4) * np.pi / 12) + np.random.normal(0, 1.5, n)
    return hours.reshape(-1, 1), temp


# ── Public API ─────────────────────────────────────────────────────────────

def train_and_save():
    """Train both models and persist them to disk."""
    X, y = _generate_training_data()

    lr = LinearRegression()
    lr.fit(X, y)
    joblib.dump(lr, MODEL_PATH)

    iso = IsolationForest(contamination=0.05, random_state=42)
    iso.fit(X)
    joblib.dump(iso, ANOMALY_MODEL_PATH)

    print(f"✅ Models trained and saved → {MODEL_PATH}, {ANOMALY_MODEL_PATH}")
    return lr, iso


def load_models():
    """Load models from disk, training if needed."""
    if os.path.exists(MODEL_PATH) and os.path.exists(ANOMALY_MODEL_PATH):
        lr = joblib.load(MODEL_PATH)
        iso = joblib.load(ANOMALY_MODEL_PATH)
        print("✅ Models loaded from disk.")
    else:
        print("⚙️  No saved models found — training now …")
        lr, iso = train_and_save()
    return lr, iso


# Module-level singletons
_lr_model, _iso_model = load_models()


def predict_temperature(hour: float) -> float:
    """Predict expected temperature for a given hour of day."""
    X = np.array([[hour]])
    return float(_lr_model.predict(X)[0])


def is_anomaly(hour: float) -> bool:
    """
    Return True if the hour/reading pattern is an anomaly
    according to Isolation Forest (-1 = anomaly, 1 = normal).
    """
    X = np.array([[hour]])
    label = _iso_model.predict(X)[0]
    return label == -1


def full_inference(hour: float, actual_temp: float) -> dict:
    """Run both models and return a combined result dict."""
    predicted = predict_temperature(hour)
    anomaly = is_anomaly(hour)
    delta = abs(actual_temp - predicted)
    return {
        "hour": hour,
        "actual_temperature": actual_temp,
        "predicted_temperature": round(predicted, 2),
        "delta": round(delta, 2),
        "is_anomaly_lr": delta > 5.0,      # simple threshold on regression error
        "is_anomaly_iso": anomaly,
        "anomaly_score": round(delta / predicted * 100, 1) if predicted else 0,
    }
