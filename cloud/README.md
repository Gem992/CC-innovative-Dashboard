# Agent 2 — Cloud Backend & Database

## Overview
FastAPI backend that stores sensor readings in Firebase Firestore and triggers AI inference on every new reading.

## Components
| File | Purpose |
|---|---|
| `main.py` | FastAPI application with all endpoints |
| `firebase_client.py` | Firestore client with in-memory fallback |

## Setup & Run

```bash
cd cloud
pip install -r requirements.txt

# Optional: add Firebase credentials
# 1. Go to Firebase Console → Project Settings → Service Accounts
# 2. Generate a new private key → save as cloud/serviceAccountKey.json
# 3. Set FIREBASE_CREDENTIALS_PATH=serviceAccountKey.json (or use default path)

# Start server (ML module must be installed)
python main.py
# or
uvicorn cloud.main:app --host 0.0.0.0 --port 8000 --reload
```

> Without `serviceAccountKey.json`, the server uses an **in-memory store** automatically.

## API Endpoints
| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/data` | Ingest sensor reading + run ML inference |
| `GET` | `/data/all` | List all stored readings |
| `GET` | `/predictions` | List all AI predictions |

## Interactive Docs
Visit `http://localhost:8000/docs` after starting the server.
