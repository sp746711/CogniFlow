import React, { useEffect, useState } from 'react';
import { useApp } from '../context/AppContext';
import api from '../services/api';
import GlassCard from '../components/common/GlassCard';
import StatCard from '../components/common/StatCard';
import FlowGauge from '../components/common/FlowGauge';
import SkeletonLoader from '../components/ui/SkeletonLoader';
import ErrorState from '../components/ui/ErrorState';
import EmptyState from '../components/ui/EmptyState';
import EventCard from '../components/events/EventCard';
import {
  Users,
  Building2,
  Activity,
  Zap,
  BellOff,
  Shuffle,
  Clock,
  Award,
  PlayCircle,
  Sparkles,
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';

export const Dashboard = () => {
  const { refreshKey, openSimulationModal } = useApp();
  const [data, setData] = useState(null);
  const [teams, setTeams] = useState([]);
  const [recentEvents, setRecentEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchDashboardData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [overview, teamsList, eventsList] = await Promise.all([
        api.getDashboardOverview(),
        api.getTeams().catch(() => []),
        api.getEvents({}).catch(() => []),
      ]);
      setData(overview);
      setTeams(teamsList);
      setRecentEvents(eventsList.slice(0, 5));
    } catch (err) {
      setError(err.message || 'Failed to load dashboard metrics from FastAPI.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, [refreshKey]);

  if (loading) return <SkeletonLoader type="cards" count={4} />;
  if (error) return <ErrorState message={error} onRetry={fetchDashboardData} />;
  if (!data) return <EmptyState title="No Workspace Data" description="Run a workday simulation to generate metrics." actionLabel="Run Simulation" onAction={openSimulationModal} />;

  // Prepare chart data for teams
  const teamChartData = teams.map((t) => ({
    name: t.code,
    developers: t.developers?.length || 5,
  }));

  const COLORS = ['#0ea5e9', '#38bdf8', '#06b6d4', '#6366f1', '#10b981'];

  return (
    <div className="fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* Dashboard Header */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '1rem',
        }}
      >
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: 800, color: '#0f172a' }}>
            Welcome Back 👋 <span className="gradient-text">Workspace Overview</span>
          </h1>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
            Real-time developer telemetry and focus-state telemetry from FastAPI backend.
          </p>
        </div>

        <button
          onClick={openSimulationModal}
          className="btn-glass btn-primary btn-pill"
          style={{ padding: '0.65rem 1.35rem' }}
        >
          <Sparkles size={16} />
          <span>Run Workday Simulation</span>
        </button>
      </div>

      {/* Top KPI Cards Grid */}
      <div className="grid-4">
        <StatCard
          label="Total Developers"
          value={data.developers ?? 25}
          subtext="Across active engineering teams"
          icon={Users}
        />
        <StatCard
          label="Flow Sessions"
          value={data.flow_sessions ?? 0}
          subtext="Deep focus intervals recorded"
          icon={Zap}
        />
        <StatCard
          label="Total Interruptions"
          value={data.interruptions ?? 0}
          subtext="Slack & meeting disruptions"
          icon={BellOff}
        />
        <StatCard
          label="Context Switches"
          value={data.context_switches ?? 0}
          subtext="Tool/context transitions"
          icon={Shuffle}
        />
      </div>

      {/* Main Analytics Row */}
      <div className="grid-3" style={{ gridTemplateColumns: '1.2fr 1.8fr' }}>
        {/* Flow Score Gauge */}
        <GlassCard title="Platform Flow Score" icon={Award}>
          <FlowGauge
            score={data.flow_score ?? 0}
            title="Overall Flow Quality"
            description="Derived from focus duration, recovery speed, and interruption frequency."
          />
          <div
            style={{
              marginTop: '1.25rem',
              paddingTop: '1rem',
              borderTop: '1px solid var(--glass-border-subtle)',
              display: 'flex',
              justifyContent: 'space-around',
              textAlign: 'center',
            }}
          >
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-subtle)', fontWeight: 700, textTransform: 'uppercase' }}>
                Focused Time
              </div>
              <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#0ea5e9', marginTop: '0.2rem' }}>
                {Math.round((data.total_focused_time_seconds || 0) / 60)} min
              </div>
            </div>
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-subtle)', fontWeight: 700, textTransform: 'uppercase' }}>
                Avg Recovery
              </div>
              <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#4f46e5', marginTop: '0.2rem' }}>
                {Math.round((data.recovery_time_seconds || 0) / 60)} min
              </div>
            </div>
          </div>
        </GlassCard>

        {/* Team Distribution Chart */}
        <GlassCard title="Engineered Teams Roster" icon={Building2}>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '1.25rem' }}>
            Developer allocation across Front-end, Back-end, DevOps, Data Engine, and QA Teams.
          </p>
          <div style={{ height: '220px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={teamChartData}>
                <XAxis dataKey="name" stroke="#64748b" fontSize={12} tickLine={false} axisLine={{ stroke: 'rgba(14, 165, 233, 0.15)' }} />
                <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={{ stroke: 'rgba(14, 165, 233, 0.15)' }} />
                <Tooltip
                  contentStyle={{
                    background: '#ffffff',
                    backdropFilter: 'blur(16px)',
                    borderRadius: '12px',
                    border: '1px solid rgba(14, 165, 233, 0.25)',
                    color: '#0f172a',
                    boxShadow: '0 10px 30px rgba(14, 165, 233, 0.15)',
                  }}
                />
                <Bar dataKey="developers" radius={[8, 8, 0, 0]}>
                  {teamChartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>
      </div>

      {/* Recent Activity Ticker */}
      <GlassCard title="Recent Activity Telemetry" icon={Activity}>
        {recentEvents.length === 0 ? (
          <EmptyState
            title="No Activity Events"
            description="No activity recorded yet. Click 'Run Workday Simulation' to populate events."
            actionLabel="Run Simulation"
            onAction={openSimulationModal}
          />
        ) : (
          recentEvents.map((evt) => <EventCard key={evt.id} event={evt} />)
        )}
      </GlassCard>
    </div>
  );
};

export default Dashboard;


