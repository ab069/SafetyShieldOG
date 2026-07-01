import { useEffect, useState } from 'react';
import { useSafetyStore } from '../store/safetyStore';

export default function IncidentList() {
  const { incidents, fetchIncidents } = useSafetyStore();
  const [expanded, setExpanded] = useState<string | null>(null);

  useEffect(() => { fetchIncidents(); }, []);

  const severityColor = (s: string) => {
    const map: Record<string, string> = {
      critical: 'badge-critical', high: 'badge-high', medium: 'badge-medium', low: 'badge-low',
    };
    return map[s] || 'badge-medium';
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
      <h2 style={{ fontSize: 20 }}>Incidents ({incidents.length})</h2>
      {incidents.map((inc) => (
        <div key={inc.id} className="card" onClick={() => setExpanded(expanded === inc.id ? null : inc.id)} style={{ cursor: 'pointer' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <strong>{inc.title}</strong>
              <span style={{ marginLeft: 10, fontSize: 13, color: 'var(--text-dim)' }}>{inc.incident_type.replace('_', ' ')}</span>
            </div>
            <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
              <span className={`badge ${severityColor(inc.severity)}`}>{inc.severity}</span>
              <span className={`badge ${inc.status === 'closed' ? 'badge-closed' : 'badge-open'}`}>{inc.status}</span>
            </div>
          </div>
          {expanded === inc.id && (
            <div style={{ marginTop: 12, paddingTop: 12, borderTop: '1px solid var(--border)', fontSize: 14, display: 'flex', flexDirection: 'column', gap: 8 }}>
              <div><strong>Location:</strong> {inc.location}</div>
              <div><strong>Description:</strong> {inc.description}</div>
              {inc.root_cause?.length > 0 && (
                <div><strong>Root Cause:</strong> {inc.root_cause.map((r: any) => r.cause || JSON.stringify(r)).join(', ')}</div>
              )}
              {inc.corrective_actions?.length > 0 && (
                <div><strong>Corrective Actions:</strong> {inc.corrective_actions.map((a: any) => a.action || JSON.stringify(a)).join(', ')}</div>
              )}
              <div style={{ color: 'var(--text-dim)', fontSize: 12 }}>Reported by: {inc.reported_by} | {new Date(inc.created_at).toLocaleDateString()}</div>
            </div>
          )}
        </div>
      ))}
      {incidents.length === 0 && <div style={{ color: 'var(--text-dim)' }}>No incidents reported yet.</div>}
    </div>
  );
}
