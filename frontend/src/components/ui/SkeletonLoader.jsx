import React from 'react';

export const SkeletonLoader = ({ type = 'cards', count = 4 }) => {
  if (type === 'cards') {
    return (
      <div className="grid-4" style={{ marginBottom: '2rem' }}>
        {Array.from({ length: count }).map((_, i) => (
          <div key={i} className="glass-panel skeleton-card skeleton" />
        ))}
      </div>
    );
  }

  if (type === 'table') {
    return (
      <div className="glass-panel" style={{ padding: '1.5rem' }}>
        <div className="skeleton skeleton-title" />
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
          {Array.from({ length: count }).map((_, i) => (
            <div key={i} className="skeleton skeleton-text" style={{ width: `${90 - i * 10}%` }} />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="glass-panel" style={{ padding: '2rem' }}>
      <div className="skeleton skeleton-title" />
      <div className="skeleton skeleton-text" />
      <div className="skeleton skeleton-text" style={{ width: '60%' }} />
    </div>
  );
};

export default SkeletonLoader;
