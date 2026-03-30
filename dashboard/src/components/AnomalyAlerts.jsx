export default function AnomalyAlerts({ predictions }) {
  const anomalies = (predictions || [])
    .filter(p => p.is_anomaly_lr || p.is_anomaly_iso)
    .slice(-15)
    .reverse()

  return (
    <div className="card">
      <div className="card-header">
        <span className="card-title">⚠️ Anomaly Alerts</span>
        {anomalies.length > 0 && (
          <span style={{
            background: 'rgba(248,113,113,0.15)', color: 'var(--accent-red)',
            fontSize: '0.7rem', fontWeight: 700, padding: '2px 10px',
            borderRadius: '100px', border: '1px solid rgba(248,113,113,0.3)'
          }}>
            {anomalies.length} detected
          </span>
        )}
      </div>
      {anomalies.length === 0
        ? (
          <div className="empty-state">
            <div style={{ fontSize: 28, marginBottom: 8 }}>✅</div>
            No anomalies detected. All readings within normal range.
          </div>
        )
        : (
          <div className="alert-list">
            {anomalies.map((a, i) => (
              <div key={a.id || i} className="alert-item">
                <span className="alert-icon">🔴</span>
                <div className="alert-main">
                  <div className="alert-title">
                    {a.device_id} — {a.actual_temperature?.toFixed(1)}°C
                    {a.is_anomaly_lr && ' · LR anomaly'}
                    {a.is_anomaly_iso && ' · IsoForest anomaly'}
                  </div>
                  <div className="alert-body">
                    Predicted: {a.predicted_temperature?.toFixed(1)}°C &nbsp;|&nbsp;
                    Δ {a.delta?.toFixed(1)}°C &nbsp;|&nbsp;
                    Score: {a.anomaly_score?.toFixed(0)}%
                  </div>
                  <div className="alert-time">{new Date(a.timestamp).toLocaleString()}</div>
                </div>
              </div>
            ))}
          </div>
        )
      }
    </div>
  )
}
