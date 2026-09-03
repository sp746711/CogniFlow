import React, { useEffect, useState } from 'react';
import api from '../services/api';
import GlassCard from '../components/common/GlassCard';
import StatCard from '../components/common/StatCard';
import LoadingSkeleton from '../components/common/LoadingSkeleton';
import ErrorState from '../components/common/ErrorState';
import EmptyState from '../components/common/EmptyState';
import { Shuffle, Users, Layers, Activity } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export const ContextSwitching = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchContextSwitches = async () => {
    setLoading(true);
    try {
      const res = await api.getContextSwitchAnalytics();
      setData(res);
      setError(null);
    } catch (err) {
      setError(err.message || 'Failed to fetch context-switching analytics.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchContextSwitches();
  }, []);

  if (loading) return <LoadingSkeleton count={3} />;
  if (error) return <ErrorState message={error} onRetry={fetchContextSwitches} />;
  if (!data) return <EmptyState title="No Context Switch Data" message="Run a simulation to detect tool and task transitions." />;

  const developerList = data.developers || [];
  const totalSwitches = developerList.reduce((acc, dev) => acc + (dev.context_switches || 0), 0);

  const chartData = developerList.slice(0, 10).map((d) => ({
    name: `Dev #${d.developer_id}`,
    switches: d.context_switches,
  }));

  return (
    <div className="fade-in">
      <div className="grid-3" style={{ marginBottom: '1.5rem' }}>
        <StatCard
          label="Total Developers"
          value={data.developer_count ?? developerList.length}
          subtext="Monitored developers"
          icon={Users}
        />
        <StatCard
          label="Total Context Switches"
          value={totalSwitches}
          subtext="Transitions between IDE, Slack, Jira, GitHub"
          icon={Shuffle}
        />
        <StatCard
          label="Avg Context Switches / Dev"
          value={(totalSwitches / Math.max(developerList.length, 1)).toFixed(1)}
          subtext="Per simulated workday"
          icon={Layers}
        />
      </div>

      <div className="grid-2" style={{ marginBottom: '1.5rem' }}>
        <GlassCard title="Context-Switch Frequency per Developer" icon={Shuffle}>
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
                <Bar dataKey="switches" fill="#6366f1" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>

        <GlassCard title="Developer Context Switch Roster" icon={Activity}>
          <div className="glass-table-container">
            <table className="glass-table">
              <thead>
                <tr>
                  <th>Developer ID</th>
                  <th>Events Analyzed</th>
                  <th>Context Switches</th>
                  <th>Fragmentation Level</th>
                </tr>
              </thead>
              <tbody>
                {developerList.slice(0, 8).map((d) => (
                  <tr key={d.developer_id}>
                    <td>
                      <span className="badge badge-indigo">Dev #{d.developer_id}</span>
                    </td>
                    <td>{d.events_analyzed}</td>
                    <td style={{ fontWeight: 800, color: 'var(--accent-indigo)' }}>{d.context_switches}</td>
                    <td>
                      <span className={`badge ${d.context_switches > 10 ? 'badge-warning' : 'badge-success'}`}>
                        {d.context_switches > 10 ? 'High Switching' : 'Stable Context'}
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

export default ContextSwitching;
