import React from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';
import Sidebar from '../components/layout/Sidebar';
import Navbar from '../components/layout/Navbar';
import Footer from '../components/layout/Footer';
import RunSimulationModal from '../components/simulation/RunSimulationModal';

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

const pageTitles = {
  '/': 'Dashboard Overview',
  '/live': 'Live Monitor Stream',
  '/developers': 'Developers Directory',
  '/teams': 'Engineered Teams',
  '/flow': 'Flow Analytics Engine',
  '/interruptions': 'Interruption Analytics',
  '/context-switching': 'Context-Switch Analytics',
  '/recovery': 'Recovery Time Analytics',
  '/timeline': 'Chronological Timeline',
  '/reports': 'Daily Productivity Reports',
  '/simulation': 'Workday Simulation Engine',
  '/settings': 'Platform Settings',
  '/profile': 'Workspace Profile',
};

export const AppRoutes = () => {
  const location = useLocation();

  // Determine current page title
  let title = pageTitles[location.pathname];
  if (!title) {
    if (location.pathname.startsWith('/developers/')) title = 'Developer Performance Detail';
    else if (location.pathname.startsWith('/teams/')) title = 'Team Performance Detail';
    else title = 'CogniFlow';
  }

  return (
    <div className="app-container">
      <Sidebar />
      <div className="main-wrapper">
        <Navbar title={title} />
        <main className="content-area">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/live" element={<LiveMonitor />} />
            <Route path="/developers" element={<Developers />} />
            <Route path="/developers/:id" element={<DeveloperDetail />} />
            <Route path="/teams" element={<Teams />} />
            <Route path="/teams/:id" element={<TeamDetail />} />
            <Route path="/flow" element={<FlowAnalytics />} />
            <Route path="/interruptions" element={<InterruptionAnalytics />} />
            <Route path="/context-switching" element={<ContextSwitching />} />
            <Route path="/recovery" element={<RecoveryAnalytics />} />
            <Route path="/timeline" element={<Timeline />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/simulation" element={<Simulation />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
        <Footer />
      </div>
      <RunSimulationModal />
    </div>
  );
};

export default AppRoutes;
