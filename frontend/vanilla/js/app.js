// This file is intentionally minimal as each component is self-initializing
document.addEventListener('DOMContentLoaded', () => {
    // The following objects are already initialized in their respective files:
    // - apiService (api.js)
    // - alarmFilters (filters.js)
    // - alarmStats (stats.js)
    // - alarmManager (alarms.js)

    // Add any global event listeners or initialization here if needed
    window.addEventListener('error', (event) => {
        console.error('Global error:', event.error);
    });
});
