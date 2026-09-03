import React, { useEffect, useState } from 'react';
import api from '../services/api';
import GlassCard from '../components/common/GlassCard';
import StatCard from '../components/common/StatCard';
import SkeletonLoader from '../components/ui/SkeletonLoader';
import ErrorState from '../components/ui/ErrorState';
import EmptyState from '../components/ui/EmptyState';
import { BellOff, Users, Activity, AlertTriangle } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export const InterruptionAnalytics = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchInterruptions = async () => {
    setLoading(true);
    try {
      const res = await api.getInterruptionAnalytics();
      setData(res);
      setError(null);
    } catch (err) {
      setError(err.message || 'Failed to fetch interruption analytics.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInterruptions();
  }, []);

  if (loading) return <SkeletonLoader type="cards" count={3} />;
  if (error) return <ErrorState message={error} onRetry={fetchInterruptions} />;
  if (!data) return <EmptyState title="No Interruption Data" description="Run a workday simulation to generate interruption metrics." />;

  const developerList = data.developers || [];
  const totalInterruptions = developerList.reduce((acc, dev) => acc + (dev.interruptions || 0), 0);

  const chartData = developerList.slice(0, 10).map((d) => ({
    name: `Dev #${d.developer_id}`,
    interruptions: d.interruptions,
  }));

  const COLORS = ['#f43f5e', '#f59e0b', '#8b5cf6', '#38bdf8'];

  return (
    <div className="fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      <div>
        <h1 style={{ fontSize: '2rem', fontWeight: 800, color: '#ffffff' }}>
          Interruption <span className="gradient-text">Analytics</span>
        </h1>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
          Slack @mentions, urgent meetings, and unmanaged context disruption telemetry.
        </p>
      </div>

      <div className="grid-3">
        <StatCard
          label="Developers Processed"
          value={data.developer_count ?? developerList.length}
          subtext="Simulated engineer count"
          icon={Users}
        />
        <StatCard
          label="Total Interruptions"
          value={totalInterruptions}
          subtext="Slack & meeting disruptions"
          icon={BellOff}
        />
        <StatCard
          label="Avg Interruptions / Dev"
          value={(totalInterruptions / Math.max(developerList.length, 1)).toFixed(1)}
          subtext="Per simulated workday"
          icon={AlertTriangle}
        />
      </div>

      <div className="grid-2">
        {/* Interruption Distribution Chart */}
        <GlassCard title="Interruption Frequency per Developer" icon={BellOff}>
          <div style={{ height: '250px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <XAxis dataKey="name" stroke="#64748b" fontSize={11} tickLine={false} axisLine={{ stroke: 'rgba(255,255,255,0.1)' }} />
                <YAxis stroke="#64748b" fontSize={11} tickLine={false} axisLine={{ stroke: 'rgba(255,255,255,0.1)' }} />
                <Tooltip
                  contentStyle={{
                    background: 'rgba(18, 20, 32, 0.95)',
                    backdropFilter: 'blur(16px)',
                    borderRadius: '12px',
                    border: '1px solid rgba(255, 255, 255, 0.15)',
                    color: '#ffffff',
                    boxShadow: '0 10px 30px rgba(0,0,0,0.5)',
                  }}
                />
                <Bar dataKey="interruptions" radius={[8, 8, 0, 0]}>
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>

        {/* Breakdown Table */}
        <GlassCard title="Developer Interruption Telemetry" icon={Activity}>
          <div className="glass-table-container">
            <table className="glass-table">
              <thead>
                <tr>
                  <th>Developer ID</th>
                  <th>Events Analyzed</th>
                  <th>Interruptions</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {developerList.slice(0, 8).map((d) => (
                  <tr key={d.developer_id}>
                    <td>
                      <span className="badge badge-indigo">Dev #{d.developer_id}</span>
                    </td>
                    <td>{d.events_analyzed}</td>
                    <td style={{ fontWeight: 800, color: '#f43f5e' }}>{d.interruptions}</td>
                    <td>
                      <span className={`badge ${d.interruptions > 5 ? 'badge-danger' : 'badge-success'}`}>
                        {d.interruptions > 5 ? 'High Disruptions' : 'Healthy Flow'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </GlassCard>
      </div>
    </div>
  );
};

export default InterruptionAnalytics;

