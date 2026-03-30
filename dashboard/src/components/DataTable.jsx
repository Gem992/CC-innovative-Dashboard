export default function DataTable({ readings }) {
  const rows = (readings || []).slice(0, 50)

  return (
    <div className="card">
      <div className="card-header">
        <span className="card-title">📋 Raw Sensor Readings</span>
        <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Latest {rows.length}</span>
      </div>
      {rows.length === 0
        ? <div className="empty-state">No readings in store.</div>
        : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Device</th>
                  <th>Temp (°C)</th>
                  <th>Humidity (%)</th>
                  <th>Edge Latency</th>
                  <th>Timestamp</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((r, i) => {
                  const isAnomaly = (r.temperature || 0) > 30
                  return (
                    <tr key={r.reading_id || i}>
                      <td className="mono">{r.device_id}</td>
                      <td style={{ color: isAnomaly ? 'var(--accent-red)' : 'var(--accent-green)', fontWeight: 600 }}>
                        {r.temperature?.toFixed(1)}
                      </td>
                      <td style={{ color: 'var(--accent-cyan)' }}>{r.humidity?.toFixed(1)}</td>
                      <td className="mono" style={{ color: 'var(--text-muted)' }}>
                        {r.edge_latency_ms ? `${r.edge_latency_ms} ms` : '—'}
                      </td>
                      <td className="mono" style={{ color: 'var(--text-muted)', fontSize: '0.72rem' }}>
                        {new Date(r.timestamp).toLocaleTimeString()}
                      </td>
                      <td>
                        <span className={`badge ${isAnomaly ? 'badge-anomaly' : 'badge-normal'}`}>
                          {isAnomaly ? '⚠ anomaly' : '✓ normal'}
                        </span>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        )
      }
    </div>
  )
}
