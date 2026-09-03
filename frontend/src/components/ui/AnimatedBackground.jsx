import React from 'react';

export const AnimatedBackground = () => {
  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        pointerEvents: 'none',
        zIndex: 0,
        overflow: 'hidden',
        background: '#f7fbff',
      }}
    >
      {/* Animated Soft Sky-Blue Glowing Blobs */}
      <div
        className="ambient-blob blob-1"
        style={{
          position: 'absolute',
          top: '-20%',
          left: '15%',
          width: '650px',
          height: '650px',
          borderRadius: '50%',
          background: 'radial-gradient(circle, rgba(56, 189, 248, 0.22) 0%, rgba(56, 189, 248, 0) 70%)',
          filter: 'blur(70px)',
          animation: 'floatBlob1 22s ease-in-out infinite alternate',
        }}
      />
      <div
        className="ambient-blob blob-2"
        style={{
          position: 'absolute',
          top: '35%',
          right: '-10%',
          width: '700px',
          height: '700px',
          borderRadius: '50%',
          background: 'radial-gradient(circle, rgba(14, 165, 233, 0.18) 0%, rgba(14, 165, 233, 0) 70%)',
          filter: 'blur(90px)',
          animation: 'floatBlob2 28s ease-in-out infinite alternate',
        }}
      />
      <div
        className="ambient-blob blob-3"
        style={{
          position: 'absolute',
          bottom: '-15%',
          left: '30%',
          width: '600px',
          height: '600px',
          borderRadius: '50%',
          background: 'radial-gradient(circle, rgba(103, 232, 249, 0.25) 0%, rgba(103, 232, 249, 0) 70%)',
          filter: 'blur(80px)',
          animation: 'floatBlob3 25s ease-in-out infinite alternate',
        }}
      />

      {/* Faint Subtle Light Grid Overlay */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          backgroundImage: `radial-gradient(rgba(14, 165, 233, 0.08) 1px, transparent 1px)`,
          backgroundSize: '40px 40px',
          opacity: 0.5,
        }}
      />

      {/* Keyframe animations */}
      <style>{`
        @keyframes floatBlob1 {
          0% { transform: translate(0, 0) scale(1); }
          50% { transform: translate(70px, 50px) scale(1.08); }
          100% { transform: translate(-50px, 90px) scale(0.95); }
        }
        @keyframes floatBlob2 {
          0% { transform: translate(0, 0) scale(1); }
          50% { transform: translate(-90px, 70px) scale(1.1); }
          100% { transform: translate(50px, -60px) scale(0.92); }
        }
        @keyframes floatBlob3 {
          0% { transform: translate(0, 0) scale(1); }
          50% { transform: translate(-50px, -70px) scale(1.12); }
          100% { transform: translate(70px, 40px) scale(1); }
        }
        @media (prefers-reduced-motion: reduce) {
          .ambient-blob { animation: none !important; }
        }
      `}</style>
    </div>
  );
};

export default AnimatedBackground;
