import { Routes, Route, Link, useNavigate } from 'react-router-dom';
import { useSafetyStore } from '../store/safetyStore';
import Dashboard from './Dashboard';
import IncidentList from './IncidentList';
import IncidentForm from './IncidentForm';
import PermitForm from './PermitForm';
import AlertFeed from './AlertFeed';

export default function Layout() {
  const { user, logout } = useSafetyStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <nav style={{
        width: 240, background: 'var(--surface)',
        borderRight: '1px solid var(--border)', padding: 20, display: 'flex',
        flexDirection: 'column', gap: 8,
      }}>
        <div style={{ fontSize: 20, fontWeight: 700, color: 'var(--accent)', marginBottom: 20 }}>
          SafetyShield OG
        </div>
        <Link to="/" style={{ padding: '8px 12px', borderRadius: 6, color: 'var(--text)', fontSize: 14 }}>
          Dashboard
        </Link>
        <Link to="/incidents" style={{ padding: '8px 12px', borderRadius: 6, color: 'var(--text)', fontSize: 14 }}>
          Incidents
        </Link>
        <Link to="/incidents/new" style={{ padding: '8px 12px', borderRadius: 6, color: 'var(--text)', fontSize: 14 }}>
          Report Incident
        </Link>
        <Link to="/permits/new" style={{ padding: '8px 12px', borderRadius: 6, color: 'var(--text)', fontSize: 14 }}>
          New Permit
        </Link>
        <Link to="/alerts" style={{ padding: '8px 12px', borderRadius: 6, color: 'var(--text)', fontSize: 14 }}>
          HSE Alerts
        </Link>
        <div style={{ flex: 1 }} />
        <div style={{ color: 'var(--text-dim)', fontSize: 12 }}>{user?.name}</div>
        <button onClick={handleLogout} style={{ background: 'transparent', border: '1px solid var(--border)', color: 'var(--text-dim)', fontSize: 13 }}>
          Logout
        </button>
      </nav>
      <main style={{ flex: 1, padding: 24, overflow: 'auto' }}>
        <Routes>
          <Route index element={<Dashboard />} />
          <Route path="incidents" element={<IncidentList />} />
          <Route path="incidents/new" element={<IncidentForm />} />
          <Route path="permits/new" element={<PermitForm />} />
          <Route path="alerts" element={<AlertFeed />} />
        </Routes>
      </main>
    </div>
  );
}
