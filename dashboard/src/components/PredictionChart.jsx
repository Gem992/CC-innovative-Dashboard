import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer, ReferenceLine
} from 'recharts'

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div style={{
      background: '#131929', border: '1px solid rgba(255,255,255,0.1)',
      borderRadius: 10, padding: '10px 14px', fontSize: '0.78rem'
    }}>
      <p style={{ color: '#94a3b8', marginBottom: 4 }}>{label}</p>
      {payload.map(p => (
        <p key={p.name} style={{ color: p.color }}>
          {p.name}: <strong>{p.value}°C</strong>
        </p>
      ))}
    </div>
  )
}

export default function PredictionChart({ data }) {
  // data can be either predictions (from cloud) or raw readings with predicted_temperature
  const chartData = (data || []).slice(-30).map(r => ({
    time: new Date(r.timestamp).toLocaleTimeString(),
    Actual: Number((r.actual_temperature ?? r.temperature ?? 0).toFixed(1)),
    Predicted: Number((r.predicted_temperature ?? 0).toFixed(1)),
    anomaly: r.is_anomaly_lr || r.is_anomaly_iso,
  })).filter(r => r.Predicted > 0)

  return (
    <div className="card">
      <div className="card-header">
        <span className="card-title">🤖 AI Predictions vs Actual</span>
        <span style={{
          fontSize: '0.72rem', background: 'rgba(167,139,250,0.12)',
          color: 'var(--accent-purple)', padding: '3px 10px',
          borderRadius: '100px', border: '1px solid rgba(167,139,250,0.25)'
        }}>Linear Regression</span>
      </div>
      {chartData.length === 0
        ? (
          <div className="empty-state">
            <div style={{ fontSize: 28, marginBottom: 8 }}>⏳</div>
            Waiting for predictions… (anomalies trigger cloud inference)
          </div>
        )
        : (
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={chartData} margin={{ top: 4, right: 12, bottom: 4, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
              <XAxis dataKey="time" tick={{ fontSize: 10, fill: '#475569' }} tickLine={false} />
              <YAxis tick={{ fontSize: 10, fill: '#475569' }} tickLine={false} axisLine={false} unit="°C" />
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ fontSize: '0.75rem', paddingTop: 10 }} />
              <ReferenceLine y={30} stroke="rgba(248,113,113,0.4)" strokeDasharray="4 4"
                label={{ value: 'Anomaly Threshold', fill: '#f87171', fontSize: 10 }} />
              <Line type="monotone" dataKey="Actual"    stroke="#fb923c" strokeWidth={2} dot={false}
                activeDot={{ r: 4, fill: '#fb923c' }} />
              <Line type="monotone" dataKey="Predicted" stroke="#a78bfa" strokeWidth={2} dot={false}
                strokeDasharray="5 3" activeDot={{ r: 4, fill: '#a78bfa' }} />
            </LineChart>
          </ResponsiveContainer>
        )
      }
    </div>
  )
}
