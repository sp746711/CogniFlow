import React from 'react';
import { Inbox } from 'lucide-react';

export const EmptyState = ({
  title = 'No Data Available',
  message = 'No activity or metrics found for the selected view.',
  action,
}) => {
  return (
    <div
      className="glass-panel"
      style={{
        padding: '3rem 2rem',
        textAlign: 'center',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <div
        style={{
          width: '64px',
          height: '64px',
          borderRadius: '50%',
          background: 'rgba(2, 132, 199, 0.1)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'var(--primary-blue)',
          marginBottom: '1rem',
        }}
      >
        <Inbox size={32} />
      </div>
      <h3 style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>{title}</h3>
      <p style={{ maxWidth: '420px', fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: action ? '1.5rem' : '0' }}>
        {message}
      </p>
      {action}
    </div>
  );
};

export default EmptyState;
