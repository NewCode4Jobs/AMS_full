class AlarmManager {
    constructor() {
        this.alarms = [];
        this.grid = document.getElementById('alarmGrid');
        this.modal = new bootstrap.Modal(document.getElementById('alarmModal'));
        this.form = document.getElementById('alarmForm');
        this.saveBtn = document.getElementById('saveAlarmBtn');
        this.newBtn = document.getElementById('newAlarmBtn');
        this.selectedAlarm = null;
        
        this.setupEventListeners();
    }

    async init() {
        await this.fetchAlarms();
    }

    setupEventListeners() {
        this.newBtn.addEventListener('click', () => this.showCreateModal());
        this.saveBtn.addEventListener('click', () => this.handleSave());
        alarmFilters.onFilterChange(() => this.renderAlarms());
    }

    async fetchAlarms() {
        try {
            this.showLoading();
            this.alarms = await apiService.getAlarms();
            this.renderAlarms();
        } catch (error) {
            console.error('Error fetching alarms:', error);
            this.showError();
        }
    }

    renderAlarms() {
        const filteredAlarms = alarmFilters.filterAlarms(this.alarms);
        
        if (filteredAlarms.length === 0) {
            this.showEmptyState();
            return;
        }

        this.grid.innerHTML = '';
        filteredAlarms.forEach(alarm => {
            const card = this.createAlarmCard(alarm);
            this.grid.appendChild(card);
        });
    }

    createAlarmCard(alarm) {
        const card = document.createElement('div');
        card.className = 'card alarm-card severity-' + alarm.severity;
        card.innerHTML = `
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <h5 class="card-title mb-0">${alarm.name}</h5>
                    <span class="status-badge status-${alarm.status}">${alarm.status}</span>
                </div>
                <p class="card-text">${alarm.description}</p>
                <div class="d-flex justify-content-between align-items-center">
                    <small class="text-muted">
                        <i class="bi bi-clock me-1"></i>
                        ${new Date(alarm.timestamp).toLocaleString()}
                    </small>
                    <div class="btn-group">
                        <button class="btn btn-sm btn-outline-primary edit-btn">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger delete-btn">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;

        // Add event listeners
        card.querySelector('.edit-btn').addEventListener('click', () => this.showEditModal(alarm));
        card.querySelector('.delete-btn').addEventListener('click', () => this.handleDelete(alarm));

        return card;
    }

    showCreateModal() {
        this.selectedAlarm = null;
        document.getElementById('alarmModalTitle').textContent = 'New Alarm';
        this.form.reset();
        this.modal.show();
    }

    showEditModal(alarm) {
        this.selectedAlarm = alarm;
        document.getElementById('alarmModalTitle').textContent = 'Edit Alarm';
        
        // Fill form with alarm data
        Object.entries(alarm).forEach(([key, value]) => {
            const input = this.form.elements[key];
            if (input) input.value = value;
        });

        this.modal.show();
    }

    async handleSave() {
        const formData = new FormData(this.form);
        const alarmData = Object.fromEntries(formData.entries());
        console.log('alarmdata: ', alarmData);
        // Add required fields
        alarmData.status = 'active';  // New alarms are always active
        alarmData.acknowledged = false;  // New alarms are not acknowledged

        try {
            if (this.selectedAlarm) {
                await apiService.updateAlarm(this.selectedAlarm.id, alarmData);
            } else {
                await apiService.createAlarm(alarmData);
            }

            this.modal.hide();
            await this.fetchAlarms();
            await alarmStats.updateStats();
        } catch (error) {
            console.error('Error saving alarm:', error);
            alert('Failed to save alarm: ' + error.message);
        }
    }

    async handleDelete(alarm) {
        if (!confirm('Are you sure you want to delete this alarm?')) return;

        try {
            await apiService.deleteAlarm(alarm.id);
            await this.fetchAlarms();
            await alarmStats.updateStats();
        } catch (error) {
            console.error('Error deleting alarm:', error);
            alert('Failed to delete alarm');
        }
    }

    showLoading() {
        this.grid.innerHTML = `
            <div class="loading-spinner">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `;
    }

    showError() {
        this.grid.innerHTML = `
            <div class="empty-state">
                <i class="bi bi-exclamation-triangle text-danger"></i>
                <p>Failed to load alarms</p>
                <button class="btn btn-primary btn-sm" onclick="alarmManager.fetchAlarms()">
                    <i class="bi bi-arrow-clockwise me-1"></i>
                    Retry
                </button>
            </div>
        `;
    }

    showEmptyState() {
        const filters = alarmFilters.getFilters();
        const hasActiveFilters = Object.values(filters).some(value => value !== '');
        
        this.grid.innerHTML = `
            <div class="empty-state">
                <i class="bi bi-inbox"></i>
                <p>${hasActiveFilters ? 'No alarms match the current filters' : 'No alarms found'}</p>
                ${hasActiveFilters ? `
                    <button class="btn btn-link" onclick="alarmFilters.clearFilters()">
                        Clear Filters
                    </button>
                ` : ''}
            </div>
        `;
    }
}

const alarmManager = new AlarmManager();
alarmManager.init();
