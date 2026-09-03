import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import { PlayCircle, X, CheckCircle2, AlertCircle, Loader2, Sparkles } from 'lucide-react';

export const RunSimulationModal = () => {
  const { simulationModalOpen, setSimulationModalOpen, handleRunSimulation, selectedDate } = useApp();
  const [targetDate, setTargetDate] = useState(selectedDate);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  if (!simulationModalOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await handleRunSimulation(targetDate);
      setResult(res);
    } catch (err) {
      setError(err.message || 'Simulation failed to run.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        {/* Modal Header */}
        <div className="glass-header">
          <div className="glass-header-title">
            <PlayCircle size={22} color="#0ea5e9" />
            <span style={{ color: '#0f172a' }}>Run Workday Simulation</span>
          </div>
          <button
            onClick={() => {
              setSimulationModalOpen(false);
              setResult(null);
              setError(null);
            }}
            className="btn-glass btn-sm"
            style={{ padding: '0.35rem', borderRadius: '50%' }}
          >
            <X size={18} />
          </button>
        </div>

        {/* Modal Body */}
        <div className="glass-body">
          <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginBottom: '1.25rem', lineHeight: 1.6 }}>
            Generate simulated telemetry across IDE, Slack, Jira, and GitHub for 25 developers over a 10:00 AM – 6:00 PM workday, and execute the CogniFlow analytics pipeline.
          </p>

          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '1.25rem' }}>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 700, marginBottom: '0.4rem', color: 'var(--text-secondary)' }}>
                Simulation Workday Date
              </label>
              <input
                type="date"
                className="glass-input"
                value={targetDate}
                onChange={(e) => setTargetDate(e.target.value)}
                required
              />
            </div>

            {error && (
              <div
                className="glass-panel"
                style={{
                  padding: '0.75rem 1rem',
                  marginBottom: '1rem',
                  borderLeft: '4px solid var(--danger-color)',
                  fontSize: '0.85rem',
                  color: 'var(--danger-color)',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  background: 'var(--danger-bg)',
                }}
              >
                <AlertCircle size={16} />
                <span>{error}</span>
              </div>
            )}

            {result && (
              <div
                className="glass-panel"
                style={{
                  padding: '1rem',
                  marginBottom: '1rem',
                  background: 'var(--success-bg)',
                  border: '1px solid var(--success-border)',
                  borderRadius: 'var(--radius-md)',
                  fontSize: '0.85rem',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--success-color)', fontWeight: 700, marginBottom: '0.5rem' }}>
                  <CheckCircle2 size={18} />
                  <span>{result.message || 'Simulation Complete!'}</span>
                </div>
                <div className="grid-2" style={{ gap: '0.5rem', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                  <div>Events Generated: <strong>{result.events_generated}</strong></div>
                  <div>Flow Sessions: <strong>{result.analytics?.flow_sessions}</strong></div>
                  <div>Interruptions: <strong>{result.analytics?.interruptions}</strong></div>
                  <div>Context Switches: <strong>{result.analytics?.context_switches}</strong></div>
                </div>
              </div>
            )}

            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '1.5rem' }}>
              <button
                type="button"
                className="btn-glass btn-secondary btn-pill"
                onClick={() => setSimulationModalOpen(false)}
                disabled={loading}
              >
                Close
              </button>
              <button
                type="submit"
                className="btn-glass btn-primary btn-pill"
                disabled={loading}
                style={{ gap: '0.5rem' }}
              >
                {loading ? <Loader2 size={16} style={{ animation: 'spin 1s linear infinite' }} /> : <Sparkles size={16} />}
                <span>{loading ? 'Processing Simulation...' : 'Execute Simulation'}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default RunSimulationModal;

