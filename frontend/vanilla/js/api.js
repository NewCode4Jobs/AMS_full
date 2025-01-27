const API_BASE_URL = 'http://localhost:8000/api/v1';

class ApiService {
    async handleResponse(response) {
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'API request failed');
        }
        return response.json();
    }

    async getAlarms() {
        const response = await fetch(`${API_BASE_URL}/alarms`);
        return this.handleResponse(response);
    }

    async getAlarmStats() {
        const response = await fetch(`${API_BASE_URL}/alarms/stats`);
        return this.handleResponse(response);
    }

    async createAlarm(alarmData) {
        console.log('Creating alarm with data:', alarmData);
        const response = await fetch(`${API_BASE_URL}/alarms`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(alarmData),
        });
        return this.handleResponse(response);
    }

    async updateAlarm(id, alarmData) {
        console.log('Updating alarm with data:', alarmData);
        const response = await fetch(`${API_BASE_URL}/alarms/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(alarmData),
        });
        return this.handleResponse(response);
    }

    async deleteAlarm(id) {
        const response = await fetch(`${API_BASE_URL}/alarms/${id}`, {
            method: 'DELETE',
        });
        return this.handleResponse(response);
    }
}

const apiService = new ApiService();
