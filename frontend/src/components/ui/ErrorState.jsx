import React from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';

export const ErrorState = ({
  title = 'Something Went Wrong',
  message = 'We encountered an error retrieving metrics from the FastAPI backend.',
  onRetry,
}) => {
  const isOffline = message?.toLowerCase().includes('offline') || message?.toLowerCase().includes('connect');
  const displayTitle = isOffline ? 'Backend Service Offline' : title;

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
        maxWidth: '560px',
        margin: '2rem auto',
        borderColor: isOffline ? 'rgba(245, 158, 11, 0.4)' : 'rgba(244, 63, 94, 0.3)',
        background: isOffline ? 'rgba(245, 158, 11, 0.05)' : 'rgba(244, 63, 94, 0.04)',
      }}
    >
      <div
        style={{
          width: '58px',
          height: '58px',
          borderRadius: '50%',
          background: isOffline ? 'rgba(245, 158, 11, 0.15)' : 'rgba(244, 63, 94, 0.15)',
          border: isOffline ? '1px solid rgba(245, 158, 11, 0.4)' : '1px solid rgba(244, 63, 94, 0.4)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: isOffline ? '#d97706' : '#f43f5e',
          marginBottom: '1.25rem',
        }}
      >
        <AlertCircle size={28} />
      </div>
      <h3 style={{ fontSize: '1.3rem', fontWeight: 700, marginBottom: '0.5rem', color: 'var(--text-main)' }}>
        {displayTitle}
      </h3>
      <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', maxWidth: '460px', marginBottom: '1.25rem' }}>
        {message}
      </p>

      {isOffline && (
        <div
          style={{
            background: 'rgba(15, 23, 42, 0.85)',
            color: '#38bdf8',
            borderRadius: '8px',
            padding: '0.85rem 1.25rem',
            fontFamily: 'monospace',
            fontSize: '0.825rem',
            textAlign: 'left',
            width: '100%',
            maxWidth: '460px',
            marginBottom: '1.5rem',
            boxShadow: 'inset 0 2px 4px rgba(0,0,0,0.3)',
          }}
        >
          <div style={{ color: '#94a3b8', fontSize: '0.75rem', marginBottom: '0.4rem', fontWeight: 600 }}>
            Start Backend Server:
          </div>
          <div><span style={{ color: '#f43f5e' }}>PS&gt;</span> cd backend</div>
          <div><span style={{ color: '#f43f5e' }}>PS&gt;</span> python -m uvicorn app.main:app --port 8000 --reload</div>
          <div style={{ color: '#94a3b8', fontSize: '0.75rem', marginTop: '0.4rem' }}>
            Or run <code style={{ color: '#38bdf8' }}>npm run dev</code> from root folder
          </div>
        </div>
      )}

      {onRetry && (
        <button onClick={onRetry} className="btn-glass btn-primary btn-pill">
          <RefreshCw size={16} />
          <span>Retry Connection</span>
        </button>
      )}
    </div>
  );
};

export default ErrorState;
