import React, { useEffect, useState } from 'react';
import api from '../services/api';
import GlassCard from '../components/common/GlassCard';
import EventCard from '../components/events/EventCard';
import LoadingSkeleton from '../components/common/LoadingSkeleton';
import ErrorState from '../components/common/ErrorState';
import EmptyState from '../components/common/EmptyState';
import { Calendar, Filter, Code, MessageSquare, CheckSquare, GitCommit } from 'lucide-react';

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
      setEvents(evts);
      setTasks(tsk);
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
    <div className="fade-in">
      <GlassCard title="Unified Activity Timeline" icon={Calendar} style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
            Chronological log of IDE edits, Slack messages, Jira task updates, and GitHub commits.
          </p>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Filter size={16} color="var(--text-muted)" />
            {['ALL', 'IDE', 'SLACK', 'JIRA', 'GITHUB'].map((src) => (
              <button
                key={src}
                onClick={() => setSelectedSource(src)}
                className={`btn-glass btn-sm ${selectedSource === src ? 'btn-primary' : ''}`}
              >
                {src}
              </button>
            ))}
          </div>
        </div>
      </GlassCard>

      {/* Main Timeline Stream */}
      <GlassCard title={`Timeline Stream (${events.length} Events)`} icon={Calendar}>
        {loading ? (
          <LoadingSkeleton count={4} />
        ) : error ? (
          <ErrorState message={error} onRetry={fetchTimelineData} />
        ) : events.length === 0 ? (
          <EmptyState title="No Timeline Events" message="No matching events found for this filter." />
        ) : (
          events.map((evt) => <EventCard key={evt.id} event={evt} />)
        )}
      </GlassCard>
    </div>
  );
};

export default Timeline;
