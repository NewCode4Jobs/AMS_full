import axios from 'axios';
import { API_CONFIG } from '../config/api';

// Create axios instance with base configuration
const apiClient = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const alarmService = {
  getAlarms: async () => {
    const response = await apiClient.get('/alarms');
    return response.data;
  },

  getAlarmStats: async () => {
    console.log('Fetching stats...');
    const response = await apiClient.get('/alarms/stats');
    console.log('Stats: ', response.data);
    return response.data;
  },

  createAlarm: async (alarmData) => {
    const response = await apiClient.post('/alarms', alarmData);
    return response.data;
  },

  updateAlarm: async (id, alarmData) => {
    const response = await apiClient.put(`/alarms/${id}`, alarmData);
    return response.data;
  },

  deleteAlarm: async (id) => {
    const response = await apiClient.delete(`/alarms/${id}`);
    return response.data;
  }
};