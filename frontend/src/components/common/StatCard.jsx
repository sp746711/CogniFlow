import React from 'react';

export const StatCard = ({
  label,
  value,
  subtext,
  icon: Icon,
  trend,
  className = '',
}) => {
  return (
    <div className={`glass-panel stat-card ${className}`}>
      <div className="stat-info">
        <span className="stat-label">{label}</span>
        <span className="stat-value">{value ?? '—'}</span>
        {subtext && (
          <span className="stat-subtext">
            {trend && (
              <span className={`badge badge-${trend === 'up' ? 'success' : 'warning'}`}>
                {trend === 'up' ? '↑' : '↓'}
              </span>
            )}
            {subtext}
          </span>
        )}
      </div>
      {Icon && (
        <div className="stat-icon-wrapper">
          <Icon size={24} />
        </div>
      )}
    </div>
  );
};

export default StatCard;
