class AlarmSystem {
    constructor() {
        this.alarms = [];
        this.grid = document.getElementById('alarmGrid');
    }

    async fetchAlarms() {
        try {
            const response = await fetch('http://localhost:8000/api/v1/alarms');
            this.alarms = await response.json();
            this.renderAlarms();
        } catch (error) {
            console.error('Error fetching alarms:', error);
        }
    }

    renderAlarms() {
        this.grid.innerHTML = '';
        this.alarms.forEach(alarm => {
            const card = this.createAlarmCard(alarm);
            this.grid.appendChild(card);
        });
    }

    createAlarmCard(alarm) {
        const card = document.createElement('div');
        card.className = `alarm-card severity-${alarm.severity}`;
        card.innerHTML = `
            <h3>${alarm.name}</h3>
            <p>${alarm.description}</p>
            <div class="alarm-meta">
                <span class="source">${alarm.source}</span>
                <span class="timestamp">${new Date(alarm.timestamp).toLocaleString()}</span>
            </div>
        `;
        return card;
    }
}

const alarmSystem = new AlarmSystem();
alarmSystem.fetchAlarms();
