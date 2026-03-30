# Smart Cloud–Edge AI System for IoT Devices

A full-stack demonstration of a modern AI-powered IoT pipeline with 5 independent-yet-interconnected modules.

```
IoT Sensor → Edge Filter → Cloud API → AI/ML Inference → Firebase
                                                     ↓
                                         React Dashboard (live)
                ↕
         Quantum Scheduler Demo
```

---

## Project Structure

See [`folder_structure.txt`](./folder_structure.txt) for the full layout.

| Module | Tech | Port |
|---|---|---|
| **Agent 1 – Edge** | Python, Flask | 5001 |
| **Agent 2 – Cloud** | Python, FastAPI | 8000 |
| **Agent 3 – ML** | scikit-learn, joblib | — |
| **Agent 4 – Dashboard** | React, Vite, Recharts | 3000 |
| **Agent 5 – Quantum** | Qiskit | — |

---

## Quick Start (All Modules Together)

Open **5 terminals** and run each module in order:

### 1 · Cloud Backend (start first — needs ML models)
```bash
cd inn
pip install -r cloud/requirements.txt -r ml/requirements.txt
python ml/train.py              # train & save models once
uvicorn cloud.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2 · Edge Server
```bash
cd inn/edge
pip install -r requirements.txt
python edge_server.py
```

### 3 · IoT Sensor Simulator
```bash
cd inn/edge
python sensor_simulator.py
```

### 4 · React Dashboard
```bash
cd inn/dashboard
npm install
npm run dev
# Open http://localhost:3000
```

### 5 · Quantum Comparison (standalone)
```bash
cd inn/quantum
pip install -r requirements.txt
python compare.py
```

---

## Module READMEs

- [Edge Layer](./edge/README.md)
- [Cloud Backend](./cloud/README.md)
- [AI/ML Module](./ml/README.md)
- [Dashboard](./dashboard/README.md)
- [Quantum Module](./quantum/README.md)

---

## Firebase Setup (optional — works without it)

1. Create a free project at [console.firebase.google.com](https://console.firebase.google.com)
2. Enable **Cloud Firestore** in Native mode
3. Go to **Project Settings → Service Accounts → Generate new private key**
4. Save as `inn/cloud/serviceAccountKey.json`
5. The cloud backend auto-detects and uses it; otherwise falls back to in-memory storage.

---

## Architecture

```
[IoT Devices]
     │  (every 3 s)
     ▼
[Edge Server :5001]  ◄─── sensor_simulator.py
  edge_filter.py
  (temp > 30°C?)
     │ YES (anomaly only)
     ▼
[Cloud API :8000]
  FastAPI
  ml/model.py → Linear Regression + Isolation Forest
  firebase_client.py → Firestore / in-memory
     │
     ▼
[Firebase Firestore]  ◄──────────────────┐
                                         │ GET /data/all
                                         │ GET /predictions
                                    [Dashboard :3000]
                                     React + Recharts
                                     (polls every 3 s)
```

---

## Free-Tier Services Used

| Service | Usage |
|---|---|
| Firebase Firestore | Time-series sensor & prediction storage (1 GiB free) |
| Render.com | Optional cloud deployment for FastAPI backend (free tier) |
| Qiskit StatevectorSampler | Local quantum simulation (no quantum hardware needed) |

---

## License
MIT
