import React from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import FloatingNavbar from '../components/layout/FloatingNavbar';
import AnimatedBackground from '../components/ui/AnimatedBackground';
import Footer from '../components/layout/Footer';
import RunSimulationModal from '../components/simulation/RunSimulationModal';

import Landing from '../pages/Landing';
import Dashboard from '../pages/Dashboard';
import LiveMonitor from '../pages/LiveMonitor';
import Developers from '../pages/Developers';
import DeveloperDetail from '../pages/DeveloperDetail';
import Teams from '../pages/Teams';
import TeamDetail from '../pages/TeamDetail';
import FlowAnalytics from '../pages/FlowAnalytics';
import InterruptionAnalytics from '../pages/InterruptionAnalytics';
import ContextSwitching from '../pages/ContextSwitching';
import RecoveryAnalytics from '../pages/RecoveryAnalytics';
import Timeline from '../pages/Timeline';
import Reports from '../pages/Reports';
import Simulation from '../pages/Simulation';
import Settings from '../pages/Settings';
import Profile from '../pages/Profile';
import NotFound from '../pages/NotFound';

export const AppRoutes = () => {
  const location = useLocation();
  const isWorkspace = location.pathname.startsWith('/workspace');

  return (
    <div className="app-container">
      <AnimatedBackground />

      {/* Floating Workspace Navbar ONLY rendered inside /workspace routes. NO NAVBAR ON LANDING PAGE! */}
      {isWorkspace && <FloatingNavbar />}

      <div className="main-wrapper" style={{ paddingTop: isWorkspace ? 'var(--navbar-height)' : '0px' }}>
        <AnimatePresence mode="wait">
          <motion.main
            key={location.pathname}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
            className="content-area"
          >
            <Routes location={location}>
              {/* Default Landing Page Route (NO NAVBAR HERE) */}
              <Route path="/" element={<Landing />} />

              {/* Main Workspace Routes */}
              <Route path="/workspace" element={<Dashboard />} />
              <Route path="/workspace/live" element={<LiveMonitor />} />
              <Route path="/workspace/developers" element={<Developers />} />
              <Route path="/workspace/developers/:id" element={<DeveloperDetail />} />
              <Route path="/workspace/teams" element={<Teams />} />
              <Route path="/workspace/teams/:id" element={<TeamDetail />} />
              <Route path="/workspace/flow" element={<FlowAnalytics />} />
              <Route path="/workspace/interruptions" element={<InterruptionAnalytics />} />
              <Route path="/workspace/context-switching" element={<ContextSwitching />} />
              <Route path="/workspace/recovery" element={<RecoveryAnalytics />} />
              <Route path="/workspace/timeline" element={<Timeline />} />
              <Route path="/workspace/reports" element={<Reports />} />
              <Route path="/workspace/simulation" element={<Simulation />} />
              <Route path="/workspace/settings" element={<Settings />} />
              <Route path="/workspace/profile" element={<Profile />} />

              <Route path="*" element={<NotFound />} />
            </Routes>
          </motion.main>
        </AnimatePresence>
        <Footer />
      </div>

      <RunSimulationModal />
    </div>
  );
};

export default AppRoutes;
