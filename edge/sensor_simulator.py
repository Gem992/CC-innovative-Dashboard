"""
IoT Sensor Simulator – Agent 1
Generates fake sensor readings every 3 seconds.

Data flow:
  1. POST  → edge server (filters, forwards anomalies only)
  2. POST  → cloud API directly (ALL readings, for full dashboard visibility)

Run: python sensor_simulator.py
"""

import random
import time
import uuid
import requests
from datetime import datetime, timezone

EDGE_URL  = "http://localhost:5001/edge/send"
CLOUD_URL = "http://localhost:8000/data"        # direct, bypasses edge filter

DEVICE_IDS = [f"device-{i:03d}" for i in range(1, 6)]

# Track connectivity so we don't spam errors
_edge_ok  = True
_cloud_ok = True


def generate_reading() -> dict:
    return {
        "device_id":   random.choice(DEVICE_IDS),
        "temperature": round(random.uniform(18.0, 42.0), 2),   # °C
        "humidity":    round(random.uniform(30.0, 90.0), 2),   # %
        "timestamp":   datetime.now(timezone.utc).isoformat(),
        "reading_id":  str(uuid.uuid4()),
    }


def send_to_edge(reading: dict) -> None:
    global _edge_ok
    try:
        resp = requests.post(EDGE_URL, json=reading, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("forwarded"):
                print(f"  ⚡ ANOMALY forwarded to cloud via edge  "
                      f"(edge: {data.get('edge_latency_ms')} ms, "
                      f"cloud: {data.get('cloud_latency_ms')} ms)")
            else:
                print(f"  ✅ Normal reading – filtered at edge.")
            _edge_ok = True
        else:
            print(f"  ⚠️  Edge server returned {resp.status_code}")
    except requests.exceptions.ConnectionError:
        if _edge_ok:
            print("  ❌ Edge server not reachable (start edge_server.py)")
        _edge_ok = False


def send_to_cloud(reading: dict) -> None:
    """Send ALL readings directly to cloud for full dashboard visibility."""
    global _cloud_ok
    try:
        payload = {**reading, "source": "direct"}
        requests.post(CLOUD_URL, json=payload, timeout=5)
        _cloud_ok = True
    except requests.exceptions.ConnectionError:
        if _cloud_ok:
            print("  ❌ Cloud API not reachable (start cloud backend first)")
        _cloud_ok = False


def run_simulator(interval: float = 3.0) -> None:
    print("🚀 IoT Sensor Simulator started  │  Ctrl+C to stop")
    print("─" * 62)
    while True:
        reading = generate_reading()
        t_str   = reading["timestamp"][11:19]   # HH:MM:SS
        print(f"[{t_str}] {reading['device_id']}  "
              f"Temp: {reading['temperature']:5.1f}°C  "
              f"Humidity: {reading['humidity']:5.1f}%")

        send_to_edge(reading)    # edge filter: only anomalies go to cloud
        send_to_cloud(reading)   # direct: all readings stored for dashboard

        time.sleep(interval)


if __name__ == "__main__":
    run_simulator()
