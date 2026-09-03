import React, { useEffect, useState } from 'react';
import { useApp } from '../context/AppContext';
import api from '../services/api';
import GlassCard from '../components/common/GlassCard';
import StatCard from '../components/common/StatCard';
import FlowGauge from '../components/common/FlowGauge';
import LoadingSkeleton from '../components/common/LoadingSkeleton';
import ErrorState from '../components/common/ErrorState';
import EmptyState from '../components/common/EmptyState';
import { FileText, Calendar, Printer, Download, Award, Users, Building2, Zap, BellOff, Shuffle, Clock } from 'lucide-react';

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
    <div className="fade-in">
      {/* Top Report Controls */}
      <GlassCard title="Daily Productivity Report Generator" icon={FileText} style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <Calendar size={18} color="var(--primary-blue)" />
            <span style={{ fontSize: '0.9rem', fontWeight: 700 }}>Select Workday Date:</span>
            <input
              type="date"
              className="glass-input"
              style={{ width: 'auto' }}
              value={reportDate}
              onChange={(e) => setReportDate(e.target.value)}
            />
          </div>

          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button onClick={handlePrint} className="btn-glass btn-sm" style={{ gap: '0.4rem' }}>
              <Printer size={14} /> Print Report
            </button>
          </div>
        </div>
      </GlassCard>

      {/* Report Document Content */}
      {loading ? (
        <LoadingSkeleton count={4} />
      ) : error ? (
        <ErrorState message={error} onRetry={fetchReport} />
      ) : !report ? (
        <EmptyState title="No Report Available" message="No activity report found for the selected date." />
      ) : (
        <div className="fade-in">
          {/* Executive Summary Card */}
          <GlassCard className="mb-6" style={{ marginBottom: '1.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid var(--glass-border-subtle)', paddingBottom: '1rem', marginBottom: '1.25rem' }}>
              <div>
                <h2 style={{ fontSize: '1.5rem', fontWeight: 800 }}>
                  CogniFlow Daily Productivity Snapshot
                </h2>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-subtle)' }}>
                  Workday: <strong>{report.work_date}</strong> (10:00 AM – 6:00 PM)
                </p>
              </div>
              <span className="badge badge-success" style={{ fontSize: '0.85rem', padding: '0.5rem 1rem' }}>
                Report Generated
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
