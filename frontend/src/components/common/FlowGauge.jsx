import React from 'react';

export const FlowGauge = ({ score = 0, title = 'Flow Score', description }) => {
  const numericScore = typeof score === 'number' ? Math.min(Math.max(score, 0), 100) : 0;
  
  // Calculate flow state text & badge color
  let statusText = 'Optimal Flow';
  let badgeClass = 'badge-success';
  if (numericScore < 40) {
    statusText = 'Fragmented Work';
    badgeClass = 'badge-danger';
  } else if (numericScore < 70) {
    statusText = 'Moderate Focus';
    badgeClass = 'badge-warning';
  }

  return (
    <div className="flow-score-gauge">
      <div className="gauge-circle">
        <span className="gauge-score">{numericScore.toFixed(1)}</span>
        <span className="gauge-max">/ 100</span>
      </div>
      <span className={`badge ${badgeClass}`} style={{ marginBottom: '0.5rem' }}>
        {statusText}
      </span>
      <h4 style={{ fontSize: '1.1rem', marginTop: '0.25rem' }}>{title}</h4>
      {description && (
        <p style={{ fontSize: '0.825rem', color: 'var(--text-subtle)', marginTop: '0.25rem' }}>
          {description}
        </p>
      )}
    </div>
  );
};

export default FlowGauge;
