import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer
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
          {p.name}: <strong>{p.value}</strong>
        </p>
      ))}
    </div>
  )
}

export default function SensorChart({ data }) {
  const chartData = (data || []).slice(-30).map((r, i) => ({
    time: new Date(r.timestamp).toLocaleTimeString(),
    Temperature: Number(r.temperature?.toFixed(1)),
    Humidity: Number(r.humidity?.toFixed(1)),
    device: r.device_id,
  }))

  return (
    <div className="card">
      <div className="card-header">
        <span className="card-title">🌡️ Live Sensor Data</span>
        <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
          Last {chartData.length} readings
        </span>
      </div>
      {chartData.length === 0
        ? <div className="empty-state">No data yet. Waiting for sensor readings…</div>
        : (
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={chartData} margin={{ top: 4, right: 12, bottom: 4, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
              <XAxis dataKey="time" tick={{ fontSize: 10, fill: '#475569' }} tickLine={false} />
              <YAxis tick={{ fontSize: 10, fill: '#475569' }} tickLine={false} axisLine={false} />
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ fontSize: '0.75rem', paddingTop: 10 }} />
              <Line
                type="monotone" dataKey="Temperature"
                stroke="#4f9cf9" strokeWidth={2} dot={false}
                activeDot={{ r: 4, fill: '#4f9cf9' }}
              />
              <Line
                type="monotone" dataKey="Humidity"
                stroke="#22d3ee" strokeWidth={2} dot={false}
                activeDot={{ r: 4, fill: '#22d3ee' }}
              />
            </LineChart>
          </ResponsiveContainer>
        )
      }
    </div>
  )
}
