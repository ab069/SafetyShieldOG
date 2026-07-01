import { create } from 'zustand';
import axios from 'axios';

const api = axios.create({ baseURL: '/api' });

interface Incident {
  id: string; title: string; incident_type: string; severity: string;
  location: string; description: string; root_cause: any[]; corrective_actions: any[];
  status: string; reported_by: string; created_at: string;
}

interface Permit {
  id: string; permit_number: string; job_description: string; work_type: string;
  location: string; requester: string; risk_assessment: any[]; permit_issuer: string | null;
  start_time: string; end_time: string; status: string;
}

interface Observation {
  id: string; observation_type: string; description: string; location: string;
  category: string; status: string; created_at: string;
}

interface Stats {
  incidents: { total: number; open: number; by_severity: Record<string, number>; by_type: Record<string, number> };
  permits: { total: number; active: number; by_type: Record<string, number> };
  observations: { total: number; open: number; by_category: Record<string, number> };
  safety_score: number;
}

interface SafetyState {
  token: string | null;
  user: { id: string; email: string; name: string } | null;
  incidents: Incident[];
  permits: Permit[];
  observations: Observation[];
  stats: Stats | null;
  alerts: any[];
  setAuth: (token: string, user: any) => void;
  logout: () => void;
  fetchIncidents: () => Promise<void>;
  fetchPermits: () => Promise<void>;
  fetchObservations: () => Promise<void>;
  fetchStats: () => Promise<void>;
  submitIncident: (data: any) => Promise<void>;
  submitPermit: (data: any) => Promise<void>;
  submitObservation: (data: any) => Promise<void>;
}

export const useSafetyStore = create<SafetyState>((set, get) => ({
  token: localStorage.getItem('token'),
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  incidents: [],
  permits: [],
  observations: [],
  stats: null,
  alerts: [],

  setAuth: (token, user) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
    set({ token, user });
  },

  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    set({ token: null, user: null, incidents: [], permits: [], observations: [], stats: null });
  },

  fetchIncidents: async () => {
    const res = await api.get('/incidents/', {
      headers: { Authorization: `Bearer ${get().token}` },
    });
    set({ incidents: res.data });
  },

  fetchPermits: async () => {
    const res = await api.get('/permits/', {
      headers: { Authorization: `Bearer ${get().token}` },
    });
    set({ permits: res.data });
  },

  fetchObservations: async () => {
    const res = await api.get('/observations/', {
      headers: { Authorization: `Bearer ${get().token}` },
    });
    set({ observations: res.data });
  },

  fetchStats: async () => {
    const token = get().token;
    const [incRes, permRes, obsRes] = await Promise.all([
      api.get('/incidents/stats', { headers: { Authorization: `Bearer ${token}` } }),
      api.get('/permits/stats', { headers: { Authorization: `Bearer ${token}` } }),
      api.get('/observations/stats', { headers: { Authorization: `Bearer ${token}` } }),
    ]);
    const inc = incRes.data;
    const perm = permRes.data;
    const obs = obsRes.data;
    let safety_score = 100;
    if (inc.total > 0) {
      const sevWeights: Record<string, number> = { critical: 40, high: 30, medium: 20, low: 10 };
      const totalWeight = Object.entries(inc.by_severity).reduce((sum, [sev, cnt]) => sum + (sevWeights[sev] || 10) * cnt, 0);
      const avgSev = totalWeight / inc.total;
      safety_score = Math.round(100 - avgSev);
      safety_score = Math.max(0, Math.min(100, safety_score));
    }
    set({ stats: { incidents: inc, permits: perm, observations: obs, safety_score } });
  },

  submitIncident: async (data) => {
    await api.post('/incidents/', data, {
      headers: { Authorization: `Bearer ${get().token}` },
    });
    await get().fetchIncidents();
  },

  submitPermit: async (data) => {
    await api.post('/permits/', data, {
      headers: { Authorization: `Bearer ${get().token}` },
    });
    await get().fetchPermits();
  },

  submitObservation: async (data) => {
    await api.post('/observations/', data, {
      headers: { Authorization: `Bearer ${get().token}` },
    });
    await get().fetchObservations();
  },
}));
