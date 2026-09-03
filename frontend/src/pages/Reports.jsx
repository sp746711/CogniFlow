import React, { useEffect, useState } from 'react';
import { useApp } from '../context/AppContext';
import api from '../services/api';
import GlassCard from '../components/common/GlassCard';
import StatCard from '../components/common/StatCard';
import FlowGauge from '../components/common/FlowGauge';
import SkeletonLoader from '../components/ui/SkeletonLoader';
import ErrorState from '../components/ui/ErrorState';
import EmptyState from '../components/ui/EmptyState';
import { FileText, Calendar, Printer, Award, Users, Building2, Zap, BellOff, Shuffle, Clock } from 'lucide-react';

export const Reports = () => {
  const { selectedDate } = useApp();
  const [reportDate, setReportDate] = useState(selectedDate);
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchReport = async () => {
    setLoading(true);
    try {
      const data = await api.getDailyReport(reportDate);
      setReport(data);
      setError(null);
    } catch (err) {
      setError(err.message || 'Failed to generate daily productivity report.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReport();
  }, [reportDate]);

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* Header & Controls */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: 800, color: '#ffffff' }}>
            Executive <span className="gradient-text">Productivity Reports</span>
          </h1>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
            Automated daily snapshot of team focus time, flow sessions, and interruptions.
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Calendar size={16} style={{ color: '#8b5cf6' }} />
            <input
              type="date"
              className="glass-input"
              style={{ width: 'auto', padding: '0.45rem 0.85rem' }}
              value={reportDate}
              onChange={(e) => setReportDate(e.target.value)}
            />
          </div>

          <button onClick={handlePrint} className="btn-glass btn-secondary btn-sm btn-pill" style={{ gap: '0.4rem' }}>
            <Printer size={14} /> Print Report
          </button>
        </div>
      </div>

      {/* Report Document Content */}
      {loading ? (
        <SkeletonLoader type="cards" count={4} />
      ) : error ? (
        <ErrorState message={error} onRetry={fetchReport} />
      ) : !report ? (
        <EmptyState title="No Report Available" description="No activity report found for the selected date. Try running a workday simulation first." />
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
          {/* Executive Summary Card */}
          <GlassCard>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid var(--glass-border-subtle)', paddingBottom: '1rem', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
              <div>
                <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: '#ffffff' }}>
                  CogniFlow Executive Productivity Snapshot
                </h2>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
                  Workday Date: <strong style={{ color: '#ffffff' }}>{report.work_date}</strong> (10:00 AM – 6:00 PM)
                </p>
              </div>
              <span className="badge badge-success" style={{ fontSize: '0.85rem', padding: '0.5rem 1rem' }}>
                Verified FastAPI Telemetry
              </span>
            </div>

            <div className="grid-3" style={{ gridTemplateColumns: '1fr 2fr' }}>
              <FlowGauge
                score={report.flow_score ?? 0}
                title="Workday Flow Index"
                description="Aggregated workflow efficiency"
              />

              <div className="grid-2">
                <StatCard label="Total Teams" value={report.teams} icon={Building2} />
                <StatCard label="Total Developers" value={report.developers} icon={Users} />
                <StatCard label="Total Events" value={report.events} icon={FileText} />
                <StatCard label="Flow Sessions" value={report.flow_sessions} icon={Zap} />
              </div>
            </div>
          </GlassCard>

          {/* Secondary Metric Breakdown Grid */}
          <div className="grid-4">
            <StatCard
              label="Focused Time"
              value={`${Math.round((report.total_focused_time_seconds || 0) / 60)} min`}
              subtext="Total focus time"
              icon={Clock}
            />
            <StatCard
              label="Avg Flow Session"
              value={`${Math.round((report.average_flow_seconds || 0) / 60)} min`}
              subtext="Average duration"
              icon={Award}
            />
            <StatCard
              label="Interruptions"
              value={report.interruptions}
              subtext="Disruption events"
              icon={BellOff}
            />
            <StatCard
              label="Context Switches"
              value={report.context_switches}
              subtext="Tool transitions"
              icon={Shuffle}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default Reports;

