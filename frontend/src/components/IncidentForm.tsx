import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useSafetyStore } from '../store/safetyStore';

const INCIDENT_TYPES = [
  'near_miss', 'first_aid', 'medical_treatment', 'lost_time', 'fatality',
  'environmental', 'fire', 'explosion',
];

const SEVERITIES = ['critical', 'high', 'medium', 'low'];

export default function IncidentForm() {
  const navigate = useNavigate();
  const { submitIncident, user } = useSafetyStore();
  const [form, setForm] = useState({
    title: '', incident_type: 'near_miss', severity: 'medium',
    location: '', description: '', root_cause: '',
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e: any) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    await submitIncident({
      ...form,
      root_cause: form.root_cause ? [{ cause: form.root_cause }] : [],
      corrective_actions: [],
      reported_by: user?.name || '',
    });
    setLoading(false);
    navigate('/incidents');
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: 600, display: 'flex', flexDirection: 'column', gap: 16 }}>
      <h2 style={{ fontSize: 20 }}>Report HSE Incident</h2>
      <input name="title" placeholder="Incident Title" value={form.title} onChange={handleChange} required />
      <select name="incident_type" value={form.incident_type} onChange={handleChange}>
        {INCIDENT_TYPES.map((t) => <option key={t} value={t}>{t.replace('_', ' ')}</option>)}
      </select>
      <select name="severity" value={form.severity} onChange={handleChange}>
        {SEVERITIES.map((s) => <option key={s} value={s}>{s}</option>)}
      </select>
      <input name="location" placeholder="Location" value={form.location} onChange={handleChange} required />
      <textarea name="description" placeholder="Description" rows={4} value={form.description} onChange={handleChange} required />
      <textarea name="root_cause" placeholder="Root Cause (text)" rows={2} value={form.root_cause} onChange={handleChange} />
      <button type="submit" disabled={loading}>{loading ? 'Submitting...' : 'Submit Incident'}</button>
    </form>
  );
}
