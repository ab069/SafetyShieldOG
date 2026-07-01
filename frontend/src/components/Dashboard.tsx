import { useEffect } from 'react';
import { useSafetyStore } from '../store/safetyStore';
import StatsCards from './StatsCards';

export default function Dashboard() {
  const { fetchIncidents, fetchPermits, fetchObservations, fetchStats } = useSafetyStore();

  useEffect(() => {
    fetchIncidents();
    fetchPermits();
    fetchObservations();
    fetchStats();
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <h2 style={{ fontSize: 22 }}>Dashboard</h2>
      <StatsCards />
    </div>
  );
}
