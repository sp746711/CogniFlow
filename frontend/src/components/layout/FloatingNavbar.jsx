import React, { useState, useRef, useEffect } from 'react';
import { NavLink, useLocation, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Zap,
  LayoutDashboard,
  Activity,
  Users,
  Building2,
  BellOff,
  Calendar,
  PlayCircle,
  Settings,
  User,
  Menu,
  X,
  Sparkles,
  ShieldCheck,
  FileText,
  ChevronDown,
  Layers,
  Shuffle,
  Clock,
  Home,
} from 'lucide-react';
import { useApp } from '../../context/AppContext';

// Primary Horizontal Tabs (Keep navbar compact & clean)
const primaryNavItems = [
  { label: 'Overview', path: '/workspace', icon: LayoutDashboard },
  { label: 'Live Stream', path: '/workspace/live', icon: Activity },
  { label: 'Teams', path: '/workspace/teams', icon: Building2 },
  { label: 'Developers', path: '/workspace/developers', icon: Users },
  { label: 'Timeline', path: '/workspace/timeline', icon: Calendar },
];

// Deep Sub-Analytics Sub-Menu ("More ▾")
const moreNavItems = [
  { label: 'Flow Analytics', path: '/workspace/flow', icon: Zap, subtext: 'Deep focus index & velocity' },
  { label: 'Interruption Audit', path: '/workspace/interruptions', icon: BellOff, subtext: 'Slack & meeting disruptions' },
  { label: 'Context Switching', path: '/workspace/context-switching', icon: Shuffle, subtext: 'Tool transition telemetry' },
  { label: 'Recovery Latency', path: '/workspace/recovery', icon: Clock, subtext: 'Focus restoration speed' },
  { label: 'Productivity Reports', path: '/workspace/reports', icon: FileText, subtext: 'Daily executive snapshots' },
  { label: 'Simulation Engine', path: '/workspace/simulation', icon: PlayCircle, subtext: 'Neural workday generator' },
];

export const FloatingNavbar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { openSimulationModal } = useApp();

  const [moreDropdownOpen, setMoreDropdownOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const dropdownRef = useRef(null);

  // Close dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setMoreDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Check if current route belongs to "More" dropdown
  const isMoreActive = moreNavItems.some((item) => location.pathname === item.path);

  return (
    <header
      style={{
        position: 'fixed',
        top: '12px',
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
          maxWidth: '1380px',
          height: '62px',
          borderRadius: '9999px',
          background: 'rgba(255, 255, 255, 0.88)',
          backdropFilter: 'blur(20px)',
          WebkitBackdropFilter: 'blur(20px)',
          border: '1px solid rgba(255, 255, 255, 0.95)',
          boxShadow: '0 12px 36px -4px rgba(14, 165, 233, 0.15)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0 0.85rem 0 1.25rem',
        }}
      >
        {/* LEFT GROUP: Brand & Home Return */}
        <div
          onClick={() => navigate('/')}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.65rem',
            cursor: 'pointer',
            userSelect: 'none',
          }}
          title="Return to Landing Page"
        >
          <div
            style={{
              width: '34px',
              height: '34px',
              borderRadius: '10px',
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
                fontSize: '1.1rem',
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
              padding: '0.2rem 0.55rem',
              borderRadius: '9999px',
              background: 'rgba(16, 185, 129, 0.1)',
              border: '1px solid rgba(16, 185, 129, 0.25)',
              fontSize: '0.7rem',
              fontWeight: 600,
              color: '#10b981',
              marginLeft: '0.5rem',
            }}
          >
            <ShieldCheck size={12} />
            <span>FastAPI Live</span>
          </div>
        </div>

        {/* CENTER GROUP: Primary Horizontal Pill Navigation */}
        <nav
          className="desktop-nav"
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.2rem',
            background: 'rgba(239, 248, 255, 0.7)',
            padding: '4px',
            borderRadius: '9999px',
            border: '1px solid rgba(14, 165, 233, 0.12)',
            position: 'relative',
          }}
        >
          {primaryNavItems.map((item) => {
            const isActive =
              item.path === '/workspace'
                ? location.pathname === '/workspace'
                : location.pathname.startsWith(item.path);
            const Icon = item.icon;

            return (
              <NavLink
                key={item.path}
                to={item.path}
                style={{
                  position: 'relative',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.45rem',
                  padding: '0.45rem 0.85rem',
                  fontSize: '0.825rem',
                  fontWeight: 600,
                  color: isActive ? '#0ea5e9' : 'var(--text-muted)',
                  borderRadius: '9999px',
                  transition: 'color 0.2s ease',
                  textDecoration: 'none',
                  whiteSpace: 'nowrap',
                }}
              >
                {isActive && (
                  <motion.div
                    layoutId="activePillLight"
                    transition={{ type: 'spring', stiffness: 380, damping: 30 }}
                    style={{
                      position: 'absolute',
                      inset: 0,
                      borderRadius: '9999px',
                      background: '#ffffff',
                      border: '1px solid rgba(14, 165, 233, 0.3)',
                      boxShadow: '0 4px 14px rgba(14, 165, 233, 0.15)',
                      zIndex: 0,
                    }}
                  />
                )}
                <Icon size={15} style={{ position: 'relative', zIndex: 1, color: isActive ? '#0ea5e9' : 'currentColor' }} />
                <span style={{ position: 'relative', zIndex: 1 }}>{item.label}</span>
              </NavLink>
            );
          })}

          {/* "More ▾" Glass Dropdown Trigger */}
          <div ref={dropdownRef} style={{ position: 'relative' }}>
            <button
              onClick={() => setMoreDropdownOpen(!moreDropdownOpen)}
              style={{
                position: 'relative',
                display: 'flex',
                alignItems: 'center',
                gap: '0.35rem',
                padding: '0.45rem 0.85rem',
                fontSize: '0.825rem',
                fontWeight: 600,
                color: isMoreActive || moreDropdownOpen ? '#0ea5e9' : 'var(--text-muted)',
                borderRadius: '9999px',
                border: 'none',
                background: 'transparent',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
              }}
            >
              {isMoreActive && (
                <motion.div
                  layoutId="activePillLight"
                  transition={{ type: 'spring', stiffness: 380, damping: 30 }}
                  style={{
                    position: 'absolute',
                    inset: 0,
                    borderRadius: '9999px',
                    background: '#ffffff',
                    border: '1px solid rgba(14, 165, 233, 0.3)',
                    boxShadow: '0 4px 14px rgba(14, 165, 233, 0.15)',
                    zIndex: 0,
                  }}
                />
              )}
              <Layers size={15} style={{ position: 'relative', zIndex: 1, color: isMoreActive ? '#0ea5e9' : 'currentColor' }} />
              <span style={{ position: 'relative', zIndex: 1 }}>Analytics</span>
              <ChevronDown
                size={14}
                style={{
                  position: 'relative',
                  zIndex: 1,
                  transform: moreDropdownOpen ? 'rotate(180deg)' : 'rotate(0deg)',
                  transition: 'transform 0.2s ease',
                }}
              />
            </button>

            {/* Framer Motion Glass Dropdown Menu */}
            <AnimatePresence>
              {moreDropdownOpen && (
                <motion.div
                  initial={{ opacity: 0, y: 10, scale: 0.95 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: 10, scale: 0.95 }}
                  transition={{ duration: 0.15, ease: 'easeOut' }}
                  style={{
                    position: 'absolute',
                    top: 'calc(100% + 12px)',
                    right: 0,
                    width: '260px',
                    background: 'rgba(255, 255, 255, 0.96)',
                    backdropFilter: 'blur(24px)',
                    WebkitBackdropFilter: 'blur(24px)',
                    border: '1px solid rgba(14, 165, 233, 0.2)',
                    borderRadius: '18px',
                    padding: '0.6rem',
                    boxShadow: '0 20px 45px -8px rgba(14, 165, 233, 0.25)',
                    zIndex: 200,
                  }}
                >
                  <div style={{ fontSize: '0.725rem', fontWeight: 700, color: 'var(--text-subtle)', padding: '0.4rem 0.6rem 0.25rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                    Deep Telemetry Engines
                  </div>

                  {moreNavItems.map((subItem) => {
                    const isSubActive = location.pathname === subItem.path;
                    const SubIcon = subItem.icon;

                    return (
                      <NavLink
                        key={subItem.path}
                        to={subItem.path}
                        onClick={() => setMoreDropdownOpen(false)}
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '0.65rem',
                          padding: '0.6rem 0.75rem',
                          borderRadius: '12px',
                          textDecoration: 'none',
                          color: isSubActive ? '#0ea5e9' : 'var(--text-main)',
                          background: isSubActive ? 'rgba(240, 249, 255, 0.9)' : 'transparent',
                          transition: 'all 0.15s ease',
                          marginBottom: '2px',
                        }}
                      >
                        <div
                          style={{
                            width: '32px',
                            height: '32px',
                            borderRadius: '8px',
                            background: isSubActive ? 'rgba(14, 165, 233, 0.15)' : 'rgba(248, 250, 252, 0.8)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            color: isSubActive ? '#0ea5e9' : 'var(--text-muted)',
                            flexShrink: 0,
                          }}
                        >
                          <SubIcon size={16} />
                        </div>
                        <div>
                          <div style={{ fontSize: '0.85rem', fontWeight: 700, lineHeight: 1.2 }}>{subItem.label}</div>
                          <div style={{ fontSize: '0.725rem', color: 'var(--text-subtle)', marginTop: '0.1rem' }}>{subItem.subtext}</div>
                        </div>
                      </NavLink>
                    );
                  })}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </nav>

        {/* RIGHT GROUP: Utility Controls & User Avatar */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
          <button
            onClick={openSimulationModal}
            className="btn-glass btn-primary btn-sm btn-pill"
            style={{
              padding: '0.45rem 0.95rem',
              fontSize: '0.8rem',
            }}
          >
            <Sparkles size={14} />
            <span className="desktop-only">Simulate Workday</span>
          </button>

          <NavLink
            to="/workspace/settings"
            className="btn-glass btn-sm"
            style={{
              padding: '0.45rem',
              borderRadius: '50%',
              width: '34px',
              height: '34px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: location.pathname === '/workspace/settings' ? '#0ea5e9' : 'var(--text-muted)',
            }}
            title="Settings"
          >
            <Settings size={16} />
          </NavLink>

          <NavLink
            to="/workspace/profile"
            className="btn-glass btn-sm"
            style={{
              padding: '0.45rem',
              borderRadius: '50%',
              width: '34px',
              height: '34px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: location.pathname === '/workspace/profile' ? '#0ea5e9' : 'var(--text-muted)',
              background: 'linear-gradient(135deg, rgba(14, 165, 233, 0.12), rgba(56, 189, 248, 0.18))',
            }}
            title="Profile"
          >
            <User size={16} />
          </NavLink>

          {/* Mobile Toggle Button */}
          <button
            className="mobile-toggle"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            style={{
              background: 'transparent',
              border: 'none',
              color: '#0f172a',
              padding: '0.4rem',
              cursor: 'pointer',
            }}
          >
            {mobileMenuOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>
      </div>

      {/* Responsive Mobile Navigation Drawer */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.2 }}
            style={{
              position: 'fixed',
              top: '80px',
              left: '1rem',
              right: '1rem',
              background: 'rgba(255, 255, 255, 0.96)',
              backdropFilter: 'blur(24px)',
              border: '1px solid rgba(14, 165, 233, 0.2)',
              borderRadius: '20px',
              padding: '1.25rem',
              boxShadow: '0 20px 45px rgba(14, 165, 233, 0.2)',
              pointerEvents: 'auto',
              display: 'flex',
              flexDirection: 'column',
              gap: '0.4rem',
              maxHeight: 'calc(100vh - 100px)',
              overflowY: 'auto',
              zIndex: 99,
            }}
          >
            <NavLink
              to="/"
              onClick={() => setMobileMenuOpen(false)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
                padding: '0.75rem 1rem',
                borderRadius: '12px',
                color: 'var(--text-main)',
                background: 'rgba(239, 248, 255, 0.8)',
                textDecoration: 'none',
                fontWeight: 600,
                marginBottom: '0.5rem',
              }}
            >
              <Home size={18} color="#0ea5e9" />
              <span>Return to Landing Page</span>
            </NavLink>

            <div style={{ fontSize: '0.725rem', fontWeight: 700, color: 'var(--text-subtle)', padding: '0.2rem 0.5rem', textTransform: 'uppercase' }}>
              Primary Navigation
            </div>

            {primaryNavItems.map((item) => {
              const isActive = location.pathname === item.path;
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  onClick={() => setMobileMenuOpen(false)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.75rem',
                    padding: '0.65rem 0.85rem',
                    borderRadius: '12px',
                    color: isActive ? '#0ea5e9' : 'var(--text-secondary)',
                    background: isActive ? '#ffffff' : 'transparent',
                    border: isActive ? '1px solid rgba(14, 165, 233, 0.3)' : '1px solid transparent',
                    boxShadow: isActive ? '0 4px 14px rgba(14, 165, 233, 0.1)' : 'none',
                    textDecoration: 'none',
                    fontWeight: 600,
                  }}
                >
                  <Icon size={18} color={isActive ? '#0ea5e9' : 'currentColor'} />
                  <span>{item.label}</span>
                </NavLink>
              );
            })}

            <div style={{ fontSize: '0.725rem', fontWeight: 700, color: 'var(--text-subtle)', padding: '0.6rem 0.5rem 0.2rem', textTransform: 'uppercase' }}>
              Analytics Engines
            </div>

            {moreNavItems.map((item) => {
              const isActive = location.pathname === item.path;
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  onClick={() => setMobileMenuOpen(false)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.75rem',
                    padding: '0.65rem 0.85rem',
                    borderRadius: '12px',
                    color: isActive ? '#0ea5e9' : 'var(--text-secondary)',
                    background: isActive ? '#ffffff' : 'transparent',
                    border: isActive ? '1px solid rgba(14, 165, 233, 0.3)' : '1px solid transparent',
                    textDecoration: 'none',
                    fontWeight: 600,
                  }}
                >
                  <Icon size={18} color={isActive ? '#0ea5e9' : 'currentColor'} />
                  <span>{item.label}</span>
                </NavLink>
              );
            })}
          </motion.div>
        )}
      </AnimatePresence>

      <style>{`
        .desktop-only { display: flex; }
        .desktop-nav { display: flex; }
        .mobile-toggle { display: none; }

        @media (max-width: 1080px) {
          .desktop-only { display: none !important; }
          .desktop-nav { display: none !important; }
          .mobile-toggle { display: block !important; }
        }
      `}</style>
    </header>
  );
};

export default FloatingNavbar;
