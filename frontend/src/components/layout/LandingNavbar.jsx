import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Zap, ArrowRight, ShieldCheck, Sparkles } from 'lucide-react';

export const LandingNavbar = () => {
  const navigate = useNavigate();

  return (
    <header
      style={{
        position: 'fixed',
        top: '16px',
        left: 0,
        right: 0,
        zIndex: 100,
        display: 'flex',
        justifyContent: 'center',
        padding: '0 1rem',
        pointerEvents: 'none',
      }}
    >
      <div
        className="glass-panel"
        style={{
          pointerEvents: 'auto',
          width: '100%',
          maxWidth: '1240px',
          height: '64px',
          borderRadius: '9999px',
          background: 'rgba(255, 255, 255, 0.85)',
          backdropFilter: 'blur(20px)',
          WebkitBackdropFilter: 'blur(20px)',
          border: '1px solid rgba(255, 255, 255, 0.9)',
          boxShadow: '0 12px 36px -4px rgba(14, 165, 233, 0.15)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0 0.85rem 0 1.35rem',
        }}
      >
        {/* Brand Logo */}
        <div
          onClick={() => navigate('/')}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.65rem',
            cursor: 'pointer',
            userSelect: 'none',
          }}
        >
          <div
            style={{
              width: '36px',
              height: '36px',
              borderRadius: '11px',
              background: 'var(--primary-gradient)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#ffffff',
              boxShadow: 'var(--glow-sky)',
            }}
          >
            <Zap size={20} />
          </div>
          <div>
            <span
              style={{
                fontSize: '1.25rem',
                fontWeight: 800,
                letterSpacing: '-0.02em',
                fontFamily: 'var(--font-heading)',
                color: '#0f172a',
              }}
            >
              Cogni<span style={{ color: '#0ea5e9' }}>Flow</span>
            </span>
          </div>

          <div
            className="desktop-only"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.35rem',
              padding: '0.2rem 0.6rem',
              borderRadius: '9999px',
              background: 'rgba(14, 165, 233, 0.1)',
              border: '1px solid rgba(14, 165, 233, 0.25)',
              fontSize: '0.725rem',
              fontWeight: 600,
              color: '#0284c7',
              marginLeft: '0.5rem',
            }}
          >
            <ShieldCheck size={13} />
            <span>AI SaaS Platform</span>
          </div>
        </div>

        {/* Center Nav Links */}
        <nav
          className="desktop-nav"
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '1.75rem',
            fontSize: '0.9rem',
            fontWeight: 600,
            color: 'var(--text-secondary)',
          }}
        >
          <a href="#overview" style={{ color: 'inherit', textDecoration: 'none' }}>
            Product
          </a>
          <a href="#capabilities" style={{ color: 'inherit', textDecoration: 'none' }}>
            Capabilities
          </a>
          <a href="#how-it-works" style={{ color: 'inherit', textDecoration: 'none' }}>
            How It Works
          </a>
        </nav>

        {/* Right Enter Workspace CTA */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <button
            onClick={() => navigate('/workspace')}
            className="btn-glass btn-primary btn-pill"
            style={{
              padding: '0.6rem 1.4rem',
              fontSize: '0.9rem',
            }}
          >
            <Sparkles size={16} />
            <span>Enter Workspace</span>
            <ArrowRight size={16} />
          </button>
        </div>
      </div>

      <style>{`
        .desktop-only { display: flex; }
        .desktop-nav { display: flex; }

        @media (max-width: 768px) {
          .desktop-only { display: none !important; }
          .desktop-nav { display: none !important; }
        }
      `}</style>
    </header>
  );
};

export default LandingNavbar;
