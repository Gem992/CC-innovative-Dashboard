# Agent 1 — IoT & Edge Layer

## Overview
Simulates IoT sensor data and filters anomalies before forwarding to the cloud backend.

## Components
| File | Purpose |
|---|---|
| `sensor_simulator.py` | Generates fake device readings every 3 s |
| `edge_filter.py` | Anomaly filter (temp > 30°C) |
| `edge_server.py` | Flask server exposing `POST /edge/send` |

## Setup & Run

```bash
cd edge
pip install -r requirements.txt

# Terminal 1 – start edge server
python edge_server.py

# Terminal 2 – start IoT simulator (requires edge server running)
python sensor_simulator.py
```

## Configuration
| Variable | Default | Description |
|---|---|---|
| `CLOUD_URL` | `http://localhost:8000/data` | Cloud backend endpoint (in `edge_server.py`) |
| `TEMP_THRESHOLD` | `30.0` | Anomaly threshold in °C (in `edge_filter.py`) |

## API
```
POST /edge/send
Content-Type: application/json

{
  "device_id": "device-001",
  "temperature": 35.5,
  "humidity": 60.0,
  "timestamp": "2025-01-01T12:00:00+00:00",
  "reading_id": "uuid"
}
```
Returns a JSON object indicating whether the reading was forwarded and latency metrics.
