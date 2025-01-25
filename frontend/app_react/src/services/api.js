import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
});

export const alarmService = {
  getAlarms: async () => {
    const { data } = await api.get('/alarms');
    return data;
  },
  
  createAlarm: async (alarm) => {
    const { data } = await api.post('/alarms', alarm);
    return data;
  },
  
  updateAlarm: async (id, alarm) => {
    const { data } = await api.put(`/alarms/${id}`, alarm);
    return data;
  },
  
  deleteAlarm: async (id) => {
    await api.delete(`/alarms/${id}`);
  },
};