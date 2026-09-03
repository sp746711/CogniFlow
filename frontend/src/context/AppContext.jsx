import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [selectedTeamId, setSelectedTeamId] = useState(null);
  const [selectedDeveloperId, setSelectedDeveloperId] = useState(null);
  const [systemHealth, setSystemHealth] = useState({ status: 'checking', database: 'checking' });
  const [isSimulating, setIsSimulating] = useState(false);
  const [simulationModalOpen, setSimulationModalOpen] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);

  // Poll system health on mount
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const health = await api.getHealthStatus();
        setSystemHealth(health);
      } catch (err) {
        setSystemHealth({ status: 'unhealthy', database: 'unavailable' });
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const triggerRefresh = () => {
    setRefreshKey((prev) => prev + 1);
  };

  const handleRunSimulation = async (workDate = null) => {
    setIsSimulating(true);
    try {
      const result = await api.runSimulation(workDate || selectedDate);
      triggerRefresh();
      return result;
    } finally {
      setIsSimulating(false);
    }
  };

  return (
    <AppContext.Provider
      value={{
        selectedDate,
        setSelectedDate,
        selectedTeamId,
        setSelectedTeamId,
        selectedDeveloperId,
        setSelectedDeveloperId,
        systemHealth,
        isSimulating,
        simulationModalOpen,
        setSimulationModalOpen,
        refreshKey,
        triggerRefresh,
        handleRunSimulation,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};
