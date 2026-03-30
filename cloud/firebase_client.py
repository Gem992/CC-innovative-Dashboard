"""
Firebase Firestore Client – Agent 2
Uses firebase-admin SDK.  Falls back to an in-memory store when no credentials
are provided so the app can still run locally during development.
"""

import os
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any

# ── Try to initialise Firebase ─────────────────────────────────────────────
_db = None

try:
    import firebase_admin
    from firebase_admin import credentials, firestore

    _cred_path = os.environ.get("FIREBASE_CREDENTIALS_PATH", "serviceAccountKey.json")

    if os.path.exists(_cred_path):
        if not firebase_admin._apps:
            cred = credentials.Certificate(_cred_path)
            firebase_admin.initialize_app(cred)
        _db = firestore.client()
        print("✅ Connected to Firebase Firestore.")
    else:
        print(
            "⚠️  serviceAccountKey.json not found – using in-memory store.\n"
            "   Set FIREBASE_CREDENTIALS_PATH env var to use real Firestore."
        )
except ImportError:
    print("⚠️  firebase-admin not installed – using in-memory store.")


# ── In-memory fallback ─────────────────────────────────────────────────────
_store: List[Dict[str, Any]] = []
_store_predictions: List[Dict[str, Any]] = []


# ── Public helpers ─────────────────────────────────────────────────────────

def save_reading(data: dict) -> str:
    """Persist a sensor reading. Returns the document / record id."""
    doc_id = data.get("reading_id", str(uuid.uuid4()))
    payload = {**data, "saved_at": datetime.now(timezone.utc).isoformat()}

    if _db:
        _db.collection("sensor_readings").document(doc_id).set(payload)
    else:
        _store.append({**payload, "id": doc_id})

    return doc_id


def get_all_readings() -> List[Dict[str, Any]]:
    """Retrieve all stored sensor readings."""
    if _db:
        docs = _db.collection("sensor_readings").order_by(
            "timestamp", direction=firestore.Query.DESCENDING
        ).limit(200).stream()
        return [{"id": d.id, **d.to_dict()} for d in docs]
    return list(reversed(_store[-200:]))


def save_prediction(prediction: dict) -> str:
    """Persist a model prediction record."""
    doc_id = str(uuid.uuid4())
    payload = {**prediction, "id": doc_id}

    if _db:
        _db.collection("predictions").document(doc_id).set(payload)
    else:
        _store_predictions.append(payload)

    return doc_id




def get_all_predictions() -> List[Dict[str, Any]]:
    """Retrieve all stored predictions."""
    if _db:
        docs = _db.collection("predictions").order_by(
            "timestamp", direction=firestore.Query.DESCENDING
        ).limit(200).stream()
        return [{"id": d.id, **d.to_dict()} for d in docs]
    return list(reversed(_store_predictions[-200:]))
