import { useState, useEffect, useCallback, useRef } from 'react'
import StatCard from './components/StatCard'
import SensorChart from './components/SensorChart'
import PredictionChart from './components/PredictionChart'
import AnomalyAlerts from './components/AnomalyAlerts'
import LatencyPanel from './components/LatencyPanel'
import DataTable from './components/DataTable'

const CLOUD_BASE    = 'http://localhost:8000'
const POLL_INTERVAL = 3000   // ms
const DEVICES       = ['device-001','device-002','device-003','device-004','device-005']

// ── Mock data generator (shown when backend is offline) ────────────────────
let _mockStore     = []
let _mockPredStore = []

function makeMockReading() {
  const temp      = +(18 + Math.random() * 24).toFixed(2)  // 18–42 °C
  const humidity  = +(30 + Math.random() * 60).toFixed(2)
  const device    = DEVICES[Math.floor(Math.random() * DEVICES.length)]
  const now       = new Date().toISOString()
  const reading_id = crypto.randomUUID()
  const edgeMs    = +(0.5 + Math.random() * 2).toFixed(2)

  const reading = { device_id: device, temperature: temp, humidity, timestamp: now, reading_id, edge_latency_ms: edgeMs }

  // simple "prediction" using a sine model
  const hour = new Date().getHours() + new Date().getMinutes() / 60
  const predicted = +(22 + 8 * Math.sin((hour - 4) * Math.PI / 12)).toFixed(2)
  const delta     = +Math.abs(temp - predicted).toFixed(2)
  const is_anomaly_lr  = delta > 5 || temp > 30
  const is_anomaly_iso = temp > 35
  const pred = {
    id: crypto.randomUUID(),
    reading_id,
    device_id: device,
    timestamp: now,
    actual_temperature: temp,
    predicted_temperature: predicted,
    delta,
    is_anomaly_lr,
    is_anomaly_iso,
    anomaly_score: +(delta / Math.max(predicted, 1) * 100).toFixed(1),
    inference_ms: +(1 + Math.random() * 4).toFixed(2),
  }

  _mockStore.unshift(reading)
  if (_mockStore.length > 200) _mockStore.pop()
  if (is_anomaly_lr || is_anomaly_iso) {
    _mockPredStore.unshift(pred)
    if (_mockPredStore.length > 200) _mockPredStore.pop()
  }

  return { readings: [..._mockStore], predictions: [..._mockPredStore] }
}

// ── Data hook ──────────────────────────────────────────────────────────────
function useCloudData() {
  const [readings, setReadings]       = useState([])
  const [predictions, setPredictions] = useState([])
  const [status, setStatus]           = useState('connecting')
  const [mode, setMode]               = useState('live')   // 'live' | 'demo'
  const [lastUpdate, setLastUpdate]   = useState(null)
  const failCount = useRef(0)

  const fetchLive = useCallback(async () => {
    try {
      const [rRes, pRes] = await Promise.all([
        fetch(`${CLOUD_BASE}/data/all?limit=100`),
        fetch(`${CLOUD_BASE}/predictions?limit=100`),
      ])
      if (!rRes.ok || !pRes.ok) throw new Error('API error')
      const [rData, pData] = await Promise.all([rRes.json(), pRes.json()])
      failCount.current = 0
      setReadings(rData)
      setPredictions(pData)
      setStatus('live')
      setMode('live')
      setLastUpdate(new Date())
    } catch {
      failCount.current += 1
      if (failCount.current >= 2) {
        setStatus('offline')
        setMode('demo')
      }
    }
  }, [])

  // Demo tick — generates a new mock reading every 3 s when offline
  const tickDemo = useCallback(() => {
    const { readings: r, predictions: p } = makeMockReading()
    setReadings(r)
    setPredictions(p)
    setLastUpdate(new Date())
  }, [])

  useEffect(() => {
    fetchLive()
    const interval = setInterval(() => {
      if (failCount.current < 2) {
        fetchLive()
      } else {
        tickDemo()
      }
    }, POLL_INTERVAL)
    return () => clearInterval(interval)
  }, [fetchLive, tickDemo])

  return { readings, predictions, status, mode, lastUpdate }
}

// ── App ────────────────────────────────────────────────────────────────────
export default function App() {
  const { readings, predictions, status, mode, lastUpdate } = useCloudData()

  const totalReadings  = readings.length
  const anomalyCount   = predictions.filter(p => p.is_anomaly_lr || p.is_anomaly_iso).length
  const latestTemp     = readings[0]?.temperature?.toFixed(1) ?? '—'
  const latestHumidity = readings[0]?.humidity?.toFixed(1) ?? '—'
  const uniqueDevices  = new Set(readings.map(r => r.device_id)).size
  const avgDelta       = predictions.length
    ? (predictions.reduce((s, p) => s + (p.delta || 0), 0) / predictions.length).toFixed(1)
    : '—'

  return (
    <div className="app-wrapper">
      {/* ── Header ─────────────────────────────────────────────────────── */}
      <header className="header">
        <div className="header-left">
          <div className="header-logo">🛰️</div>
          <div>
            <div className="header-title">Smart Cloud–Edge AI System</div>
            <div className="header-sub">IoT Real-time Monitoring Dashboard</div>
          </div>
        </div>
        <div className="header-right">
          <span className={`status-badge ${status === 'live' ? 'live' : status === 'offline' ? 'error' : 'live'}`}>
            <span className="status-dot" />
            {status === 'live'       ? 'Live – Cloud Connected'
           : status === 'offline'    ? 'Demo Mode (Cloud Offline)'
           : 'Connecting…'}
          </span>
          {mode === 'demo' && (
            <span style={{
              fontSize: '0.7rem', background: 'rgba(251,146,60,0.12)',
              color: '#fb923c', padding: '3px 10px', borderRadius: '100px',
              border: '1px solid rgba(251,146,60,0.3)'
            }}>
              🎭 Simulated data
            </span>
          )}
          <span className="refresh-info">
            {lastUpdate ? `Updated ${lastUpdate.toLocaleTimeString()}` : 'Polling every 3 s'}
          </span>
        </div>
      </header>

      {/* ── Main ───────────────────────────────────────────────────────── */}
      <main className="main-content">

        {/* Backend offline banner */}
        {mode === 'demo' && (
          <div style={{
            background: 'rgba(251,146,60,0.08)', border: '1px solid rgba(251,146,60,0.25)',
            borderRadius: 'var(--radius-md)', padding: '12px 18px',
            display: 'flex', alignItems: 'center', gap: 10,
            marginBottom: 22, fontSize: '0.82rem', color: '#fb923c'
          }}>
            <span style={{ fontSize: 18 }}>⚠️</span>
            <span>
              <strong>Cloud backend not reachable.</strong> Showing simulated demo data. 
              Start the backend: <code style={{ fontFamily: 'JetBrains Mono, monospace', background: 'rgba(0,0,0,0.3)', padding: '2px 6px', borderRadius: 4 }}>
                uvicorn cloud.main:app --host 0.0.0.0 --port 8000
              </code> from the <code style={{ fontFamily: 'JetBrains Mono, monospace', background: 'rgba(0,0,0,0.3)', padding: '2px 6px', borderRadius: 4 }}>inn/</code> directory.
            </span>
          </div>
        )}

        {/* KPI strip */}
        <div className="stats-grid">
          <StatCard icon="🌡️" label="Latest Temperature" value={latestTemp} unit="°C"
            sub="Most recent reading" colorClass="stat-orange" glowClass="stat-glow-orange" />
          <StatCard icon="💧" label="Latest Humidity"    value={latestHumidity} unit="%"
            sub="Most recent reading" colorClass="stat-cyan"   glowClass="stat-glow-cyan" />
          <StatCard icon="📡" label="Total Readings"     value={totalReadings}
            sub="In store" colorClass="stat-blue"   glowClass="stat-glow-blue" />
          <StatCard icon="⚠️" label="Anomalies"          value={anomalyCount}
            sub="Detected by AI" colorClass="stat-red"    glowClass="stat-glow-red" />
          <StatCard icon="🖥️" label="Active Devices"    value={uniqueDevices}
            sub="Unique device IDs" colorClass="stat-green"  glowClass="stat-glow-green" />
          <StatCard icon="🤖" label="Avg Pred. Δ"        value={avgDelta} unit="°C"
            sub="LR model error" colorClass="stat-purple" glowClass="stat-glow-purple" />
        </div>

        {/* Live charts row */}
        <div className="charts-grid">
          <SensorChart data={readings} />
          <PredictionChart data={predictions} />
        </div>

        {/* Alerts + Latency row */}
        <div className="charts-grid">
          <AnomalyAlerts predictions={predictions} />
          <LatencyPanel readings={readings} />
        </div>

        {/* Raw data table */}
        <DataTable readings={readings} />

      </main>
    </div>
  )
}
