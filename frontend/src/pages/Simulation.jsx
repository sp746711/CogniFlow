import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import GlassCard from '../components/common/GlassCard';
import StatCard from '../components/common/StatCard';
import { PlayCircle, CheckCircle2, AlertCircle, Loader2, Users, Building2, Cpu, Database } from 'lucide-react';

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
    <div className="fade-in">
      <GlassCard title="CogniFlow Simulation Engine" icon={PlayCircle} style={{ marginBottom: '1.5rem' }}>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>
          Execute the simulated workday data generator and CogniFlow analytics pipeline. Simulates 25 developers across 5 teams from 10:00 AM to 6:00 PM and derives flow sessions, interruptions, context switches, recovery times, and flow scores into PostgreSQL.
        </p>

        <div className="grid-4" style={{ marginBottom: '1.5rem' }}>
          <StatCard label="Teams" value="5" subtext="Front-end, Back-end, DevOps, QA, Data" icon={Building2} />
          <StatCard label="Developers" value="25" subtext="5 developers per team" icon={Users} />
          <StatCard label="Workday Window" value="8 hrs" subtext="10:00 AM – 6:00 PM" icon={Cpu} />
          <StatCard label="Database" value="PostgreSQL" subtext="SQLAlchemy & psycopg" icon={Database} />
        </div>

        <form onSubmit={handleExecute}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 700, marginBottom: '0.35rem' }}>
                Simulation Target Date
              </label>
              <input
                type="date"
                className="glass-input"
                value={targetDate}
                onChange={(e) => setTargetDate(e.target.value)}
                required
              />
            </div>

            <div style={{ alignSelf: 'flex-end' }}>
              <button
                type="submit"
                className="btn-glass btn-primary"
                disabled={loading}
                style={{ gap: '0.5rem', padding: '0.75rem 1.5rem' }}
              >
                {loading ? <Loader2 size={18} className="spin" /> : <PlayCircle size={18} />}
                <span>{loading ? 'Running Simulation Pipeline...' : 'Run Workday Simulation'}</span>
              </button>
            </div>
          </div>
        </form>
      </GlassCard>

      {/* Error Card */}
      {error && (
        <GlassCard style={{ marginBottom: '1.5rem', borderLeft: '4px solid var(--danger-color)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', color: 'var(--danger-color)' }}>
            <AlertCircle size={22} />
            <div>
              <h4 style={{ fontWeight: 700 }}>Simulation Error</h4>
              <p style={{ fontSize: '0.875rem' }}>{error}</p>
            </div>
          </div>
        </GlassCard>
      )}

      {/* Results Card */}
      {result && (
        <GlassCard title="Simulation Results & Analytics Pipeline Output" icon={CheckCircle2} className="fade-in">
          <div className="badge badge-success" style={{ padding: '0.5rem 1rem', fontSize: '0.85rem', marginBottom: '1.25rem' }}>
            {result.message || 'Simulation Pipeline Execution Successful'}
          </div>

          <div className="grid-3" style={{ marginBottom: '1.25rem' }}>
            <StatCard label="Events Generated" value={result.events_generated} subtext="Raw activity records" icon={Cpu} />
            <StatCard label="Events Persisted" value={result.events_persisted} subtext="Stored in PostgreSQL" icon={Database} />
            <StatCard label="Devs Processed" value={result.analytics?.developers_processed} subtext="Derived metrics calculated" icon={Users} />
          </div>

          <div style={{ background: 'rgba(15, 23, 42, 0.05)', padding: '1rem', borderRadius: 'var(--radius-md)', fontSize: '0.85rem' }}>
            <h4 style={{ fontSize: '0.9rem', fontWeight: 700, marginBottom: '0.5rem' }}>Analytics Summary Breakdown:</h4>
            <ul style={{ paddingLeft: '1.25rem', lineHeight: '1.8' }}>
              <li>Flow Sessions Detected: <strong>{result.analytics?.flow_sessions}</strong></li>
              <li>Interruptions Processed: <strong>{result.analytics?.interruptions}</strong></li>
              <li>Context Switches Tracked: <strong>{result.analytics?.context_switches}</strong></li>
              <li>Total Recovery Time: <strong>{Math.round((result.analytics?.recovery_time_seconds || 0) / 60)} minutes</strong></li>
            </ul>
          </div>
        </GlassCard>
      )}
    </div>
  );
};

export default Simulation;
