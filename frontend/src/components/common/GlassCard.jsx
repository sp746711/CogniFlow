import React from 'react';

export const GlassCard = ({
  children,
  title,
  icon: Icon,
  action,
  className = '',
  interactive = false,
  noPadding = false,
}) => {
  return (
    <div
      className={`glass-panel ${interactive ? 'glass-panel-interactive' : ''} ${className}`}
    >
      {title && (
        <div className="glass-header">
          <div className="glass-header-title">
            {Icon && <Icon size={20} />}
            <span>{title}</span>
          </div>
          {action && <div className="glass-header-action">{action}</div>}
        </div>
      )}
      <div className={noPadding ? '' : 'glass-body'}>{children}</div>
    </div>
  );
};

export default GlassCard;
