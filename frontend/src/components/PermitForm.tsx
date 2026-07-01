import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useSafetyStore } from '../store/safetyStore';

const WORK_TYPES = ['hot_work', 'cold_work', 'confined_space', 'height', 'electrical', 'excavation'];

export default function PermitForm() {
  const navigate = useNavigate();
  const { submitPermit, user } = useSafetyStore();
  const [form, setForm] = useState({
    permit_number: `PTW-${Date.now()}`,
    job_description: '', work_type: 'hot_work', location: '',
    requester: user?.name || '', start_time: '', end_time: '',
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e: any) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    await submitPermit({
      ...form,
      start_time: new Date(form.start_time).toISOString(),
      end_time: new Date(form.end_time).toISOString(),
      risk_assessment: [],
    });
    setLoading(false);
    navigate('/');
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: 600, display: 'flex', flexDirection: 'column', gap: 16 }}>
      <h2 style={{ fontSize: 20 }}>New Permit to Work</h2>
      <input name="permit_number" value={form.permit_number} onChange={handleChange} placeholder="Permit Number" required />
      <textarea name="job_description" placeholder="Job Description" rows={3} value={form.job_description} onChange={handleChange} required />
      <select name="work_type" value={form.work_type} onChange={handleChange}>
        {WORK_TYPES.map((t) => <option key={t} value={t}>{t.replace('_', ' ')}</option>)}
      </select>
      <input name="location" placeholder="Location" value={form.location} onChange={handleChange} required />
      <input name="requester" placeholder="Requester" value={form.requester} onChange={handleChange} required />
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
        <input name="start_time" type="datetime-local" value={form.start_time} onChange={handleChange} required />
        <input name="end_time" type="datetime-local" value={form.end_time} onChange={handleChange} required />
      </div>
      <button type="submit" disabled={loading}>{loading ? 'Submitting...' : 'Submit Permit'}</button>
    </form>
  );
}
