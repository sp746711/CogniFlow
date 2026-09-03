import React from 'react';
import GlassCard from '../components/common/GlassCard';
import { User, Shield, Key, Bell } from 'lucide-react';

export const Profile = () => {
  return (
    <div className="fade-in">
      <GlassCard title="User Workspace Profile" icon={User} style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem', marginBottom: '1.5rem' }}>
          <div
            style={{
              width: '64px',
              height: '64px',
              borderRadius: '50%',
              background: 'var(--primary-gradient)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#ffffff',
              boxShadow: 'var(--glow-cyan)',
            }}
          >
            <User size={32} />
          </div>
          <div>
            <h2 style={{ fontSize: '1.35rem', fontWeight: 800 }}>Engineering Workspace Admin</h2>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-subtle)' }}>admin@cogniflow.internal • Lead Platform Architect</p>
            <span className="badge badge-success" style={{ marginTop: '0.35rem' }}>System Administrator</span>
          </div>
        </div>

        <div className="grid-2">
          <GlassCard title="Security & Access Control" icon={Shield}>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
              Full read/write permissions for workflow analytics dashboard, developer performance indexes, daily reporting, and workday simulations.
            </p>
          </GlassCard>

          <GlassCard title="Notification Preferences" icon={Bell}>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
              Alerts enabled for high developer interruption frequency and flow score drops below 40.0 index threshold.
            </p>
          </GlassCard>
        </div>
      </GlassCard>
    </div>
  );
};

export default Profile;
