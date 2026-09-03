import React, { useEffect, useState } from 'react';
import api from '../services/api';
import GlassCard from '../components/common/GlassCard';
import StatCard from '../components/common/StatCard';
import LoadingSkeleton from '../components/common/LoadingSkeleton';
import ErrorState from '../components/common/ErrorState';
import EmptyState from '../components/common/EmptyState';
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

  if (loading) return <LoadingSkeleton count={3} />;
  if (error) return <ErrorState message={error} onRetry={fetchRecovery} />;
  if (!data) return <EmptyState title="No Recovery Data" message="Run a simulation to analyze recovery time after disruptions." />;

  const developerList = data.developers || [];
  const totalRecoverySeconds = developerList.reduce((acc, dev) => acc + (dev.recovery_time_seconds || 0), 0);
  const totalRecoveryMinutes = Math.round(totalRecoverySeconds / 60);

  const chartData = developerList.slice(0, 10).map((d) => ({
    name: `Dev #${d.developer_id}`,
    recoveryMin: Math.round((d.recovery_time_seconds || 0) / 60),
  }));

  return (
    <div className="fade-in">
      <div className="grid-3" style={{ marginBottom: '1.5rem' }}>
        <StatCard
          label="Developers Processed"
          value={data.developer_count ?? developerList.length}
          subtext="Population evaluated"
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

      <div className="grid-2" style={{ marginBottom: '1.5rem' }}>
        <GlassCard title="Recovery Time Breakdown (Minutes)" icon={Clock}>
          <div style={{ height: '250px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <XAxis dataKey="name" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip
                  contentStyle={{
                    background: 'rgba(255, 255, 255, 0.9)',
                    backdropFilter: 'blur(10px)',
                    borderRadius: '8px',
                    border: '1px solid #e2e8f0',
                  }}
                />
                <Bar dataKey="recoveryMin" fill="#06b6d4" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>

        <GlassCard title="Developer Recovery Time Roster" icon={ShieldAlert}>
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
                      <td style={{ fontWeight: 800, color: 'var(--primary-cyan)' }}>{min} min</td>
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
