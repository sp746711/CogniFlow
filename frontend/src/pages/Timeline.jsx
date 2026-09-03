import React, { useEffect, useState } from 'react';
import api from '../services/api';
import GlassCard from '../components/common/GlassCard';
import EventCard from '../components/events/EventCard';
import SkeletonLoader from '../components/ui/SkeletonLoader';
import ErrorState from '../components/ui/ErrorState';
import EmptyState from '../components/ui/EmptyState';
import { Calendar, Filter } from 'lucide-react';

export const Timeline = () => {
  const [events, setEvents] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [selectedSource, setSelectedSource] = useState('ALL');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchTimelineData = async () => {
    setLoading(true);
    try {
      const [evts, tsk] = await Promise.all([
        api.getEvents(selectedSource !== 'ALL' ? { source: selectedSource.toLowerCase() } : {}),
        api.getTasks().catch(() => []),
      ]);
      setEvents(evts || []);
      setTasks(tsk || []);
      setError(null);
    } catch (err) {
      setError(err.message || 'Failed to fetch timeline activity.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTimelineData();
  }, [selectedSource]);

  return (
    <div className="fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* Header & Filter */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: 800, color: '#ffffff' }}>
            Chronological <span className="gradient-text">Timeline</span>
          </h1>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
            Unified stream of IDE code edits, Slack chatter, Jira tickets, and GitHub commits.
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', flexWrap: 'wrap' }}>
          <Filter size={15} style={{ color: 'var(--text-subtle)', marginRight: '0.25rem' }} />
          {['ALL', 'IDE', 'SLACK', 'JIRA', 'GITHUB'].map((src) => (
            <button
              key={src}
              onClick={() => setSelectedSource(src)}
              className={`btn-glass btn-sm ${selectedSource === src ? 'btn-primary' : 'btn-secondary'}`}
              style={{ borderRadius: '9999px', fontSize: '0.775rem', padding: '0.35rem 0.85rem' }}
            >
              {src}
            </button>
          ))}
        </div>
      </div>

      {/* Main Timeline Stream */}
      <GlassCard title={`Timeline Stream (${events.length} Telemetry Events)`} icon={Calendar}>
        {loading ? (
          <SkeletonLoader type="table" count={5} />
        ) : error ? (
          <ErrorState message={error} onRetry={fetchTimelineData} />
        ) : events.length === 0 ? (
          <EmptyState title="No Timeline Events" description="No matching events found for this telemetry filter." />
        ) : (
          events.map((evt) => <EventCard key={evt.id} event={evt} />)
        )}
      </GlassCard>
    </div>
  );
};

export default Timeline;

