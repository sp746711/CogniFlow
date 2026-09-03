import React from 'react';
import GlassCard from '../components/common/GlassCard';
import { Settings as SettingsIcon, Sliders, Shield, Database, Clock } from 'lucide-react';

export const Settings = () => {
  return (
    <div className="fade-in">
      <GlassCard title="Platform Configuration Settings" icon={SettingsIcon} style={{ marginBottom: '1.5rem' }}>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
          Overview of active CogniFlow system parameters configured via backend environment and configuration models.
        </p>

        <div className="grid-2">
          <GlassCard title="Workday Simulation Bounds" icon={Clock}>
            <div style={{ fontSize: '0.875rem', lineHeight: '1.8' }}>
              <div><strong>Start Hour:</strong> 10:00 AM (600 mins from midnight)</div>
              <div><strong>End Hour:</strong> 6:00 PM (1080 mins from midnight)</div>
              <div><strong>Workday Duration:</strong> 8 Hours</div>
              <div><strong>Timezone:</strong> Asia/Kolkata</div>
            </div>
          </GlassCard>

          <GlassCard title="Engineered Population" icon={Sliders}>
            <div style={{ fontSize: '0.875rem', lineHeight: '1.8' }}>
              <div><strong>Team Count:</strong> 5 Teams</div>
              <div><strong>Developers / Team:</strong> 5 Developers</div>
              <div><strong>Total Population:</strong> 25 Simulated Developers</div>
              <div><strong>Random Seed:</strong> 42</div>
            </div>
          </GlassCard>

          <GlassCard title="Database & Analytics Engine" icon={Database}>
            <div style={{ fontSize: '0.875rem', lineHeight: '1.8' }}>
              <div><strong>Database Engine:</strong> PostgreSQL + SQLAlchemy 2.0</div>
              <div><strong>Driver:</strong> psycopg v3.2</div>
              <div><strong>Migrations:</strong> Alembic Managed</div>
            </div>
          </GlassCard>

          <GlassCard title="API Security & CORS" icon={Shield}>
            <div style={{ fontSize: '0.875rem', lineHeight: '1.8' }}>
              <div><strong>FastAPI Framework:</strong> v0.115</div>
              <div><strong>API Base Prefix:</strong> /api</div>
              <div><strong>Allowed Origins:</strong> http://localhost:5173, http://localhost:3000</div>
            </div>
          </GlassCard>
        </div>
      </GlassCard>
    </div>
  );
};

export default Settings;
