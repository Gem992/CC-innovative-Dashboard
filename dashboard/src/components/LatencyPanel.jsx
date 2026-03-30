import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Cell
} from 'recharts'

export default function LatencyPanel({ readings }) {
  const recent = (readings || []).slice(-20)

  const avgEdge = recent.length
    ? (recent.reduce((s, r) => s + (r.edge_latency_ms || 0), 0) / recent.length).toFixed(1)
    : '—'

  const chartData = recent.map((r, i) => ({
    idx: i + 1,
    Edge: r.edge_latency_ms || 0,
  }))

  return (
    <div className="card">
      <div className="card-header">
        <span className="card-title">⚡ Edge vs Cloud Latency</span>
        <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Last 20 forwarded readings</span>
      </div>

      <div className="latency-row" style={{ marginBottom: 16 }}>
        <div className="latency-item">
          <div className="latency-label">Avg Edge Filter</div>
          <div className="latency-value stat-cyan">{avgEdge} <span style={{ fontSize: '0.8rem' }}>ms</span></div>
        </div>
        <div className="latency-item">
          <div className="latency-label">Cloud Inference</div>
          <div className="latency-value stat-purple">~2–8 <span style={{ fontSize: '0.8rem' }}>ms</span></div>
        </div>
        <div className="latency-item">
          <div className="latency-label">Poll Interval</div>
          <div className="latency-value stat-blue">3 <span style={{ fontSize: '0.8rem' }}>s</span></div>
        </div>
      </div>

      {chartData.length === 0
        ? <div className="empty-state">No forwarded readings yet.</div>
        : (
          <ResponsiveContainer width="100%" height={160}>
            <BarChart data={chartData} margin={{ top: 4, right: 8, bottom: 0, left: -20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
              <XAxis dataKey="idx" tick={{ fontSize: 9, fill: '#475569' }} tickLine={false} />
              <YAxis tick={{ fontSize: 9, fill: '#475569' }} tickLine={false} axisLine={false} unit="ms" />
              <Tooltip
                contentStyle={{ background: '#131929', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 8, fontSize: '0.75rem' }}
                labelStyle={{ color: '#94a3b8' }}
              />
              <Bar dataKey="Edge" radius={[3, 3, 0, 0]}>
                {chartData.map((_, i) => (
                  <Cell key={i} fill={`hsl(${190 + i * 3}, 80%, 60%)`} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        )
      }
    </div>
  )
}
