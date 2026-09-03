import React from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';

export const ErrorState = ({
  title = 'Something Went Wrong',
  message = 'We encountered an error retrieving metrics from the FastAPI backend.',
  onRetry,
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
        maxWidth: '540px',
        margin: '2rem auto',
        borderColor: 'rgba(244, 63, 94, 0.3)',
        background: 'rgba(244, 63, 94, 0.04)',
      }}
    >
      <div
        style={{
          width: '58px',
          height: '58px',
          borderRadius: '50%',
          background: 'rgba(244, 63, 94, 0.15)',
          border: '1px solid rgba(244, 63, 94, 0.4)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: '#f43f5e',
          marginBottom: '1.25rem',
        }}
      >
        <AlertCircle size={28} />
      </div>
      <h3 style={{ fontSize: '1.3rem', fontWeight: 700, marginBottom: '0.5rem', color: '#ffffff' }}>
        {title}
      </h3>
      <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', maxWidth: '420px', marginBottom: '1.5rem' }}>
        {message}
      </p>
      {onRetry && (
        <button onClick={onRetry} className="btn-glass btn-secondary btn-pill">
          <RefreshCw size={16} />
          <span>Retry Request</span>
        </button>
      )}
    </div>
  );
};

export default ErrorState;
