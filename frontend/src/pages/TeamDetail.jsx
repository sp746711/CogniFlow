import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import GlassCard from '../components/common/GlassCard';
import SkeletonLoader from '../components/ui/SkeletonLoader';
import ErrorState from '../components/ui/ErrorState';
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

  if (loading) return <SkeletonLoader type="cards" count={3} />;
  if (error) return <ErrorState message={error} onRetry={fetchTeam} />;
  if (!team) return <ErrorState title="Team Not Found" message={`Team ID ${id} was not found.`} />;

  return (
    <div className="fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <Link to="/workspace/teams" className="btn-glass btn-secondary btn-sm btn-pill">
          <ArrowLeft size={16} /> Back to Teams
        </Link>
      </div>

      <GlassCard>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <div
              style={{
                width: '56px',
                height: '56px',
                borderRadius: '16px',
                background: 'linear-gradient(135deg, rgba(14, 165, 233, 0.12) 0%, rgba(56, 189, 248, 0.2) 100%)',
                border: '1px solid rgba(14, 165, 233, 0.3)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#0ea5e9',
                boxShadow: 'var(--glow-sky)',
              }}
            >
              <Building2 size={28} />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: '#0f172a' }}>{team.name}</h2>
                <span className="badge badge-sky">{team.code}</span>
              </div>
              <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
                {team.description || 'Simulated engineering team.'}
              </p>
            </div>
          </div>
          <span className="badge badge-info" style={{ padding: '0.55rem 1.1rem', fontSize: '0.85rem' }}>
            <Users size={14} /> {team.developers?.length || 0} Assigned Engineers
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
                      <span className="badge badge-sky">{dev.developer_code}</span>
                    </td>
                    <td style={{ fontWeight: 700, color: '#0f172a' }}>{dev.name}</td>
                    <td>{dev.role || 'Software Engineer'}</td>
                    <td>
                      <Link to={`/workspace/developers/${dev.id}`} className="btn-glass btn-secondary btn-sm" style={{ gap: '0.35rem', borderRadius: '8px' }}>
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


