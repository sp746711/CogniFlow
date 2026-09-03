import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Activity,
  Users,
  Building2,
  Zap,
  BellOff,
  Shuffle,
  Clock,
  Calendar,
  FileText,
  PlayCircle,
  Settings,
  User,
  ShieldCheck,
} from 'lucide-react';

const navigationItems = [
  { label: 'Dashboard', path: '/', icon: LayoutDashboard },
  { label: 'Live Monitor', path: '/live', icon: Activity },
  { label: 'Developers', path: '/developers', icon: Users },
  { label: 'Teams', path: '/teams', icon: Building2 },
  { label: 'Flow Analytics', path: '/flow', icon: Zap },
  { label: 'Interruptions', path: '/interruptions', icon: BellOff },
  { label: 'Context Switching', path: '/context-switching', icon: Shuffle },
  { label: 'Recovery Time', path: '/recovery', icon: Clock },
  { label: 'Timeline', path: '/timeline', icon: Calendar },
  { label: 'Daily Reports', path: '/reports', icon: FileText },
  { label: 'Simulation', path: '/simulation', icon: PlayCircle },
];

const secondaryItems = [
  { label: 'Settings', path: '/settings', icon: Settings },
  { label: 'Profile', path: '/profile', icon: User },
];

export const Sidebar = () => {
  return (
    <aside
      className="glass-panel"
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        bottom: 0,
        width: 'var(--sidebar-width)',
        borderRadius: 0,
        borderRight: '1px solid var(--glass-border)',
        zIndex: 100,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        padding: '1.25rem 1rem',
      }}
    >
      <div>
        {/* App Brand Header */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.75rem',
            padding: '0.5rem 0.75rem',
            marginBottom: '1.5rem',
          }}
        >
          <div
            style={{
              width: '38px',
              height: '38px',
              borderRadius: '10px',
              background: 'var(--primary-gradient)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#ffffff',
              boxShadow: 'var(--glow-cyan)',
            }}
          >
            <Zap size={22} />
          </div>
          <div>
            <h2 style={{ fontSize: '1.25rem', fontFamily: 'var(--font-heading)' }}>CogniFlow</h2>
            <p style={{ fontSize: '0.7rem', color: 'var(--text-subtle)', fontWeight: 600 }}>
              WORKFLOW INTELLIGENCE
            </p>
          </div>
        </div>

        {/* Main Navigation Links */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
          <p
            style={{
              fontSize: '0.7rem',
              fontWeight: 700,
              textTransform: 'uppercase',
              color: 'var(--text-subtle)',
              letterSpacing: '0.05em',
              padding: '0.5rem 0.75rem 0.25rem',
            }}
          >
            Analytics
          </p>
          {navigationItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `btn-glass ${isActive ? 'btn-primary' : ''}`
                }
                style={({ isActive }) => ({
                  justifyContent: 'flex-start',
                  width: '100%',
                  padding: '0.65rem 0.85rem',
                  fontSize: '0.875rem',
                  border: isActive ? 'none' : '1px solid transparent',
                  background: isActive ? undefined : 'transparent',
                  color: isActive ? '#ffffff' : 'var(--text-secondary)',
                })}
              >
                <Icon size={18} />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </div>
      </div>

      {/* Footer Navigation */}
      <div>
        <p
          style={{
            fontSize: '0.7rem',
            fontWeight: 700,
            textTransform: 'uppercase',
            color: 'var(--text-subtle)',
            letterSpacing: '0.05em',
            padding: '0.5rem 0.75rem 0.25rem',
          }}
        >
          System
        </p>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
          {secondaryItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `btn-glass ${isActive ? 'btn-primary' : ''}`
                }
                style={({ isActive }) => ({
                  justifyContent: 'flex-start',
                  width: '100%',
                  padding: '0.65rem 0.85rem',
                  fontSize: '0.875rem',
                  border: isActive ? 'none' : '1px solid transparent',
                  background: isActive ? undefined : 'transparent',
                  color: isActive ? '#ffffff' : 'var(--text-secondary)',
                })}
              >
                <Icon size={18} />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </div>

        {/* Backend Info Badge */}
        <div
          style={{
            marginTop: '1rem',
            padding: '0.75rem',
            borderRadius: 'var(--radius-md)',
            background: 'rgba(224, 242, 254, 0.5)',
            border: '1px solid var(--glass-border-subtle)',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            fontSize: '0.75rem',
          }}
        >
          <ShieldCheck size={16} color="var(--success-color)" />
          <div>
            <div style={{ fontWeight: 600, color: 'var(--text-main)' }}>FastAPI Engine</div>
            <div style={{ color: 'var(--text-subtle)' }}>v1.0.0 Connected</div>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
