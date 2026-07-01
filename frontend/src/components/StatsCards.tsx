import { useSafetyStore } from '../store/safetyStore';

export default function StatsCards() {
  const stats = useSafetyStore((s) => s.stats);

  if (!stats) return <div style={{ color: 'var(--text-dim)' }}>Loading stats...</div>;

  const cards = [
    { label: 'Total Incidents', value: stats.incidents.total, color: 'var(--accent)' },
    { label: 'Open Incidents', value: stats.incidents.open, color: '#f97316' },
    { label: 'Active Permits', value: stats.permits.active, color: '#22c55e' },
    { label: 'Safety Score', value: `${stats.safety_score}/100`, color: stats.safety_score >= 60 ? '#22c55e' : 'var(--accent)' },
  ];

  return (
    <div className="grid grid-4">
      {cards.map((c) => (
        <div key={c.label} className="card" style={{ textAlign: 'center' }}>
          <div style={{ fontSize: 32, fontWeight: 700, color: c.color }}>{c.value}</div>
          <div style={{ fontSize: 13, color: 'var(--text-dim)', marginTop: 4 }}>{c.label}</div>
        </div>
      ))}
    </div>
  );
}
