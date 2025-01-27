class AlarmStats {
    constructor() {
        this.statsContainer = document.getElementById('statsContent');
        this.updateInterval = null;
        this.startAutoUpdate();
    }

    startAutoUpdate() {
        this.updateStats();
        this.updateInterval = setInterval(() => this.updateStats(), 60000);
    }

    stopAutoUpdate() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
    }

    async updateStats() {
        try {
            const stats = await apiService.getAlarmStats();
            this.renderStats(stats);
        } catch (error) {
            console.error('Error updating stats:', error);
            this.renderError();
        }
    }

    renderStats(stats) {
        const statsHtml = `
            <div class="col-md-3">
                <div class="stat-card">
                    <div class="stat-title">Total Alarms</div>
                    <div class="stat-value">${stats.total}</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card">
                    <div class="stat-title">By Severity</div>
                    <div class="stat-details">
                        <div>Critical: ${stats.by_severity.critical || 0}</div>
                        <div>High: ${stats.by_severity.high || 0}</div>
                        <div>Medium: ${stats.by_severity.medium || 0}</div>
                        <div>Low: ${stats.by_severity.low || 0}</div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card">
                    <div class="stat-title">By Status</div>
                    <div class="stat-details">
                        <div>Active: ${stats.by_status.active || 0}</div>
                        <div>Acknowledged: ${stats.by_status.acknowledged || 0}</div>
                        <div>Resolved: ${stats.by_status.resolved || 0}</div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card">
                    <div class="stat-title">By Source</div>
                    <div class="stat-details">
                        <div>System: ${stats.by_source.system || 0}</div>
                        <div>Application: ${stats.by_source.application || 0}</div>
                        <div>Security: ${stats.by_source.security || 0}</div>
                    </div>
                </div>
            </div>
        `;
        this.statsContainer.innerHTML = statsHtml;
    }

    renderError() {
        this.statsContainer.innerHTML = `
            <div class="text-center text-danger">
                <i class="bi bi-exclamation-triangle fs-1"></i>
                <p class="mt-2">Failed to load statistics</p>
            </div>
        `;
    }
}

const alarmStats = new AlarmStats();
