import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useSafetyStore } from '../store/safetyStore';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { setAuth } = useSafetyStore();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await axios.post('/api/auth/login', { email, password });
      setAuth(res.data.access_token, res.data.user);
      navigate('/');
    } catch {
      setError('Invalid credentials');
    }
  };

  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh' }}>
      <form onSubmit={handleSubmit} className="card" style={{ width: 380, display: 'flex', flexDirection: 'column', gap: 16 }}>
        <h1 style={{ color: 'var(--accent)', fontSize: 24, textAlign: 'center' }}>SafetyShield OG</h1>
        <h2 style={{ textAlign: 'center', fontSize: 16, color: 'var(--text-dim)' }}>HSE Management Platform</h2>
        {error && <div style={{ color: 'var(--accent)', fontSize: 13 }}>{error}</div>}
        <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <button type="submit">Login</button>
        <div style={{ textAlign: 'center', fontSize: 13, color: 'var(--text-dim)' }}>
          No account? <Link to="/register">Register</Link>
        </div>
      </form>
    </div>
  );
}
