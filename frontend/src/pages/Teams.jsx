import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import GlassCard from '../components/common/GlassCard';
import SkeletonLoader from '../components/ui/SkeletonLoader';
import ErrorState from '../components/ui/ErrorState';
import EmptyState from '../components/ui/EmptyState';
import { Building2, Users, ArrowRight, User, Search } from 'lucide-react';

export const Teams = () => {
  const [teams, setTeams] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchTeams = async () => {
    setLoading(true);
    try {
      const data = await api.getTeams();
      setTeams(data || []);
      setError(null);
    } catch (err) {
      setError(err.message || 'Failed to fetch teams list from FastAPI.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTeams();
  }, []);

  if (loading) return <SkeletonLoader type="cards" count={4} />;
  if (error) return <ErrorState message={error} onRetry={fetchTeams} />;

  const filteredTeams = teams.filter((t) =>
    t.name?.toLowerCase().includes(search.toLowerCase()) ||
    t.code?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* Header & Search */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: 800, color: '#0f172a' }}>
            Engineered <span className="gradient-text">Teams</span>
          </h1>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
            Real-time developer allocation across engineered software teams.
          </p>
        </div>

        <div style={{ width: '280px', position: 'relative' }}>
          <Search size={16} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-subtle)' }} />
          <input
            type="text"
            className="glass-input"
            style={{ paddingLeft: '2.5rem' }}
            placeholder="Search teams by code..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      {filteredTeams.length === 0 ? (
        <EmptyState title="No Teams Found" description="No engineering teams matched your search criteria." />
      ) : (
        <div className="grid-2">
          {filteredTeams.map((team) => (
            <GlassCard key={team.id} interactive className="fade-in">
              <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: '1rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
                  <div
                    style={{
                      width: '46px',
                      height: '46px',
                      borderRadius: '14px',
                      background: 'linear-gradient(135deg, rgba(14, 165, 233, 0.12) 0%, rgba(56, 189, 248, 0.2) 100%)',
                      border: '1px solid rgba(14, 165, 233, 0.25)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: '#0ea5e9',
                      boxShadow: 'var(--glow-sky)',
                    }}
                  >
                    <Building2 size={24} />
                  </div>
                  <div>
                    <h3 style={{ fontSize: '1.2rem', fontWeight: 800, color: '#0f172a' }}>{team.name}</h3>
                    <span className="badge badge-sky">{team.code}</span>
                  </div>
                </div>
                <div className="badge badge-info">
                  <Users size={12} />
                  <span>{team.developers?.length || 5} Members</span>
                </div>
              </div>

              <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginBottom: '1.25rem', lineHeight: 1.5 }}>
                {team.description || 'Simulated engineering team executing workflow sprints.'}
              </p>

              {/* Developer Roster Pills */}
              {team.developers && team.developers.length > 0 && (
                <div style={{ marginBottom: '1.25rem' }}>
                  <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-subtle)', marginBottom: '0.5rem', textTransform: 'uppercase' }}>
                    Team Roster
                  </div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
                    {team.developers.map((dev) => (
                      <span key={dev.id} className="badge badge-info" style={{ fontSize: '0.75rem', gap: '0.35rem' }}>
                        <User size={12} /> {dev.name}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <Link
                to={`/workspace/teams/${team.id}`}
                className="btn-glass btn-secondary btn-sm"
                style={{ width: '100%', justifyContent: 'center', gap: '0.5rem', borderRadius: '10px' }}
              >
                <span>View Team Performance</span>
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


