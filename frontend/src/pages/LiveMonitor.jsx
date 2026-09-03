import React, { useEffect, useState } from 'react';
import { useApp } from '../context/AppContext';
import api from '../services/api';
import GlassCard from '../components/common/GlassCard';
import StatCard from '../components/common/StatCard';
import EventCard from '../components/events/EventCard';
import SkeletonLoader from '../components/ui/SkeletonLoader';
import EmptyState from '../components/ui/EmptyState';
import ErrorState from '../components/ui/ErrorState';
import { Activity, Code, MessageSquare, CheckSquare, GitCommit, RefreshCw, Radio } from 'lucide-react';

export const LiveMonitor = () => {
  const { refreshKey } = useApp();
  const [events, setEvents] = useState([]);
  const [sourceFilter, setSourceFilter] = useState('ALL');
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchEvents = async () => {
    try {
      const params = {};
      if (sourceFilter !== 'ALL') params.source = sourceFilter.toLowerCase();
      const res = await api.getEvents(params);
      setEvents(res || []);
      setError(null);
    } catch (err) {
      setError(err.message || 'Failed to fetch live events stream.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, [sourceFilter, refreshKey]);

  // Polling interval
  useEffect(() => {
    if (!autoRefresh) return;
    const interval = setInterval(fetchEvents, 5000);
    return () => clearInterval(interval);
  }, [autoRefresh, sourceFilter]);

  const sources = [
    { label: 'ALL SOURCES', value: 'ALL', icon: Activity },
    { label: 'IDE WORK', value: 'IDE', icon: Code },
    { label: 'SLACK MSGS', value: 'SLACK', icon: MessageSquare },
    { label: 'JIRA TASKS', value: 'JIRA', icon: CheckSquare },
    { label: 'GITHUB COMMITS', value: 'GITHUB', icon: GitCommit },
  ];

  return (
    <div className="fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: 800, color: '#ffffff' }}>
            Live Telemetry <span className="gradient-text">Monitor</span>
          </h1>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
            Real-time developer activity stream connected to FastAPI engine.
          </p>
        </div>

        <div className="badge badge-success" style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }}>
          <Radio size={14} className="fade-in" style={{ animationDuration: '1s' }} />
          <span>Live Stream Active</span>
        </div>
      </div>

      {/* Top Control Bar & Stats */}
      <div className="grid-3" style={{ gridTemplateColumns: '2fr 1fr 1fr' }}>
        <GlassCard title="Source Stream Filter" icon={Activity}>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
            {sources.map((src) => {
              const Icon = src.icon;
              const active = sourceFilter === src.value;
              return (
                <button
                  key={src.value}
                  onClick={() => setSourceFilter(src.value)}
                  className={`btn-glass btn-sm ${active ? 'btn-primary' : 'btn-secondary'}`}
                  style={{ gap: '0.4rem', borderRadius: '9999px' }}
                >
                  <Icon size={14} />
                  <span>{src.label}</span>
                </button>
              );
            })}
          </div>
        </GlassCard>

        <StatCard
          label="Streamed Events"
          value={events.length}
          subtext="Total captured events"
          icon={Activity}
        />

        <GlassCard title="Stream Controls" icon={RefreshCw}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
            <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Auto Polling (5s)</span>
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
              style={{ width: '18px', height: '18px', cursor: 'pointer', accentColor: '#8b5cf6' }}
            />
          </div>
          <button
            onClick={fetchEvents}
            className="btn-glass btn-secondary btn-sm"
            style={{ width: '100%', gap: '0.4rem', borderRadius: '8px' }}
          >
            <RefreshCw size={14} /> Refresh Stream Now
          </button>
        </GlassCard>
      </div>

      {/* Main Activity Feed */}
      <GlassCard title={`Live Activity Feed (${sourceFilter})`} icon={Activity}>
        {loading ? (
          <SkeletonLoader type="table" count={4} />
        ) : error ? (
          <ErrorState message={error} onRetry={fetchEvents} />
        ) : events.length === 0 ? (
          <EmptyState title="No Events Streamed" description="No matching events found for this filter. Run a workday simulation to populate events." />
        ) : (
          events.map((evt) => <EventCard key={evt.id} event={evt} />)
        )}
      </GlassCard>
    </div>
  );
};

export default LiveMonitor;

