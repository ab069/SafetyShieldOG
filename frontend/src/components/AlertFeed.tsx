import { useEffect, useRef, useState } from 'react';

export default function AlertFeed() {
  const [alerts, setAlerts] = useState<any[]>([]);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    ws.current = new WebSocket(`${protocol}//${host}/ws/hse`);

    ws.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setAlerts((prev) => [data, ...prev].slice(0, 50));
      } catch {
        // ignore non-json
      }
    };

    ws.current.onclose = () => {
      setTimeout(() => {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.host;
        ws.current = new WebSocket(`${protocol}//${host}/ws/hse`);
      }, 3000);
    };

    return () => ws.current?.close();
  }, []);

  // Simulated events for demo
  useEffect(() => {
    const interval = setInterval(() => {
      const types = ['incident_reported', 'permit_approved', 'observation_closed', 'safety_alert'];
      const event = {
        type: types[Math.floor(Math.random() * types.length)],
        message: `HSE event at ${new Date().toLocaleTimeString()}`,
        timestamp: new Date().toISOString(),
      };
      setAlerts((prev) => [event, ...prev].slice(0, 50));
    }, 8000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
      <h2 style={{ fontSize: 20 }}>HSE Alert Feed</h2>
      <div style={{ fontSize: 13, color: 'var(--text-dim)', marginBottom: 8 }}>
        Real-time safety events and notifications
      </div>
      {alerts.length === 0 && <div style={{ color: 'var(--text-dim)' }}>No alerts yet. Waiting for events...</div>}
      {alerts.map((a, i) => (
        <div key={i} className="card" style={{ fontSize: 14, borderLeft: '3px solid var(--accent)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <strong style={{ color: 'var(--accent)' }}>{a.type?.replace(/_/g, ' ').toUpperCase()}</strong>
            <span style={{ fontSize: 12, color: 'var(--text-dim)' }}>{new Date(a.timestamp).toLocaleTimeString()}</span>
          </div>
          <div style={{ marginTop: 4 }}>{a.message}</div>
        </div>
      ))}
    </div>
  );
}
