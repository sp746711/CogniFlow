import React from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';

export const ErrorState = ({
  title = 'Failed to Load Data',
  message = 'An unexpected error occurred while communicating with the CogniFlow backend API.',
  onRetry,
}) => {
  return (
    <div
      className="glass-panel"
      style={{
        padding: '2.5rem 2rem',
        textAlign: 'center',
        borderLeft: '4px solid var(--danger-color)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
      }}
    >
      <AlertCircle size={40} color="var(--danger-color)" style={{ marginBottom: '0.75rem' }} />
      <h3 style={{ fontSize: '1.15rem', color: 'var(--text-main)', marginBottom: '0.35rem' }}>{title}</h3>
      <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', maxWidth: '480px', marginBottom: '1.25rem' }}>
        {message}
      </p>
      {onRetry && (
        <button onClick={onRetry} className="btn-glass btn-sm" style={{ gap: '0.4rem' }}>
          <RefreshCw size={14} /> Retry Connection
        </button>
      )}
    </div>
  );
};

export default ErrorState;
