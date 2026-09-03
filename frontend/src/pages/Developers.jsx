import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import GlassCard from '../components/common/GlassCard';
import LoadingSkeleton from '../components/common/LoadingSkeleton';
import ErrorState from '../components/common/ErrorState';
import EmptyState from '../components/common/EmptyState';
import { Users, User, ArrowRight, Shield } from 'lucide-react';

export const Developers = () => {
  const [developers, setDevelopers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');

  const fetchDevelopers = async () => {
    setLoading(true);
    try {
      const data = await api.getDevelopers();
      setDevelopers(data);
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
      dev.name.toLowerCase().includes(search.toLowerCase()) ||
      dev.developer_code.toLowerCase().includes(search.toLowerCase()) ||
      dev.role.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) return <LoadingSkeleton count={6} />;
  if (error) return <ErrorState message={error} onRetry={fetchDevelopers} />;

  return (
    <div className="fade-in">
      {/* Top Search Bar */}
      <GlassCard title="Developers Directory" icon={Users} className="mb-6" style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <input
            type="text"
            placeholder="Search developers by name, code (e.g. DEV_001), or role..."
            className="glass-input"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <div className="badge badge-info" style={{ padding: '0.6rem 1rem', flexShrink: 0 }}>
            {filtered.length} Developers
          </div>
        </div>
      </GlassCard>

      {/* Developer Grid */}
      {filtered.length === 0 ? (
        <EmptyState title="No Developers Found" message="Try searching for another developer name or code." />
      ) : (
        <div className="grid-3">
          {filtered.map((dev) => (
            <GlassCard key={dev.id} interactive className="fade-in">
              <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: '1rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                  <div
                    style={{
                      width: '42px',
                      height: '42px',
                      borderRadius: '50%',
                      background: 'var(--primary-gradient)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: '#ffffff',
                      fontWeight: 700,
                    }}
                  >
                    <User size={20} />
                  </div>
                  <div>
                    <h3 style={{ fontSize: '1.05rem', fontWeight: 700 }}>{dev.name}</h3>
                    <span className="badge badge-indigo" style={{ fontSize: '0.7rem' }}>
                      {dev.developer_code}
                    </span>
                  </div>
                </div>
                {dev.team && (
                  <span className="badge badge-info">{dev.team.name}</span>
                )}
              </div>

              <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '1rem', display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
                <div><strong>Role:</strong> {dev.role}</div>
                <div><strong>Profile:</strong> {dev.behavior_profile}</div>
                {dev.profile_description && (
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-subtle)', fontStyle: 'italic' }}>
                    "{dev.profile_description}"
                  </div>
                )}
              </div>

              <Link
                to={`/developers/${dev.id}`}
                className="btn-glass btn-sm"
                style={{ width: '100%', justifyContent: 'center', gap: '0.4rem' }}
              >
                <span>View Flow Analytics</span>
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
