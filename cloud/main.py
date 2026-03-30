"""
Cloud Backend – Agent 2
FastAPI server:
  POST  /data          – receive edge data, run ML inference, store result
  GET   /data/all      – all stored readings (newest first)
  GET   /predictions   – all AI predictions (newest first)
  GET   /health        – health check
"""

import sys
import os
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

# ── Make sure both inn/ and inn/cloud/ are on sys.path ─────────────────────
_THIS_DIR   = os.path.dirname(os.path.abspath(__file__))   # …/inn/cloud
_ROOT_DIR   = os.path.dirname(_THIS_DIR)                   # …/inn

for _p in (_ROOT_DIR, _THIS_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ── Firebase / in-memory store ──────────────────────────────────────────────
import firebase_client as _fb        # lives in inn/cloud/ (same directory)

save_reading        = _fb.save_reading
get_all_readings    = _fb.get_all_readings
save_prediction     = _fb.save_prediction
get_all_predictions = _fb.get_all_predictions

# ── ML module (optional – works without it) ─────────────────────────────────
ML_AVAILABLE  = False
full_inference = None

try:
    import importlib.util as _ilu
    _spec = _ilu.spec_from_file_location(
        "ml_model",
        os.path.join(_ROOT_DIR, "ml", "model.py")
    )
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)        # type: ignore[union-attr]
    full_inference = _mod.full_inference
    ML_AVAILABLE   = True
    print("✅  ML module loaded.")
except Exception as _e:
    print(f"⚠️   ML module unavailable: {_e}")

# ── App ─────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Smart IoT Cloud Backend",
    description="Cloud API for the Smart Cloud–Edge AI System",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Schemas ──────────────────────────────────────────────────────────────────
class SensorReading(BaseModel):
    device_id: str
    temperature: float
    humidity: float
    timestamp: str
    reading_id: Optional[str] = None
    edge_latency_ms: Optional[float] = None
    source: Optional[str] = "edge"   # "edge" | "direct"


# ── Routes ───────────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {
        "status": "ok",
        "ml_available": ML_AVAILABLE,
        "ts": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/data")
def ingest_reading(reading: SensorReading):
    """Store the reading and run AI inference."""
    data = reading.model_dump()
    doc_id = save_reading(data)

    # ── ML inference ────────────────────────────────────────────────────────
    prediction_record: Dict[str, Any] = {
        "reading_id": doc_id,
        "device_id":  reading.device_id,
        "timestamp":  reading.timestamp,
        "actual_temperature": reading.temperature,
    }

    if ML_AVAILABLE and full_inference is not None:
        try:
            dt   = datetime.fromisoformat(reading.timestamp.replace("Z", "+00:00"))
            hour = dt.hour + dt.minute / 60.0

            t0           = time.perf_counter()
            inference    = full_inference(hour, reading.temperature)
            inference_ms = round((time.perf_counter() - t0) * 1000, 2)

            prediction_record.update({**inference, "inference_ms": inference_ms})
        except Exception as exc:
            prediction_record["ml_error"] = str(exc)
    else:
        prediction_record["ml_error"] = "ML module unavailable"

    pred_id = save_prediction(prediction_record)
    prediction_record["id"] = pred_id

    return {
        "status": "stored",
        "reading_id": doc_id,
        "prediction": prediction_record,
    }


@app.get("/data/all")
def get_readings(limit: int = 100) -> List[Dict[str, Any]]:
    return get_all_readings()[:limit]


@app.get("/predictions")
def get_predictions(limit: int = 100) -> List[Dict[str, Any]]:
    return get_all_predictions()[:limit]


# ── Entrypoint ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
