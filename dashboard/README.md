# Agent 4 — React Dashboard

## Overview
Real-time web dashboard polling the cloud API every 3 seconds and visualizing sensor data, AI predictions, anomaly alerts, and edge/cloud latency.

## Tech Stack
- **Vite** (dev server, HMR)
- **React 18**
- **Recharts** (all charts)
- **Lucide React** (icons)
- **Vanilla CSS** (custom dark design system)

## Setup & Run

```bash
cd dashboard
npm install
npm run dev
# → http://localhost:3000
```

> The dashboard expects the Cloud Backend running at `http://localhost:8000`.
> Update `CLOUD_BASE` in `src/App.jsx` if your backend is hosted elsewhere.

## Panels

| Panel | Description |
|---|---|
| **KPI Cards** | Latest temp, humidity, total readings, anomaly count, active devices, avg prediction error |
| **Live Sensor Data** | Temperature + humidity line chart (last 30 readings) |
| **AI Predictions vs Actual** | LR predicted vs actual temperature with 30°C anomaly reference line |
| **Anomaly Alerts** | Scrollable feed of flagged readings from LR + Isolation Forest |
| **Edge vs Cloud Latency** | Bar chart of edge filter latency per forwarded reading |
| **Raw Readings Table** | Full data table with color-coded status badges |

## Build for Production
```bash
npm run build
npm run preview
```
