"""
Edge Filtering Layer – Agent 1
Only forwards anomalies (temperature > 30°C) to the cloud API.
"""

TEMP_THRESHOLD = 30.0   # °C


def is_anomaly(reading: dict) -> bool:
    """Return True if the reading is an anomaly."""
    return reading.get("temperature", 0) > TEMP_THRESHOLD


def filter_reading(reading: dict) -> dict:
    """
    Analyse a sensor reading.
    Returns a result dict with 'forward' flag and reason.
    """
    anomaly = is_anomaly(reading)
    return {
        "forward": anomaly,
        "reason": (
            f"Temperature {reading.get('temperature')}°C exceeds threshold {TEMP_THRESHOLD}°C"
            if anomaly
            else f"Temperature {reading.get('temperature')}°C within normal range"
        ),
        "original": reading,
    }
