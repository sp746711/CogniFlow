import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import GlassCard from '../components/common/GlassCard';
import LoadingSkeleton from '../components/common/LoadingSkeleton';
import ErrorState from '../components/common/ErrorState';
import EmptyState from '../components/common/EmptyState';
import { Building2, Users, ArrowRight, User } from 'lucide-react';

export const Teams = () => {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchTeams = async () => {
    setLoading(true);
    try {
      const data = await api.getTeams();
      setTeams(data);
      setError(null);
    } catch (err) {
      setError(err.message || 'Failed to fetch teams list.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTeams();
  }, []);

  if (loading) return <LoadingSkeleton count={4} />;
  if (error) return <ErrorState message={error} onRetry={fetchTeams} />;

  return (
    <div className="fade-in">
      <GlassCard title="Engineered Development Teams" icon={Building2} style={{ marginBottom: '1.5rem' }}>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
          CogniFlow models productivity analytics across 5 engineered development teams (5 developers per team).
        </p>
      </GlassCard>

      {teams.length === 0 ? (
        <EmptyState title="No Teams Found" message="No simulated teams found in the database." />
      ) : (
        <div className="grid-2">
          {teams.map((team) => (
            <GlassCard key={team.id} interactive className="fade-in">
              <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: '1rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                  <div
                    style={{
                      width: '44px',
                      height: '44px',
                      borderRadius: '12px',
                      background: 'var(--primary-gradient)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: '#ffffff',
                    }}
                  >
                    <Building2 size={24} />
                  </div>
                  <div>
                    <h3 style={{ fontSize: '1.15rem', fontWeight: 800 }}>{team.name}</h3>
                    <span className="badge badge-info">{team.code}</span>
                  </div>
                </div>
                <div className="badge badge-indigo">
                  {team.developers?.length || 5} Developers
                </div>
              </div>

              <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '1.25rem' }}>
                {team.description || 'Simulated engineering team.'}
              </p>

              {/* Developer Roster Pills */}
              {team.developers && team.developers.length > 0 && (
                <div style={{ marginBottom: '1.25rem' }}>
                  <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-subtle)', marginBottom: '0.5rem', textTransform: 'uppercase' }}>
                    Team Members
                  </div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
                    {team.developers.map((dev) => (
                      <span key={dev.id} className="badge badge-info" style={{ fontSize: '0.75rem', gap: '0.3rem' }}>
                        <User size={12} /> {dev.name}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <Link
                to={`/teams/${team.id}`}
                className="btn-glass btn-sm"
                style={{ width: '100%', justifyContent: 'center', gap: '0.4rem' }}
              >
                <span>View Team Analytics</span>
                <ArrowRight size={14} />
              </Link>
            </GlassCard>
          ))}
        </div>
      )}
    </div>
  );
};

export default Teams;
