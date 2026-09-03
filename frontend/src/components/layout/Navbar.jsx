import React from 'react';
import { useApp } from '../../context/AppContext';
import { Play, Calendar, Database, CheckCircle2, AlertCircle } from 'lucide-react';

export const Navbar = ({ title = 'Dashboard' }) => {
  const {
    selectedDate,
    setSelectedDate,
    systemHealth,
    setSimulationModalOpen,
    isSimulating,
  } = useApp();

  const isHealthy = systemHealth.status === 'healthy' && systemHealth.database === 'connected';

  return (
    <header
      className="glass-panel"
      style={{
        height: 'var(--navbar-height)',
        borderRadius: 0,
        borderBottom: '1px solid var(--glass-border)',
        padding: '0 2rem',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        position: 'sticky',
        top: 0,
        zIndex: 90,
      }}
    >
      {/* Title / Breadcrumb */}
      <div>
        <h1 style={{ fontSize: '1.35rem', fontWeight: 800 }}>{title}</h1>
        <p style={{ fontSize: '0.775rem', color: 'var(--text-subtle)' }}>
          Developer Workflow Observability & Flow Analytics
        </p>
      </div>

      {/* Header Actions */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        {/* System Health Badge */}
        <div
          className={`badge ${isHealthy ? 'badge-success' : 'badge-danger'}`}
          style={{ padding: '0.4rem 0.75rem', gap: '0.4rem' }}
          title={`Status: ${systemHealth.status}, DB: ${systemHealth.database}`}
        >
          {isHealthy ? <CheckCircle2 size={14} /> : <AlertCircle size={14} />}
          <span>{isHealthy ? 'PostgreSQL Active' : 'DB Disconnected'}</span>
        </div>

        {/* Date Selector */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            background: 'rgba(255, 255, 255, 0.7)',
            padding: '0.4rem 0.75rem',
            borderRadius: 'var(--radius-md)',
            border: '1px solid var(--glass-border-subtle)',
          }}
        >
          <Calendar size={16} color="var(--primary-blue)" />
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            style={{
              border: 'none',
              background: 'transparent',
              fontFamily: 'var(--font-body)',
              fontSize: '0.85rem',
              fontWeight: 600,
              color: 'var(--text-main)',
              outline: 'none',
              cursor: 'pointer',
            }}
          />
        </div>

        {/* Quick Simulation Trigger */}
        <button
          onClick={() => setSimulationModalOpen(true)}
          disabled={isSimulating}
          className="btn-glass btn-primary btn-sm"
          style={{ gap: '0.4rem' }}
        >
          <Play size={14} />
          <span>{isSimulating ? 'Simulating...' : 'Run Workday Simulation'}</span>
        </button>
      </div>
    </header>
  );
};

export default Navbar;
