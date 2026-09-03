import React from 'react';
import { Link } from 'react-router-dom';
import GlassCard from '../components/common/GlassCard';
import { AlertTriangle, Home } from 'lucide-react';

export const NotFound = () => {
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '60vh',
      }}
    >
      <GlassCard style={{ textAlign: 'center', padding: '3rem 2rem', maxWidth: '460px' }}>
        <AlertTriangle size={56} color="var(--warning-color)" style={{ marginBottom: '1rem' }} />
        <h2 style={{ fontSize: '1.75rem', fontWeight: 800, marginBottom: '0.5rem' }}>404 Page Not Found</h2>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
          The CogniFlow dashboard route you requested does not exist or has been moved.
        </p>
        <Link to="/" className="btn-glass btn-primary" style={{ gap: '0.5rem', display: 'inline-flex' }}>
          <Home size={16} /> Return to Dashboard
        </Link>
      </GlassCard>
    </div>
  );
};

export default NotFound;
