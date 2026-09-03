import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import GlassCard from '../components/common/GlassCard';
import LoadingSkeleton from '../components/common/LoadingSkeleton';
import ErrorState from '../components/common/ErrorState';
import { Building2, ArrowLeft, Users, ArrowRight, User } from 'lucide-react';

export const TeamDetail = () => {
  const { id } = useParams();
  const teamId = parseInt(id, 10);

  const [team, setTeam] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchTeam = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.getTeam(teamId);
      setTeam(res);
    } catch (err) {
      setError(err.message || `Failed to fetch team ${id}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTeam();
  }, [teamId]);

  if (loading) return <LoadingSkeleton count={3} />;
  if (error) return <ErrorState message={error} onRetry={fetchTeam} />;
  if (!team) return <ErrorState title="Team Not Found" message={`Team ID ${id} was not found.`} />;

  return (
    <div className="fade-in">
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem' }}>
        <Link to="/teams" className="btn-glass btn-sm">
          <ArrowLeft size={16} /> Back to Teams
        </Link>
      </div>

      <GlassCard className="mb-6" style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <div
              style={{
                width: '56px',
                height: '56px',
                borderRadius: '14px',
                background: 'var(--primary-gradient)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#ffffff',
                boxShadow: 'var(--glow-cyan)',
              }}
            >
              <Building2 size={28} />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>{team.name}</h2>
                <span className="badge badge-info">{team.code}</span>
              </div>
              <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                {team.description || 'Simulated engineering team.'}
              </p>
            </div>
          </div>
          <span className="badge badge-indigo" style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }}>
            {team.developers?.length || 0} Assigned Developers
          </span>
        </div>
      </GlassCard>

      {/* Developer Members Table */}
      <GlassCard title="Team Members & Roles" icon={Users}>
        {team.developers && team.developers.length > 0 ? (
          <div className="glass-table-container">
            <table className="glass-table">
              <thead>
                <tr>
                  <th>Developer Code</th>
                  <th>Name</th>
                  <th>Role</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {team.developers.map((dev) => (
                  <tr key={dev.id}>
                    <td>
                      <span className="badge badge-indigo">{dev.developer_code}</span>
                    </td>
                    <td style={{ fontWeight: 700, color: 'var(--text-main)' }}>{dev.name}</td>
                    <td>{dev.role || 'Software Engineer'}</td>
                    <td>
                      <Link to={`/developers/${dev.id}`} className="btn-glass btn-sm" style={{ gap: '0.3rem' }}>
                        <span>View Analytics</span>
                        <ArrowRight size={12} />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p style={{ fontSize: '0.9rem', color: 'var(--text-subtle)' }}>No developers assigned to this team.</p>
        )}
      </GlassCard>
    </div>
  );
};

export default TeamDetail;
