import React, { useEffect, useState } from 'react';
import api from '../services/api';
import GlassCard from '../components/common/GlassCard';
import StatCard from '../components/common/StatCard';
import SkeletonLoader from '../components/ui/SkeletonLoader';
import ErrorState from '../components/ui/ErrorState';
import EmptyState from '../components/ui/EmptyState';
import { Clock, Users, Zap, ShieldAlert } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export const RecoveryAnalytics = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchRecovery = async () => {
    setLoading(true);
    try {
      const res = await api.getRecoveryAnalytics();
      setData(res);
      setError(null);
    } catch (err) {
      setError(err.message || 'Failed to fetch recovery analytics.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecovery();
  }, []);

  if (loading) return <SkeletonLoader type="cards" count={3} />;
  if (error) return <ErrorState message={error} onRetry={fetchRecovery} />;
  if (!data) return <EmptyState title="No Recovery Data" description="Run a workday simulation to analyze recovery time after disruptions." />;

  const developerList = data.developers || [];
  const totalRecoverySeconds = developerList.reduce((acc, dev) => acc + (dev.recovery_time_seconds || 0), 0);
  const totalRecoveryMinutes = Math.round(totalRecoverySeconds / 60);

  const chartData = developerList.slice(0, 10).map((d) => ({
    name: `Dev #${d.developer_id}`,
    recoveryMin: Math.round((d.recovery_time_seconds || 0) / 60),
  }));

  return (
    <div className="fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      <div>
        <h1 style={{ fontSize: '2rem', fontWeight: 800, color: '#ffffff' }}>
          Recovery Time <span className="gradient-text">Analytics</span>
        </h1>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
          Mental latency & focus restoration duration measured after interruptions.
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
          label="Total Recovery Time"
          value={`${totalRecoveryMinutes} min`}
          subtext="Cumulative time to regain flow"
          icon={Clock}
        />
        <StatCard
          label="Avg Recovery / Dev"
          value={`${Math.round(totalRecoveryMinutes / Math.max(developerList.length, 1))} min`}
          subtext="Per workday disruption"
          icon={Zap}
        />
      </div>

      <div className="grid-2">
        <GlassCard title="Recovery Time Breakdown (Minutes)" icon={Clock}>
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
                <Bar dataKey="recoveryMin" fill="#06b6d4" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>

        <GlassCard title="Developer Recovery Time Telemetry" icon={ShieldAlert}>
          <div className="glass-table-container">
            <table className="glass-table">
              <thead>
                <tr>
                  <th>Developer ID</th>
                  <th>Events Analyzed</th>
                  <th>Recovery Time</th>
                  <th>Flow Recovery Status</th>
                </tr>
              </thead>
              <tbody>
                {developerList.slice(0, 8).map((d) => {
                  const min = Math.round((d.recovery_time_seconds || 0) / 60);
                  return (
                    <tr key={d.developer_id}>
                      <td>
                        <span className="badge badge-indigo">Dev #{d.developer_id}</span>
                      </td>
                      <td>{d.events_analyzed}</td>
                      <td style={{ fontWeight: 800, color: '#38bdf8' }}>{min} min</td>
                      <td>
                        <span className={`badge ${min > 20 ? 'badge-warning' : 'badge-success'}`}>
                          {min > 20 ? 'Slow Recovery' : 'Fast Resilience'}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </GlassCard>
      </div>
    </div>
  );
};

export default RecoveryAnalytics;

