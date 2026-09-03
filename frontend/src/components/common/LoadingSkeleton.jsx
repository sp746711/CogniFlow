import React from 'react';

export const LoadingSkeleton = ({ count = 3, type = 'card' }) => {
  return (
    <div className={`grid-${Math.min(count, 4)}`}>
      {Array.from({ length: count }).map((_, idx) => (
        <div key={idx} className="glass-panel skeleton skeleton-card" style={{ padding: '1.5rem' }}>
          <div className="skeleton skeleton-title" />
          <div className="skeleton skeleton-text" />
          <div className="skeleton skeleton-text" style={{ width: '60%' }} />
        </div>
      ))}
    </div>
  );
};

export default LoadingSkeleton;
