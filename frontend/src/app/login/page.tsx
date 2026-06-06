'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card } from '@/components/ui/Card';
import { setAuthToken, apiJson } from '@/lib/api';
import { useAuth } from '@/contexts/AuthContext';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();
  const { checkAuth } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const res = await apiJson('/auth/login', {
        method: 'POST',
        requireAuth: false,
        body: JSON.stringify({ email, password }),
      });

      if (res && res.access_token) {
        setAuthToken(res.access_token);
        await checkAuth(); // Re-fetch user context
        router.push('/');
      } else {
        setError('Invalid credentials');
      }
    } catch (err: any) {
      setError(err.message || 'Login failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', minHeight: '100vh', alignItems: 'center', justifyContent: 'center', padding: '20px' }} className="animate-fade-in">
      <Card style={{ width: '100%', maxWidth: '400px' }}>
        <div style={{ textAlign: 'center', marginBottom: '30px' }}>
          <h1 style={{ color: 'var(--primary-color)', fontSize: '28px', marginBottom: '8px' }}>FinTrack</h1>
          <p className="text-muted">Enter your credentials to access your dashboard</p>
        </div>

        {error && (
          <div style={{ backgroundColor: 'rgba(239, 68, 68, 0.1)', border: '1px solid var(--danger-color)', padding: '10px', borderRadius: 'var(--radius-sm)', marginBottom: '20px' }}>
            <span className="text-danger" style={{ fontSize: '14px' }}>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <Input 
            label="Email Address" 
            type="email" 
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="admin@example.com"
            required
          />
          
          <Input 
            label="Password" 
            type="password" 
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            required
            style={{ marginBottom: '24px' }}
          />

          <Button type="submit" style={{ width: '100%' }} isLoading={isLoading}>
            Sign In
          </Button>
        </form>
      </Card>
    </div>
  );
}
