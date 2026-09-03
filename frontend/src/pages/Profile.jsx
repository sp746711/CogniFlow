import React from 'react';
import GlassCard from '../components/common/GlassCard';
import { User, Shield, Bell, Key } from 'lucide-react';

export const Profile = () => {
  return (
    <div className="fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      <div>
        <h1 style={{ fontSize: '2rem', fontWeight: 800, color: '#ffffff' }}>
          Workspace <span className="gradient-text">Profile</span>
        </h1>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
          Manage your platform administrative credentials & notifications.
        </p>
      </div>

      <GlassCard>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem', marginBottom: '1.75rem', flexWrap: 'wrap' }}>
          <div
            style={{
              width: '68px',
              height: '68px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(139, 92, 246, 0.4) 100%)',
              border: '1px solid rgba(139, 92, 246, 0.4)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#ffffff',
              boxShadow: 'var(--glow-violet)',
            }}
          >
            <User size={34} />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.2rem' }}>
              <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: '#ffffff' }}>Platform Administrator</h2>
              <span className="badge badge-success">Active Session</span>
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>
              admin@cogniflow.internal • Lead Platform & Telemetry Architect
            </p>
          </div>
        </div>

        <div className="grid-2">
          <GlassCard title="Security & Access Control" icon={Shield}>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', lineHeight: 1.6 }}>
              Full administrative read/write authorization across workflow analytics, developer telemetry, reports generation, and workday simulations.
            </p>
          </GlassCard>

          <GlassCard title="Notification Preferences" icon={Bell}>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', lineHeight: 1.6 }}>
              Automated telemetry alerts configured for high developer interruption frequency and flow score drops below 40.0 threshold.
            </p>
          </GlassCard>
        </div>
      </GlassCard>
    </div>
  );
};

export default Profile;

