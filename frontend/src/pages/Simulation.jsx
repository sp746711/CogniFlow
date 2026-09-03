import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import GlassCard from '../components/common/GlassCard';
import StatCard from '../components/common/StatCard';
import { PlayCircle, CheckCircle2, AlertCircle, Loader2, Users, Building2, Cpu, Database, Sparkles } from 'lucide-react';

export const Simulation = () => {
  const { selectedDate, handleRunSimulation } = useApp();
  const [targetDate, setTargetDate] = useState(selectedDate);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleExecute = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await handleRunSimulation(targetDate);
      setResult(res);
    } catch (err) {
      setError(err.message || 'Simulation execution failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      <div>
        <h1 style={{ fontSize: '2rem', fontWeight: 800, color: '#ffffff' }}>
          Workday <span className="gradient-text">Simulation Engine</span>
        </h1>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
          Simulate 25 developers across 5 engineered teams to generate telemetry into PostgreSQL via FastAPI.
        </p>
      </div>

      <GlassCard title="CogniFlow Neural Pipeline Control" icon={PlayCircle}>
        <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginBottom: '1.5rem', lineHeight: 1.6 }}>
          Executes the simulated workday data generator and CogniFlow analytics pipeline. Simulates developer activities from 10:00 AM to 6:00 PM and calculates flow sessions, interruptions, context switches, recovery times, and flow scores into PostgreSQL.
        </p>

        <div className="grid-4" style={{ marginBottom: '1.75rem' }}>
          <StatCard label="Engineered Teams" value="5" subtext="Front-end, Back-end, DevOps, QA, Data" icon={Building2} />
          <StatCard label="Developers" value="25" subtext="5 developers per team" icon={Users} />
          <StatCard label="Workday Window" value="8 hrs" subtext="10:00 AM – 6:00 PM" icon={Cpu} />
          <StatCard label="Database Storage" value="PostgreSQL" subtext="SQLAlchemy & Alembic" icon={Database} />
        </div>

        <form onSubmit={handleExecute}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 700, marginBottom: '0.4rem', color: 'var(--text-secondary)' }}>
                Simulation Target Workday Date
              </label>
              <input
                type="date"
                className="glass-input"
                style={{ width: 'auto' }}
                value={targetDate}
                onChange={(e) => setTargetDate(e.target.value)}
                required
              />
            </div>

            <div style={{ alignSelf: 'flex-end' }}>
              <button
                type="submit"
                className="btn-glass btn-primary btn-pill"
                disabled={loading}
                style={{ gap: '0.6rem', padding: '0.75rem 1.6rem' }}
              >
                {loading ? <Loader2 size={18} style={{ animation: 'spin 1s linear infinite' }} /> : <Sparkles size={18} />}
                <span>{loading ? 'Executing Neural Simulation...' : 'Run Workday Simulation'}</span>
              </button>
            </div>
          </div>
        </form>
      </GlassCard>

      {/* Error View */}
      {error && (
        <GlassCard style={{ borderColor: 'rgba(244, 63, 94, 0.4)', background: 'rgba(244, 63, 94, 0.05)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem', color: '#f43f5e' }}>
            <AlertCircle size={24} />
            <div>
              <h4 style={{ fontWeight: 700, fontSize: '1rem' }}>Simulation Error</h4>
              <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>{error}</p>
            </div>
          </div>
        </GlassCard>
      )}

      {/* Results View */}
      {result && (
        <GlassCard title="Simulation Telemetry Pipeline Output" icon={CheckCircle2} className="fade-in">
          <div className="badge badge-success" style={{ padding: '0.55rem 1.1rem', fontSize: '0.85rem', marginBottom: '1.5rem' }}>
            {result.message || 'Simulation Pipeline Execution Successful'}
          </div>

          <div className="grid-3" style={{ marginBottom: '1.5rem' }}>
            <StatCard label="Events Generated" value={result.events_generated} subtext="Raw activity records" icon={Cpu} />
            <StatCard label="Events Persisted" value={result.events_persisted} subtext="Stored in PostgreSQL" icon={Database} />
            <StatCard label="Devs Processed" value={result.analytics?.developers_processed} subtext="Derived metrics calculated" icon={Users} />
          </div>

          <div style={{ background: 'rgba(8, 9, 13, 0.75)', border: '1px solid rgba(255, 255, 255, 0.08)', padding: '1.25rem', borderRadius: 'var(--radius-md)', fontSize: '0.875rem' }}>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#ffffff', marginBottom: '0.75rem' }}>
              Telemetry Analytics Breakdown:
            </h4>
            <ul style={{ paddingLeft: '1.25rem', lineHeight: '1.8', color: 'var(--text-muted)' }}>
              <li>Flow Sessions Detected: <strong style={{ color: '#ffffff' }}>{result.analytics?.flow_sessions}</strong></li>
              <li>Interruptions Processed: <strong style={{ color: '#ffffff' }}>{result.analytics?.interruptions}</strong></li>
              <li>Context Switches Tracked: <strong style={{ color: '#ffffff' }}>{result.analytics?.context_switches}</strong></li>
              <li>Total Recovery Time: <strong style={{ color: '#ffffff' }}>{Math.round((result.analytics?.recovery_time_seconds || 0) / 60)} minutes</strong></li>
            </ul>
          </div>
        </GlassCard>
      )}

      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default Simulation;

