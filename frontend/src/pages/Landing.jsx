import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  Zap,
  ArrowRight,
  Sparkles,
  Activity,
  ShieldCheck,
  Cpu,
  Shuffle,
  Clock,
  Building2,
  Users,
  CheckCircle2,
} from 'lucide-react';

export const Landing = () => {
  const navigate = useNavigate();

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '5.5rem', paddingBottom: '4rem' }}>
      {/* 1. HERO SECTION (NO NAVBAR ABOVE THIS) */}
      <section
        id="overview"
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          textAlign: 'center',
          paddingTop: '3.5rem',
          position: 'relative',
        }}
      >
        {/* Centered Brand Presentation & Version Badge */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.75rem',
            marginBottom: '1.5rem',
          }}
        >
          <div
            style={{
              width: '42px',
              height: '42px',
              borderRadius: '12px',
              background: 'var(--primary-gradient)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#ffffff',
              boxShadow: 'var(--glow-sky)',
            }}
          >
            <Zap size={24} />
          </div>
          <span
            style={{
              fontSize: '1.75rem',
              fontWeight: 800,
              letterSpacing: '-0.03em',
              fontFamily: 'var(--font-heading)',
              color: '#0f172a',
            }}
          >
            Cogni<span style={{ color: '#0ea5e9' }}>Flow</span>
          </span>
        </motion.div>

        {/* Release Pill Badge */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.05 }}
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem',
            padding: '0.4rem 1.25rem',
            borderRadius: '9999px',
            background: 'rgba(14, 165, 233, 0.1)',
            border: '1px solid rgba(14, 165, 233, 0.25)',
            color: '#0284c7',
            fontSize: '0.825rem',
            fontWeight: 700,
            marginBottom: '1.75rem',
            boxShadow: 'var(--shadow-sm)',
          }}
        >
          <Sparkles size={14} color="#0ea5e9" />
          <span>CogniFlow 1.0 — Intelligent Workflow Telemetry</span>
        </motion.div>

        {/* Main Headline */}
        <motion.h1
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          style={{
            fontSize: 'clamp(2.85rem, 5.5vw, 5rem)',
            fontWeight: 800,
            lineHeight: 1.1,
            maxWidth: '940px',
            marginBottom: '1.25rem',
            letterSpacing: '-0.03em',
            color: '#0f172a',
          }}
        >
          Your Team. Your Workflow.{' '}
          <span className="gradient-text">One Intelligent Workspace.</span>
        </motion.h1>

        {/* Supporting Text */}
        <motion.p
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          style={{
            fontSize: 'clamp(1.1rem, 2vw, 1.35rem)',
            color: 'var(--text-muted)',
            maxWidth: '680px',
            marginBottom: '2.5rem',
            lineHeight: 1.6,
          }}
        >
          A modern light workspace designed to eliminate context switching, protect team focus-state, and maximize engineering velocity.
        </motion.p>

        {/* Primary Enter Workspace CTA */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap', justifyContent: 'center' }}
        >
          <button
            onClick={() => navigate('/workspace')}
            className="btn-glass btn-primary btn-lg btn-pill"
            style={{ padding: '1rem 2.6rem', fontSize: '1.08rem' }}
          >
            <span>Enter Workspace</span>
            <ArrowRight size={18} />
          </button>

          <a
            href="#capabilities"
            className="btn-glass btn-secondary btn-lg btn-pill"
            style={{ padding: '1rem 2.1rem', fontSize: '1rem' }}
          >
            <Activity size={18} color="#0ea5e9" />
            <span>Explore Platform</span>
          </a>
        </motion.div>

        {/* Floating Product Preview Representation */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="glass-panel"
          style={{
            width: '100%',
            maxWidth: '1120px',
            marginTop: '3.75rem',
            padding: '1.5rem',
            borderRadius: '24px',
            background: 'rgba(255, 255, 255, 0.92)',
            borderColor: 'rgba(255, 255, 255, 0.95)',
            boxShadow: '0 25px 70px -10px rgba(14, 165, 233, 0.2), 0 10px 30px rgba(0, 0, 0, 0.04)',
          }}
        >
          {/* Preview Window Header */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              paddingBottom: '1rem',
              borderBottom: '1px solid var(--glass-border-subtle)',
              marginBottom: '1.25rem',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#ef4444' }} />
              <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#f59e0b' }} />
              <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#10b981' }} />
              <span style={{ fontSize: '0.8rem', color: 'var(--text-subtle)', marginLeft: '0.5rem', fontWeight: 600 }}>
                cogniflow.ai/workspace/overview
              </span>
            </div>
            <div className="badge badge-sky">
              <ShieldCheck size={13} />
              <span>FastAPI Connected</span>
            </div>
          </div>

          {/* Interactive Metric Preview */}
          <div className="grid-3">
            <div className="glass-panel" style={{ padding: '1.25rem', textAlign: 'left', background: 'rgba(240, 249, 255, 0.7)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', color: '#0ea5e9', marginBottom: '0.5rem' }}>
                <Zap size={18} />
                <span style={{ fontSize: '0.85rem', fontWeight: 700 }}>Realtime Flow Index</span>
              </div>
              <div style={{ fontSize: '2.1rem', fontWeight: 800, color: '#0f172a' }}>88.4 / 100</div>
              <p style={{ fontSize: '0.775rem', color: '#10b981', marginTop: '0.25rem', fontWeight: 600 }}>
                +14.2% higher focus velocity
              </p>
            </div>

            <div className="glass-panel" style={{ padding: '1.25rem', textAlign: 'left', background: 'rgba(240, 249, 255, 0.7)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', color: '#0284c7', marginBottom: '0.5rem' }}>
                <Shuffle size={18} />
                <span style={{ fontSize: '0.85rem', fontWeight: 700 }}>Context Switches</span>
              </div>
              <div style={{ fontSize: '2.1rem', fontWeight: 800, color: '#0f172a' }}>4.2 / hr</div>
              <p style={{ fontSize: '0.775rem', color: '#10b981', marginTop: '0.25rem', fontWeight: 600 }}>
                -62% drop after AI batching
              </p>
            </div>

            <div className="glass-panel" style={{ padding: '1.25rem', textAlign: 'left', background: 'rgba(240, 249, 255, 0.7)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', color: '#06b6d4', marginBottom: '0.5rem' }}>
                <Clock size={18} />
                <span style={{ fontSize: '0.85rem', fontWeight: 700 }}>Recovery Latency</span>
              </div>
              <div style={{ fontSize: '2.1rem', fontWeight: 800, color: '#0f172a' }}>8.4 min</div>
              <p style={{ fontSize: '0.775rem', color: 'var(--text-muted)', marginTop: '0.25rem', fontWeight: 500 }}>
                Optimized focus restoration
              </p>
            </div>
          </div>
        </motion.div>
      </section>

      {/* 2. STATS & PERFORMANCE BAR */}
      <section
        className="glass-panel"
        style={{
          padding: '2.5rem',
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '2rem',
          textAlign: 'center',
          background: '#ffffff',
          boxShadow: 'var(--shadow-md)',
        }}
      >
        <div>
          <div style={{ fontSize: '2.5rem', fontWeight: 800, color: '#0ea5e9', fontFamily: 'var(--font-heading)' }}>
            +42%
          </div>
          <div style={{ fontSize: '0.875rem', color: 'var(--text-muted)', fontWeight: 600, marginTop: '0.2rem' }}>
            Deep Focus Duration
          </div>
        </div>
        <div>
          <div style={{ fontSize: '2.5rem', fontWeight: 800, color: '#0369a1', fontFamily: 'var(--font-heading)' }}>
            -68%
          </div>
          <div style={{ fontSize: '0.875rem', color: 'var(--text-muted)', fontWeight: 600, marginTop: '0.2rem' }}>
            Context Switching Disruptions
          </div>
        </div>
        <div>
          <div style={{ fontSize: '2.5rem', fontWeight: 800, color: '#06b6d4', fontFamily: 'var(--font-heading)' }}>
            12ms
          </div>
          <div style={{ fontSize: '0.875rem', color: 'var(--text-muted)', fontWeight: 600, marginTop: '0.2rem' }}>
            Event Telemetry Sync Rate
          </div>
        </div>
        <div>
          <div style={{ fontSize: '2.5rem', fontWeight: 800, color: '#10b981', fontFamily: 'var(--font-heading)' }}>
            100%
          </div>
          <div style={{ fontSize: '0.875rem', color: 'var(--text-muted)', fontWeight: 600, marginTop: '0.2rem' }}>
            FastAPI Direct Integration
          </div>
        </div>
      </section>

      {/* 3. CAPABILITIES GRID */}
      <section id="capabilities" style={{ textAlign: 'center' }}>
        <div style={{ marginBottom: '3.25rem' }}>
          <span className="badge badge-sky" style={{ marginBottom: '0.75rem' }}>
            ENGINEERED FOR MODERN TEAMS
          </span>
          <h2 style={{ fontSize: '2.5rem', fontWeight: 800, marginBottom: '0.75rem', color: '#0f172a' }}>
            Comprehensive Flow Intelligence
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '1.05rem', maxWidth: '600px', margin: '0 auto' }}>
            Built with modern telemetry algorithms to monitor developer velocity without invasive tracking.
          </p>
        </div>

        <div className="grid-4">
          <div className="glass-panel glass-panel-interactive" style={{ padding: '2.25rem 1.6rem', textAlign: 'left', background: '#ffffff' }}>
            <div className="stat-icon-wrapper" style={{ marginBottom: '1.25rem' }}>
              <Zap size={24} />
            </div>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '0.5rem', color: '#0f172a' }}>
              Flow Analytics Engine
            </h3>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', lineHeight: 1.6 }}>
              Quantify deep work segments with high accuracy based on continuous IDE code edit telemetry.
            </p>
          </div>

          <div className="glass-panel glass-panel-interactive" style={{ padding: '2.25rem 1.6rem', textAlign: 'left', background: '#ffffff' }}>
            <div className="stat-icon-wrapper" style={{ marginBottom: '1.25rem' }}>
              <Shuffle size={24} color="#0284c7" />
            </div>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '0.5rem', color: '#0f172a' }}>
              Context Switching Trace
            </h3>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', lineHeight: 1.6 }}>
              Identify cognitive shifts between Slack messages, code reviews, and active debugging sessions.
            </p>
          </div>

          <div className="glass-panel glass-panel-interactive" style={{ padding: '2.25rem 1.6rem', textAlign: 'left', background: '#ffffff' }}>
            <div className="stat-icon-wrapper" style={{ marginBottom: '1.25rem' }}>
              <Clock size={24} color="#06b6d4" />
            </div>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '0.5rem', color: '#0f172a' }}>
              Recovery Latency Audit
            </h3>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', lineHeight: 1.6 }}>
              Measure exact minutes required for engineers to regain peak focus after unplanned interruptions.
            </p>
          </div>

          <div className="glass-panel glass-panel-interactive" style={{ padding: '2.25rem 1.6rem', textAlign: 'left', background: '#ffffff' }}>
            <div className="stat-icon-wrapper" style={{ marginBottom: '1.25rem' }}>
              <Cpu size={24} color="#10b981" />
            </div>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '0.5rem', color: '#0f172a' }}>
              Workday Simulator
            </h3>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', lineHeight: 1.6 }}>
              Simulate daily event schedules to test optimization hypotheses before altering team workflows.
            </p>
          </div>
        </div>
      </section>

      {/* 4. WORKFLOW PIPELINE */}
      <section className="glass-panel" style={{ padding: '3.75rem 2.5rem', background: '#ffffff' }}>
        <div style={{ textAlign: 'center', marginBottom: '3.5rem' }}>
          <h2 style={{ fontSize: '2.25rem', fontWeight: 800, marginBottom: '0.5rem', color: '#0f172a' }}>
            How CogniFlow Works
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '1rem' }}>
            Three seamless steps to transform team productivity
          </p>
        </div>

        <div className="grid-3" style={{ gap: '2rem' }}>
          <div style={{ textAlign: 'left' }}>
            <div
              style={{
                fontSize: '3rem',
                fontWeight: 900,
                color: 'rgba(14, 165, 233, 0.25)',
                fontFamily: 'var(--font-heading)',
                marginBottom: '0.5rem',
              }}
            >
              01
            </div>
            <h4 style={{ fontSize: '1.15rem', fontWeight: 700, color: '#0f172a', marginBottom: '0.5rem' }}>
              Ingest Telemetry Events
            </h4>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', lineHeight: 1.6 }}>
              Streams raw developer interactions from VS Code, IntelliJ, Slack channels, Jira tickets, and GitHub commits.
            </p>
          </div>

          <div style={{ textAlign: 'left' }}>
            <div
              style={{
                fontSize: '3rem',
                fontWeight: 900,
                color: 'rgba(56, 189, 248, 0.3)',
                fontFamily: 'var(--font-heading)',
                marginBottom: '0.5rem',
              }}
            >
              02
            </div>
            <h4 style={{ fontSize: '1.15rem', fontWeight: 700, color: '#0f172a', marginBottom: '0.5rem' }}>
              FastAPI Neural Scoring
            </h4>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', lineHeight: 1.6 }}>
              Calculates focus time, distraction impact, and mental recovery cycles via SQLAlchemy and PostgreSQL.
            </p>
          </div>

          <div style={{ textAlign: 'left' }}>
            <div
              style={{
                fontSize: '3rem',
                fontWeight: 900,
                color: 'rgba(16, 185, 129, 0.25)',
                fontFamily: 'var(--font-heading)',
                marginBottom: '0.5rem',
              }}
            >
              03
            </div>
            <h4 style={{ fontSize: '1.15rem', fontWeight: 700, color: '#0f172a', marginBottom: '0.5rem' }}>
              Actionable Flow Insights
            </h4>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', lineHeight: 1.6 }}>
              Delivers real-time team recommendations, focus score rankings, and daily automated executive summaries.
            </p>
          </div>
        </div>
      </section>

      {/* 5. CALL TO ACTION BANNER */}
      <section
        className="glass-panel"
        style={{
          padding: '4.25rem 2.5rem',
          textAlign: 'center',
          background: 'linear-gradient(135deg, rgba(239, 248, 255, 0.95) 0%, rgba(224, 242, 254, 0.9) 100%)',
          borderColor: 'rgba(14, 165, 233, 0.3)',
          boxShadow: '0 20px 50px rgba(14, 165, 233, 0.15)',
        }}
      >
        <h2 style={{ fontSize: '2.5rem', fontWeight: 800, marginBottom: '1rem', color: '#0f172a' }}>
          Ready to Experience CogniFlow?
        </h2>
        <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)', maxWidth: '560px', margin: '0 auto 2.25rem' }}>
          Launch the modern light sky-blue workspace connected directly to your FastAPI backend.
        </p>

        <button
          onClick={() => navigate('/workspace')}
          className="btn-glass btn-primary btn-lg btn-pill"
          style={{ padding: '1rem 2.75rem', fontSize: '1.1rem' }}
        >
          <span>Enter Workspace</span>
          <ArrowRight size={20} />
        </button>
      </section>
    </div>
  );
};

export default Landing;
