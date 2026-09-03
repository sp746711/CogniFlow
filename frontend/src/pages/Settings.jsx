import React from 'react';
import GlassCard from '../components/common/GlassCard';
import { Settings as SettingsIcon, Sliders, Shield, Database, Clock } from 'lucide-react';

export const Settings = () => {
  return (
    <div className="fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      <div>
        <h1 style={{ fontSize: '2rem', fontWeight: 800, color: '#ffffff' }}>
          Platform <span className="gradient-text">Configuration</span>
        </h1>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
          Active CogniFlow system parameters configured via FastAPI environment and backend models.
        </p>
      </div>

      <div className="grid-2">
        <GlassCard title="Workday Telemetry Bounds" icon={Clock}>
          <div style={{ fontSize: '0.875rem', lineHeight: '2', color: 'var(--text-muted)' }}>
            <div><strong style={{ color: 'var(--text-secondary)' }}>Start Hour:</strong> 10:00 AM (600 mins from midnight)</div>
            <div><strong style={{ color: 'var(--text-secondary)' }}>End Hour:</strong> 6:00 PM (1080 mins from midnight)</div>
            <div><strong style={{ color: 'var(--text-secondary)' }}>Workday Duration:</strong> 8 Hours</div>
            <div><strong style={{ color: 'var(--text-secondary)' }}>Telemetry Interval:</strong> 5 Seconds Live Polling</div>
          </div>
        </GlassCard>

        <GlassCard title="Engineered Population" icon={Sliders}>
          <div style={{ fontSize: '0.875rem', lineHeight: '2', color: 'var(--text-muted)' }}>
            <div><strong style={{ color: 'var(--text-secondary)' }}>Team Count:</strong> 5 Engineered Teams</div>
            <div><strong style={{ color: 'var(--text-secondary)' }}>Developers / Team:</strong> 5 Developers</div>
            <div><strong style={{ color: 'var(--text-secondary)' }}>Total Population:</strong> 25 Active Developers</div>
            <div><strong style={{ color: 'var(--text-secondary)' }}>Deterministic Seed:</strong> 42</div>
          </div>
        </GlassCard>

        <GlassCard title="Database & Analytics Engine" icon={Database}>
          <div style={{ fontSize: '0.875rem', lineHeight: '2', color: 'var(--text-muted)' }}>
            <div><strong style={{ color: 'var(--text-secondary)' }}>Database Engine:</strong> PostgreSQL + SQLAlchemy 2.0</div>
            <div><strong style={{ color: 'var(--text-secondary)' }}>Driver:</strong> psycopg v3</div>
            <div><strong style={{ color: 'var(--text-secondary)' }}>Migrations:</strong> Alembic Managed Schema</div>
          </div>
        </GlassCard>

        <GlassCard title="API Security & Gateway" icon={Shield}>
          <div style={{ fontSize: '0.875rem', lineHeight: '2', color: 'var(--text-muted)' }}>
            <div><strong style={{ color: 'var(--text-secondary)' }}>FastAPI Framework:</strong> v0.115</div>
            <div><strong style={{ color: 'var(--text-secondary)' }}>API Base Prefix:</strong> /api</div>
            <div><strong style={{ color: 'var(--text-secondary)' }}>CORS Origins:</strong> http://127.0.0.1:5173</div>
          </div>
        </GlassCard>
      </div>
    </div>
  );
};

export default Settings;

