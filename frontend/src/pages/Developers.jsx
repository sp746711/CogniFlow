import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import GlassCard from '../components/common/GlassCard';
import SkeletonLoader from '../components/ui/SkeletonLoader';
import ErrorState from '../components/ui/ErrorState';
import EmptyState from '../components/ui/EmptyState';
import { Users, User, ArrowRight, Search } from 'lucide-react';

export const Developers = () => {
  const [developers, setDevelopers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');

  const fetchDevelopers = async () => {
    setLoading(true);
    try {
      const data = await api.getDevelopers();
      setDevelopers(data || []);
      setError(null);
    } catch (err) {
      setError(err.message || 'Failed to fetch developers.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDevelopers();
  }, []);

  const filtered = developers.filter(
    (dev) =>
      dev.name?.toLowerCase().includes(search.toLowerCase()) ||
      dev.developer_code?.toLowerCase().includes(search.toLowerCase()) ||
      dev.role?.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) return <SkeletonLoader type="cards" count={6} />;
  if (error) return <ErrorState message={error} onRetry={fetchDevelopers} />;

  return (
    <div className="fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* Header & Search */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: 800, color: '#0f172a' }}>
            Developers <span className="gradient-text">Directory</span>
          </h1>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
            Simulated engineering workforce telemetry & individual flow profiles.
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
          <div style={{ width: '320px', position: 'relative' }}>
            <Search size={16} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-subtle)' }} />
            <input
              type="text"
              placeholder="Search by name, code (DEV_001), or role..."
              className="glass-input"
              style={{ paddingLeft: '2.5rem' }}
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
          <div className="badge badge-sky" style={{ padding: '0.55rem 1rem' }}>
            <Users size={14} /> {filtered.length} Engineers
          </div>
        </div>
      </div>

      {/* Developer Grid */}
      {filtered.length === 0 ? (
        <EmptyState title="No Developers Found" description="Try searching for another developer name or code (e.g., DEV_001)." />
      ) : (
        <div className="grid-3">
          {filtered.map((dev) => (
            <GlassCard key={dev.id} interactive className="fade-in">
              <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: '1rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                  <div
                    style={{
                      width: '44px',
                      height: '44px',
                      borderRadius: '50%',
                      background: 'linear-gradient(135deg, rgba(14, 165, 233, 0.15) 0%, rgba(56, 189, 248, 0.25) 100%)',
                      border: '1px solid rgba(14, 165, 233, 0.3)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: '#0ea5e9',
                      boxShadow: 'var(--glow-sky)',
                    }}
                  >
                    <User size={20} />
                  </div>
                  <div>
                    <h3 style={{ fontSize: '1.1rem', fontWeight: 800, color: '#0f172a' }}>{dev.name}</h3>
                    <span className="badge badge-sky" style={{ fontSize: '0.725rem' }}>
                      {dev.developer_code}
                    </span>
                  </div>
                </div>
                {dev.team && (
                  <span className="badge badge-info">{dev.team.name}</span>
                )}
              </div>

              <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '1.25rem', display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                <div><strong style={{ color: 'var(--text-secondary)' }}>Role:</strong> {dev.role}</div>
                <div><strong style={{ color: 'var(--text-secondary)' }}>Behavioral Profile:</strong> {dev.behavior_profile}</div>
                {dev.profile_description && (
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-subtle)', fontStyle: 'italic', marginTop: '0.2rem' }}>
                    "{dev.profile_description}"
                  </div>
                )}
              </div>

              <Link
                to={`/workspace/developers/${dev.id}`}
                className="btn-glass btn-secondary btn-sm"
                style={{ width: '100%', justifyContent: 'center', gap: '0.4rem', borderRadius: '10px' }}
              >
                <span>View Individual Analytics</span>
                <ArrowRight size={14} />
              </Link>
            </GlassCard>
          ))}
        </div>
      )}
    </div>
  );
};

export default Developers;


