import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import GlassCard from '../components/common/GlassCard';
import StatCard from '../components/common/StatCard';
import FlowGauge from '../components/common/FlowGauge';
import LoadingSkeleton from '../components/common/LoadingSkeleton';
import ErrorState from '../components/common/ErrorState';
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

  if (loading) return <LoadingSkeleton count={4} />;
  if (error) return <ErrorState message={error} onRetry={fetchData} />;
  if (!developer) return <ErrorState title="Developer Not Found" message={`Developer ID ${id} was not found.`} />;

  return (
    <div className="fade-in">
      {/* Back Button & Header */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem' }}>
        <Link to="/developers" className="btn-glass btn-sm">
          <ArrowLeft size={16} /> Back to Developers
        </Link>
      </div>

      {/* Developer Profile Header Card */}
      <GlassCard className="mb-6" style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
            <div
              style={{
                width: '60px',
                height: '60px',
                borderRadius: '50%',
                background: 'var(--primary-gradient)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#ffffff',
                boxShadow: 'var(--glow-cyan)',
              }}
            >
              <User size={30} />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.2rem' }}>
                <h2 style={{ fontSize: '1.5rem', fontWeight: 800 }}>{developer.name}</h2>
                <span className="badge badge-indigo">{developer.developer_code}</span>
              </div>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                {developer.role} • <strong>Profile:</strong> {developer.behavior_profile}
              </p>
            </div>
          </div>
          {developer.team && <span className="badge badge-info" style={{ fontSize: '0.9rem', padding: '0.5rem 1rem' }}>{developer.team.name}</span>}
        </div>
      </GlassCard>

      {/* Developer Analytics Row */}
      <div className="grid-3" style={{ marginBottom: '1.5rem', gridTemplateColumns: '1fr 2fr' }}>
        {/* Flow Score Gauge */}
        <GlassCard title="Developer Flow Score">
          <FlowGauge
            score={dashboard?.flow_score ?? 0}
            title={`${developer.name}'s Flow`}
            description="Focus vs Interruption performance index"
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
      <GlassCard title={`${developer.name}'s Activity Timeline`} icon={Activity}>
        {events.length === 0 ? (
          <p style={{ fontSize: '0.9rem', color: 'var(--text-subtle)' }}>No events recorded for this developer.</p>
        ) : (
          events.map((evt) => <EventCard key={evt.id} event={evt} />)
        )}
      </GlassCard>
    </div>
  );
};

export default DeveloperDetail;
