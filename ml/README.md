# Agent 3 — AI/ML Module

## Overview
Provides temperature prediction (Linear Regression) and anomaly detection (Isolation Forest) for real-time inference on incoming sensor readings.

## Components
| File | Purpose |
|---|---|
| `model.py` | Model inference API used by cloud backend |
| `train.py` | Standalone training script with evaluation metrics |
| `anomaly.py` | Anomaly scoring utilities |

## Setup & Run

```bash
cd ml
pip install -r requirements.txt

# Train models (saved as lr_model.pkl and iso_forest.pkl)
python train.py

# Models are auto-trained on first import if .pkl files are missing
```

## Inference API (used by cloud backend)
```python
from ml.model import full_inference

result = full_inference(hour=14.5, actual_temp=36.2)
# {
#   "hour": 14.5,
#   "actual_temperature": 36.2,
#   "predicted_temperature": 29.84,
#   "delta": 6.36,
#   "is_anomaly_lr": true,
#   "is_anomaly_iso": false,
#   "anomaly_score": 21.3
# }
```

## Models
| Model | Input | Output |
|---|---|---|
| Linear Regression | `hour_of_day` (0–24) | Expected temperature (°C) |
| Isolation Forest | `hour_of_day` (0–24) | Anomaly label (-1 = anomaly, 1 = normal) |
