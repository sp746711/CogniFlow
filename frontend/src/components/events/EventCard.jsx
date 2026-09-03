import React, { useState } from 'react';
import { Code, MessageSquare, CheckSquare, GitCommit, ChevronDown, ChevronUp, Clock } from 'lucide-react';

const getSourceIcon = (source) => {
  const s = (source || '').toLowerCase();
  if (s === 'ide') return <Code size={16} color="#0284c7" />;
  if (s === 'slack') return <MessageSquare size={16} color="#6366f1" />;
  if (s === 'jira') return <CheckSquare size={16} color="#06b6d4" />;
  if (s === 'github') return <GitCommit size={16} color="#10b981" />;
  return <Code size={16} />;
};

const getSourceBadgeClass = (source) => {
  const s = (source || '').toLowerCase();
  if (s === 'ide') return 'badge-info';
  if (s === 'slack') return 'badge-indigo';
  if (s === 'jira') return 'badge-warning';
  if (s === 'github') return 'badge-success';
  return 'badge-info';
};

export const EventCard = ({ event }) => {
  const [expanded, setExpanded] = useState(false);

  const formattedTime = event.timestamp
    ? new Date(event.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    : '—';

  return (
    <div
      className="glass-panel"
      style={{
        padding: '1rem 1.25rem',
        marginBottom: '0.75rem',
        transition: 'all 0.2s ease',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
          <div
            style={{
              width: '36px',
              height: '36px',
              borderRadius: '8px',
              background: 'rgba(255, 255, 255, 0.9)',
              border: '1px solid var(--glass-border-subtle)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            {getSourceIcon(event.source)}
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.2rem' }}>
              <span className={`badge ${getSourceBadgeClass(event.source)}`}>
                {event.source?.toUpperCase()}
              </span>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-subtle)', fontWeight: 600 }}>
                {event.context}
              </span>
            </div>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-main)' }}>
              {event.title}
            </h4>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
              <Clock size={12} /> {formattedTime}
            </div>
            {event.developer_id && (
              <div style={{ fontSize: '0.75rem', color: 'var(--text-subtle)' }}>
                Dev #{event.developer_id}
              </div>
            )}
          </div>

          {(event.description || event.event_metadata) && (
            <button
              onClick={() => setExpanded(!expanded)}
              className="btn-glass btn-sm"
              style={{ padding: '0.3rem', borderRadius: '50%' }}
            >
              {expanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
            </button>
          )}
        </div>
      </div>

      {expanded && (
        <div
          style={{
            marginTop: '0.85rem',
            paddingTop: '0.85rem',
            borderTop: '1px solid var(--glass-border-subtle)',
            fontSize: '0.85rem',
            color: 'var(--text-secondary)',
          }}
        >
          {event.description && <p style={{ marginBottom: '0.5rem' }}>{event.description}</p>}
          {event.event_metadata && (
            <pre
              style={{
                background: 'rgba(15, 23, 42, 0.05)',
                padding: '0.5rem 0.75rem',
                borderRadius: 'var(--radius-sm)',
                fontSize: '0.75rem',
                fontFamily: 'monospace',
                overflowX: 'auto',
              }}
            >
              {JSON.stringify(event.event_metadata, null, 2)}
            </pre>
          )}
        </div>
      )}
    </div>
  );
};

export default EventCard;
