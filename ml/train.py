"""
ML Training Script – Agent 3
Standalone script to retrain the models and display evaluation metrics.
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "lr_model.pkl")
ANOMALY_MODEL_PATH = os.path.join(os.path.dirname(__file__), "iso_forest.pkl")


def generate_dataset(n: int = 1000):
    """
    Synthetic IoT temperature dataset.
    Feature: hour_of_day (float 0–24)
    Target:  temperature (°C) with diurnal pattern + Gaussian noise
    """
    np.random.seed(42)
    hours = np.random.uniform(0, 24, n)

    # Diurnal pattern: peak ~14:00, trough ~04:00
    temp = 22 + 8 * np.sin((hours - 4) * np.pi / 12) + np.random.normal(0, 1.5, n)

    # Inject ~5% anomalies (sudden spikes)
    anomaly_idx = np.random.choice(n, size=int(0.05 * n), replace=False)
    temp[anomaly_idx] += np.random.uniform(10, 20, len(anomaly_idx))

    return hours.reshape(-1, 1), temp


def train():
    print("🔧 Generating synthetic training data …")
    X, y = generate_dataset(1000)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # ── Linear Regression ─────────────────────────────────────────────────
    print("\n📈 Training Linear Regression …")
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_test)

    print(f"   MAE  : {mean_absolute_error(y_test, y_pred):.3f} °C")
    print(f"   RMSE : {np.sqrt(mean_squared_error(y_test, y_pred)):.3f} °C")
    print(f"   R²   : {r2_score(y_test, y_pred):.4f}")

    joblib.dump(lr, MODEL_PATH)
    print(f"   ✅ Saved to {MODEL_PATH}")

    # ── Isolation Forest ──────────────────────────────────────────────────
    print("\n🌲 Training Isolation Forest …")
    iso = IsolationForest(contamination=0.05, random_state=42, n_estimators=200)
    iso.fit(X_train)

    iso_labels = iso.predict(X_test)
    n_anomalies = (iso_labels == -1).sum()
    print(f"   Detected anomalies in test set: {n_anomalies} / {len(X_test)}")

    joblib.dump(iso, ANOMALY_MODEL_PATH)
    print(f"   ✅ Saved to {ANOMALY_MODEL_PATH}")

    print("\n🎉 Training complete!")


if __name__ == "__main__":
    train()
