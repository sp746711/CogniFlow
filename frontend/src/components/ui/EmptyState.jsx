import React from 'react';
import { Inbox, Plus } from 'lucide-react';

export const EmptyState = ({
  title = 'No Data Found',
  description = 'There is currently no data to display in this workspace.',
  actionLabel,
  onAction,
  icon: Icon = Inbox,
}) => {
  return (
    <div
      className="glass-panel"
      style={{
        padding: '3.5rem 2rem',
        textAlign: 'center',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        maxWidth: '560px',
        margin: '2rem auto',
      }}
    >
      <div
        style={{
          width: '64px',
          height: '64px',
          borderRadius: '50%',
          background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.2) 100%)',
          border: '1px solid rgba(139, 92, 246, 0.3)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: '#a78bfa',
          marginBottom: '1.25rem',
        }}
      >
        <Icon size={30} />
      </div>
      <h3 style={{ fontSize: '1.35rem', fontWeight: 700, marginBottom: '0.5rem', color: '#ffffff' }}>
        {title}
      </h3>
      <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', maxWidth: '400px', marginBottom: '1.5rem' }}>
        {description}
      </p>
      {actionLabel && onAction && (
        <button onClick={onAction} className="btn-glass btn-primary btn-pill">
          <Plus size={16} />
          <span>{actionLabel}</span>
        </button>
      )}
    </div>
  );
};

export default EmptyState;
