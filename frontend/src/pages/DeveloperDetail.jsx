import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import GlassCard from '../components/common/GlassCard';
import StatCard from '../components/common/StatCard';
import FlowGauge from '../components/common/FlowGauge';
import SkeletonLoader from '../components/ui/SkeletonLoader';
import ErrorState from '../components/ui/ErrorState';
import EventCard from '../components/events/EventCard';
import { User, ArrowLeft, Zap, BellOff, Shuffle, Clock, Activity } from 'lucide-react';

export const DeveloperDetail = () => {
  const { id } = useParams();
  const developerId = parseInt(id, 10);

  const [developer, setDeveloper] = useState(null);
  const [dashboard, setDashboard] = useState(null);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [dev, dash, evts] = await Promise.all([
        api.getDeveloper(developerId),
        api.getDeveloperDashboard(developerId).catch(() => null),
        api.getEvents({ developerId }).catch(() => []),
      ]);
      setDeveloper(dev);
      setDashboard(dash);
      setEvents(evts);
    } catch (err) {
      setError(err.message || `Failed to load developer ${id}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [developerId]);

  if (loading) return <SkeletonLoader type="cards" count={4} />;
  if (error) return <ErrorState message={error} onRetry={fetchData} />;
  if (!developer) return <ErrorState title="Developer Not Found" message={`Developer ID ${id} was not found.`} />;

  return (
    <div className="fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* Back Button & Header */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <Link to="/workspace/developers" className="btn-glass btn-secondary btn-sm btn-pill">
          <ArrowLeft size={16} /> Back to Developers
        </Link>
      </div>

      {/* Developer Profile Header Card */}
      <GlassCard>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
            <div
              style={{
                width: '64px',
                height: '64px',
                borderRadius: '50%',
                background: 'linear-gradient(135deg, rgba(14, 165, 233, 0.15) 0%, rgba(56, 189, 248, 0.25) 100%)',
                border: '1px solid rgba(14, 165, 233, 0.3)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#0ea5e9',
                boxShadow: 'var(--glow-sky)',
              }}
            >
              <User size={32} />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.2rem' }}>
                <h2 style={{ fontSize: '1.6rem', fontWeight: 800, color: '#0f172a' }}>{developer.name}</h2>
                <span className="badge badge-sky">{developer.developer_code}</span>
              </div>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                {developer.role} • <strong style={{ color: 'var(--text-secondary)' }}>Behavioral Profile:</strong> {developer.behavior_profile}
              </p>
            </div>
          </div>
          {developer.team && <span className="badge badge-info" style={{ fontSize: '0.85rem', padding: '0.55rem 1.1rem' }}>{developer.team.name}</span>}
        </div>
      </GlassCard>

      {/* Developer Analytics Row */}
      <div className="grid-3" style={{ gridTemplateColumns: '1fr 2fr' }}>
        {/* Flow Score Gauge */}
        <GlassCard title="Individual Flow Score">
          <FlowGauge
            score={dashboard?.flow_score ?? 0}
            title={`${developer.name}'s Index`}
            description="Personal focus vs interruption metric"
          />
        </GlassCard>

        {/* Detailed Stat Grid */}
        <div className="grid-2">
          <StatCard
            label="Flow Sessions"
            value={dashboard?.flow_sessions ?? 0}
            subtext="Deep focus periods"
            icon={Zap}
          />
          <StatCard
            label="Focused Duration"
            value={`${Math.round((dashboard?.focused_time_seconds || 0) / 60)}m`}
            subtext="Total sustained focus"
            icon={Clock}
          />
          <StatCard
            label="Interruptions"
            value={dashboard?.interruptions ?? 0}
            subtext="Disruption events"
            icon={BellOff}
          />
          <StatCard
            label="Context Switches"
            value={dashboard?.context_switches ?? 0}
            subtext="Task transitions"
            icon={Shuffle}
          />
        </div>
      </div>

      {/* Developer Activity Timeline */}
      <GlassCard title={`${developer.name}'s Activity Telemetry`} icon={Activity}>
        {events.length === 0 ? (
          <p style={{ fontSize: '0.9rem', color: 'var(--text-subtle)' }}>No activity events recorded for this developer.</p>
        ) : (
          events.map((evt) => <EventCard key={evt.id} event={evt} />)
        )}
      </GlassCard>
    </div>
  );
};

export default DeveloperDetail;


