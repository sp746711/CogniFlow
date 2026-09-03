import React from 'react';

export const Footer = () => {
  return (
    <footer
      style={{
        padding: '1.5rem 2rem',
        borderTop: '1px solid var(--glass-border-subtle)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        fontSize: '0.8rem',
        color: 'var(--text-subtle)',
        marginTop: 'auto',
      }}
    >
      <div>
        <span style={{ fontWeight: 600, color: 'var(--text-main)' }}>CogniFlow</span> — Enterprise Developer Analytics Platform
      </div>
      <div>
        Simulated Workday Analytics Pipeline • FastAPI + PostgreSQL
      </div>
    </footer>
  );
};

export default Footer;
