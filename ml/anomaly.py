"""
Anomaly Utilities – Agent 3
Standalone anomaly scoring helpers used by the cloud backend.
"""

from typing import List, Dict, Any


TEMP_SPIKE_THRESHOLD = 5.0     # °C delta from prediction → anomaly
ABSOLUTE_THRESHOLD   = 30.0    # °C absolute temperature → anomaly


def score_reading(
    actual: float,
    predicted: float,
    humidity: float | None = None,
) -> Dict[str, Any]:
    """
    Calculate a composite anomaly score for a sensor reading.

    Returns a dict with:
      - score      : 0.0–100.0 (higher = more anomalous)
      - is_anomaly : bool
      - reasons    : list of human-readable reason strings
    """
    reasons: List[str] = []
    score = 0.0

    delta = abs(actual - predicted)

    # Rule 1 – large deviation from ML prediction
    if delta > TEMP_SPIKE_THRESHOLD:
        score += min(delta * 8, 50)
        reasons.append(f"Temp deviated {delta:.1f}°C from prediction")

    # Rule 2 – absolute high temperature
    if actual > ABSOLUTE_THRESHOLD:
        excess = actual - ABSOLUTE_THRESHOLD
        score += min(excess * 5, 40)
        reasons.append(f"Absolute temp {actual:.1f}°C exceeds {ABSOLUTE_THRESHOLD}°C")

    # Rule 3 – extreme humidity (optional)
    if humidity is not None:
        if humidity > 90 or humidity < 10:
            score += 10
            reasons.append(f"Unusual humidity: {humidity:.1f}%")

    score = min(score, 100.0)
    is_anomaly = score >= 20.0 or actual > ABSOLUTE_THRESHOLD

    return {
        "score": round(score, 1),
        "is_anomaly": is_anomaly,
        "reasons": reasons,
    }
