import React, { useEffect, useState } from 'react';
import api from '../services/api';
import GlassCard from '../components/common/GlassCard';
import StatCard from '../components/common/StatCard';
import LoadingSkeleton from '../components/common/LoadingSkeleton';
import ErrorState from '../components/common/ErrorState';
import EmptyState from '../components/common/EmptyState';
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

  if (loading) return <LoadingSkeleton count={3} />;
  if (error) return <ErrorState message={error} onRetry={fetchInterruptions} />;
  if (!data) return <EmptyState title="No Interruption Data" message="Run a simulation to generate interruption metrics." />;

  const developerList = data.developers || [];
  const totalInterruptions = developerList.reduce((acc, dev) => acc + (dev.interruptions || 0), 0);

  const chartData = developerList.slice(0, 10).map((d) => ({
    name: `Dev #${d.developer_id}`,
    interruptions: d.interruptions,
  }));

  const COLORS = ['#ef4444', '#f59e0b', '#0284c7', '#6366f1'];

  return (
    <div className="fade-in">
      <div className="grid-3" style={{ marginBottom: '1.5rem' }}>
        <StatCard
          label="Developers Processed"
          value={data.developer_count ?? developerList.length}
          subtext="Developer population"
          icon={Users}
        />
        <StatCard
          label="Total Interruptions"
          value={totalInterruptions}
          subtext="Slack @mentions & unmanaged pings"
          icon={BellOff}
        />
        <StatCard
          label="Avg Interruptions / Dev"
          value={(totalInterruptions / Math.max(developerList.length, 1)).toFixed(1)}
          subtext="Per simulated workday"
          icon={AlertTriangle}
        />
      </div>

      <div className="grid-2" style={{ marginBottom: '1.5rem' }}>
        {/* Interruption Distribution Chart */}
        <GlassCard title="Interruption Frequency per Developer" icon={BellOff}>
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
                <Bar dataKey="interruptions" radius={[6, 6, 0, 0]}>
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>

        {/* Breakdown Table */}
        <GlassCard title="Developer Interruption Roster" icon={Activity}>
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
                    <td style={{ fontWeight: 800, color: 'var(--danger-color)' }}>{d.interruptions}</td>
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
