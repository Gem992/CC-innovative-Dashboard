/* StatCard – KPI tile */
export default function StatCard({ icon, label, value, unit, sub, colorClass, glowClass }) {
  return (
    <div className={`stat-card ${glowClass || ''}`}>
      <div className="stat-icon">{icon}</div>
      <div className="stat-label">{label}</div>
      <div className={`stat-value ${colorClass || ''}`}>
        {value}
        {unit && <span style={{ fontSize: '1rem', marginLeft: 4 }}>{unit}</span>}
      </div>
      {sub && <div className="stat-sub">{sub}</div>}
    </div>
  )
}
