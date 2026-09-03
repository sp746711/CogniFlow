import React, { useEffect, useState } from 'react';
import { useApp } from '../context/AppContext';
import api from '../services/api';
import GlassCard from '../components/common/GlassCard';
import StatCard from '../components/common/StatCard';
import EventCard from '../components/events/EventCard';
import LoadingSkeleton from '../components/common/LoadingSkeleton';
import EmptyState from '../components/common/EmptyState';
import ErrorState from '../components/common/ErrorState';
import { Activity, Code, MessageSquare, CheckSquare, GitCommit, RefreshCw } from 'lucide-react';

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
      setEvents(res);
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
    <div className="fade-in">
      {/* Top Control Bar & Stats */}
      <div className="grid-3" style={{ marginBottom: '1.5rem', gridTemplateColumns: '2fr 1fr 1fr' }}>
        <GlassCard title="Source Stream Filter" icon={Activity}>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
            {sources.map((src) => {
              const Icon = src.icon;
              const active = sourceFilter === src.value;
              return (
                <button
                  key={src.value}
                  onClick={() => setSourceFilter(src.value)}
                  className={`btn-glass btn-sm ${active ? 'btn-primary' : ''}`}
                  style={{ gap: '0.4rem' }}
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
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>Auto Polling (5s)</span>
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
              style={{ width: '18px', height: '18px', cursor: 'pointer' }}
            />
          </div>
          <button
            onClick={fetchEvents}
            className="btn-glass btn-sm"
            style={{ width: '100%', marginTop: '0.75rem', gap: '0.4rem' }}
          >
            <RefreshCw size={14} /> Refresh Stream Now
          </button>
        </GlassCard>
      </div>

      {/* Main Activity Feed */}
      <GlassCard title={`Live Activity Feed (${sourceFilter})`} icon={Activity}>
        {loading ? (
          <LoadingSkeleton count={4} />
        ) : error ? (
          <ErrorState message={error} onRetry={fetchEvents} />
        ) : events.length === 0 ? (
          <EmptyState title="No Events Streamed" message="No matching events found for this filter." />
        ) : (
          events.map((evt) => <EventCard key={evt.id} event={evt} />)
        )}
      </GlassCard>
    </div>
  );
};

export default LiveMonitor;
