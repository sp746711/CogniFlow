import axios from 'axios';

// Base API configuration (Vite proxy handles /api in dev mode)
const API_BASE_URL = import.meta.env.VITE_API_URL || '';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
});

// Helper for error formatting
const handleApiError = (error, fallbackMessage) => {
  const isOffline =
    error.response?.status === 503 ||
    error.code === 'ERR_NETWORK' ||
    error.code === 'ECONNREFUSED' ||
    error.message?.includes('Network Error');

  if (isOffline) {
    console.warn('[API Warning] Backend service is offline or unreachable.');
    const offlineError = new Error(
      'Backend server is offline (http://127.0.0.1:8000). Please start the Python backend service.'
    );
    offlineError.isBackendOffline = true;
    throw offlineError;
  }

  console.error('[API Error]:', error);
  const detail = error.response?.data?.detail || error.message || fallbackMessage;
  throw new Error(detail);
};

export const api = {
  // 1. System Root
  async getSystemRoot() {
    try {
      const response = await client.get('/');
      return response.data;
    } catch (error) {
      return { name: 'CogniFlow', version: '1.0.0', status: 'offline' };
    }
  },

  // 2. Health Check
  async getHealthStatus() {
    try {
      const response = await client.get('/health');
      return response.data;
    } catch (error) {
      return { status: 'offline', database: 'unavailable', dialect: 'none' };
    }
  },

  // 3. Get Teams
  async getTeams() {
    try {
      const response = await client.get('/api/teams');
      return response.data;
    } catch (error) {
      handleApiError(error, 'Failed to fetch teams list.');
    }
  },

  // 4. Get Team Detail
  async getTeam(teamId) {
    try {
      const response = await client.get(`/api/teams/${teamId}`);
      return response.data;
    } catch (error) {
      handleApiError(error, `Failed to fetch team ${teamId}.`);
    }
  },

  // 5. Get Developers
  async getDevelopers() {
    try {
      const response = await client.get('/api/developers');
      return response.data;
    } catch (error) {
      handleApiError(error, 'Failed to fetch developers list.');
    }
  },

  // 6. Get Developer Detail
  async getDeveloper(developerId) {
    try {
      const response = await client.get(`/api/developers/${developerId}`);
      return response.data;
    } catch (error) {
      handleApiError(error, `Failed to fetch developer ${developerId}.`);
    }
  },

  // 7. Get Tasks
  async getTasks() {
    try {
      const response = await client.get('/api/tasks');
      return response.data;
    } catch (error) {
      handleApiError(error, 'Failed to fetch Jira tasks.');
    }
  },

  // 8. Get Task Detail
  async getTask(taskId) {
    try {
      const response = await client.get(`/api/tasks/${taskId}`);
      return response.data;
    } catch (error) {
      handleApiError(error, `Failed to fetch task ${taskId}.`);
    }
  },

  // 9. Get Activity Events
  async getEvents({ developerId, source, startTime, endTime } = {}) {
    try {
      const params = {};
      if (developerId) params.developer_id = developerId;
      if (source) params.source = source;
      if (startTime) params.start_time = startTime;
      if (endTime) params.end_time = endTime;

      const response = await client.get('/api/events', { params });
      return response.data;
    } catch (error) {
      handleApiError(error, 'Failed to fetch activity events.');
    }
  },

  // 10. Get Single Event
  async getEvent(eventId) {
    try {
      const response = await client.get(`/api/events/${eventId}`);
      return response.data;
    } catch (error) {
      handleApiError(error, `Failed to fetch event ${eventId}.`);
    }
  },

  // 11. Get Flow Analytics
  async getFlowMetrics(developerId = null) {
    try {
      const params = developerId ? { developer_id: developerId } : {};
      const response = await client.get('/api/flow', { params });
      return response.data;
    } catch (error) {
      handleApiError(error, 'Failed to fetch flow analytics.');
    }
  },

  // 12. Get Interruption Analytics
  async getInterruptionAnalytics(developerId = null) {
    try {
      const params = developerId ? { developer_id: developerId } : {};
      const response = await client.get('/api/interruptions', { params });
      return response.data;
    } catch (error) {
      handleApiError(error, 'Failed to fetch interruption analytics.');
    }
  },

  // 13. Get Context-Switch Analytics
  async getContextSwitchAnalytics(developerId = null) {
    try {
      const params = developerId ? { developer_id: developerId } : {};
      const response = await client.get('/api/context-switching', { params });
      return response.data;
    } catch (error) {
      handleApiError(error, 'Failed to fetch context-switch analytics.');
    }
  },

  // 14. Get Recovery Analytics
  async getRecoveryAnalytics(developerId = null) {
    try {
      const params = developerId ? { developer_id: developerId } : {};
      const response = await client.get('/api/recovery', { params });
      return response.data;
    } catch (error) {
      handleApiError(error, 'Failed to fetch recovery analytics.');
    }
  },

  // 15. Get Dashboard Overview
  async getDashboardOverview() {
    try {
      const response = await client.get('/api/dashboard');
      return response.data;
    } catch (error) {
      handleApiError(error, 'Failed to fetch overall dashboard metrics.');
    }
  },

  // 16. Get Developer Dashboard Summary
  async getDeveloperDashboard(developerId) {
    try {
      const response = await client.get(`/api/dashboard/developer/${developerId}`);
      return response.data;
    } catch (error) {
      handleApiError(error, `Failed to fetch dashboard metrics for developer ${developerId}.`);
    }
  },

  // 17. Get Daily Productivity Report
  async getDailyReport(workDate = null) {
    try {
      const params = workDate ? { work_date: workDate } : {};
      const response = await client.get('/api/reports/daily', { params });
      return response.data;
    } catch (error) {
      handleApiError(error, 'Failed to fetch daily productivity report.');
    }
  },

  // 18. Run Simulation
  async runSimulation(workDate = null) {
    try {
      const params = workDate ? { work_date: workDate } : {};
      const response = await client.post('/api/simulation/run', null, { params });
      return response.data;
    } catch (error) {
      handleApiError(error, 'Failed to run workday simulation.');
    }
  },
};

export default api;
