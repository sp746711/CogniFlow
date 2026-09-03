import React, { useEffect, useState } from 'react';
import { useApp } from '../context/AppContext';
import api from '../services/api';
import GlassCard from '../components/common/GlassCard';
import StatCard from '../components/common/StatCard';
import FlowGauge from '../components/common/FlowGauge';
import LoadingSkeleton from '../components/common/LoadingSkeleton';
import ErrorState from '../components/common/ErrorState';
import EmptyState from '../components/common/EmptyState';
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
  const { refreshKey, setSimulationModalOpen } = useApp();
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
      setError(err.message || 'Failed to load dashboard metrics.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, [refreshKey]);

  if (loading) return <LoadingSkeleton count={4} />;
  if (error) return <ErrorState message={error} onRetry={fetchDashboardData} />;
  if (!data) return <EmptyState title="No Dashboard Data" message="Run a workday simulation to populate metrics." />;

  // Prepare chart data for teams
  const teamChartData = teams.map((t) => ({
    name: t.code,
    developers: t.developers?.length || 5,
  }));

  const COLORS = ['#0284c7', '#06b6d4', '#6366f1', '#10b981', '#f59e0b'];

  return (
    <div className="fade-in">
      {/* Top Stat Cards Grid */}
      <div className="grid-4" style={{ marginBottom: '1.5rem' }}>
        <StatCard
          label="Total Developers"
          value={data.developers ?? 25}
          subtext="Across 5 active teams"
          icon={Users}
        />
        <StatCard
          label="Flow Sessions"
          value={data.flow_sessions ?? 0}
          subtext="Deep work sessions"
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
          subtext="Tool/task transitions"
          icon={Shuffle}
        />
      </div>

      {/* Main Analytics Row */}
      <div className="grid-3" style={{ marginBottom: '1.5rem', gridTemplateColumns: '1.2fr 1.8fr' }}>
        {/* Flow Score Gauge */}
        <GlassCard title="Platform Flow Score" icon={Award}>
          <FlowGauge
            score={data.flow_score ?? 0}
            title="Overall Flow Quality"
            description="Derived from focus duration, recovery speed, and interruption count."
          />
          <div
            style={{
              marginTop: '1rem',
              paddingTop: '1rem',
              borderTop: '1px solid var(--glass-border-subtle)',
              display: 'flex',
              justifyContent: 'space-around',
              textAlign: 'center',
            }}
          >
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-subtle)', fontWeight: 600 }}>FOCUSED TIME</div>
              <div style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--primary-blue)' }}>
                {Math.round((data.total_focused_time_seconds || 0) / 60)} min
              </div>
            </div>
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-subtle)', fontWeight: 600 }}>AVG RECOVERY</div>
              <div style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--accent-indigo)' }}>
                {Math.round((data.recovery_time_seconds || 0) / 60)} min
              </div>
            </div>
          </div>
        </GlassCard>

        {/* Team Distribution Chart */}
        <GlassCard
          title="Engineered Teams Roster"
          icon={Building2}
          action={
            <button
              onClick={() => setSimulationModalOpen(true)}
              className="btn-glass btn-primary btn-sm"
              style={{ gap: '0.35rem' }}
            >
              <PlayCircle size={14} /> Run Simulation
            </button>
          }
        >
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
            Simulated population across Front-end, Back-end, DevOps, Data Engine, and QA Teams.
          </p>
          <div style={{ height: '200px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={teamChartData}>
                <XAxis dataKey="name" stroke="#64748b" fontSize={12} />
                <YAxis stroke="#64748b" fontSize={12} />
                <Tooltip
                  contentStyle={{
                    background: 'rgba(255, 255, 255, 0.9)',
                    backdropFilter: 'blur(10px)',
                    borderRadius: '8px',
                    border: '1px solid #e2e8f0',
                  }}
                />
                <Bar dataKey="developers" radius={[6, 6, 0, 0]}>
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
      <GlassCard title="Recent Activity Feed" icon={Activity}>
        {recentEvents.length === 0 ? (
          <EmptyState
            title="No Activity Events"
            message="No activity recorded yet. Click 'Run Workday Simulation' to generate events."
          />
        ) : (
          recentEvents.map((evt) => <EventCard key={evt.id} event={evt} />)
        )}
      </GlassCard>
    </div>
  );
};

export default Dashboard;
