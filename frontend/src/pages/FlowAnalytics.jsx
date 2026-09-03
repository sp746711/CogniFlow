import React, { useEffect, useState } from 'react';
import api from '../services/api';
import GlassCard from '../components/common/GlassCard';
import StatCard from '../components/common/StatCard';
import FlowGauge from '../components/common/FlowGauge';
import LoadingSkeleton from '../components/common/LoadingSkeleton';
import ErrorState from '../components/common/ErrorState';
import EmptyState from '../components/common/EmptyState';
import { Zap, Clock, Activity, Award } from 'lucide-react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

export const FlowAnalytics = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchFlow = async () => {
    setLoading(true);
    try {
      const res = await api.getFlowMetrics();
      setData(res);
      setError(null);
    } catch (err) {
      setError(err.message || 'Failed to fetch flow analytics.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFlow();
  }, []);

  if (loading) return <LoadingSkeleton count={4} />;
  if (error) return <ErrorState message={error} onRetry={fetchFlow} />;
  if (!data) return <EmptyState title="No Flow Data" message="Run a simulation to generate flow session metrics." />;

  const chartData = [
    { hour: '10:00 AM', flow: 45 },
    { hour: '11:00 AM', flow: 85 },
    { hour: '12:00 PM', flow: 70 },
    { hour: '01:00 PM', flow: 30 },
    { hour: '02:00 PM', flow: 90 },
    { hour: '03:00 PM', flow: 95 },
    { hour: '04:00 PM', flow: 60 },
    { hour: '05:00 PM', flow: 75 },
  ];

  return (
    <div className="fade-in">
      <div className="grid-4" style={{ marginBottom: '1.5rem' }}>
        <StatCard
          label="Events Analyzed"
          value={data.events_analyzed ?? 0}
          subtext="Total unified events"
          icon={Activity}
        />
        <StatCard
          label="Flow Sessions"
          value={data.flow_sessions ?? 0}
          subtext="Sustained focus windows"
          icon={Zap}
        />
        <StatCard
          label="Total Focus Time"
          value={`${Math.round((data.focused_time_seconds || 0) / 60)} min`}
          subtext="Cumulative deep work"
          icon={Clock}
        />
        <StatCard
          label="Avg Session Length"
          value={`${Math.round((data.average_flow_seconds || 0) / 60)} min`}
          subtext="Per flow session"
          icon={Award}
        />
      </div>

      <div className="grid-3" style={{ gridTemplateColumns: '1fr 2fr', marginBottom: '1.5rem' }}>
        <GlassCard title="Flow Score Index" icon={Award}>
          <FlowGauge
            score={data.flow_score ?? 0}
            title="System Flow Quality"
            description="Evaluated from raw event patterns"
          />
        </GlassCard>

        <GlassCard title="Flow Session Intensity Curve" icon={Zap}>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
            Simulated workday flow intensity (10:00 AM – 6:00 PM). Peak flow typically occurs during afternoon focus blocks.
          </p>
          <div style={{ height: '220px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData}>
                <defs>
                  <linearGradient id="flowGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#0284c7" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#06b6d4" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <XAxis dataKey="hour" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip
                  contentStyle={{
                    background: 'rgba(255, 255, 255, 0.9)',
                    backdropFilter: 'blur(10px)',
                    borderRadius: '8px',
                    border: '1px solid #e2e8f0',
                  }}
                />
                <Area type="monotone" dataKey="flow" stroke="#0284c7" strokeWidth={3} fillOpacity={1} fill="url(#flowGrad)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>
      </div>
    </div>
  );
};

export default FlowAnalytics;
