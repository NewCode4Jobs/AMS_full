class AlarmFilters {
    constructor() {
        this.filters = {
            severity: '',
            status: '',
            source: '',
            search: ''
        };
        this.filterChangeCallbacks = [];
        this.form = document.getElementById('filterForm');
        this.setupEventListeners();
    }

    setupEventListeners() {
        this.form.addEventListener('input', this.handleFilterChange.bind(this));
    }

    handleFilterChange(event) {
        const { name, value } = event.target;
        this.filters[name] = value;
        this.notifyFilterChange();
    }

    onFilterChange(callback) {
        this.filterChangeCallbacks.push(callback);
    }

    notifyFilterChange() {
        this.filterChangeCallbacks.forEach(callback => callback(this.filters));
    }

    getFilters() {
        return { ...this.filters };
    }

    clearFilters() {
        this.filters = {
            severity: '',
            status: '',
            source: '',
            search: ''
        };
        
        // Reset form inputs
        Array.from(this.form.elements).forEach(element => {
            if (element.tagName === 'SELECT' || element.tagName === 'INPUT') {
                element.value = '';
            }
        });

        this.notifyFilterChange();
    }

    filterAlarms(alarms) {
        return alarms.filter(alarm => {
            const matchesSeverity = !this.filters.severity || alarm.severity === this.filters.severity;
            const matchesStatus = !this.filters.status || alarm.status === this.filters.status;
            const matchesSource = !this.filters.source || alarm.source === this.filters.source;
            
            const searchTerm = this.filters.search.toLowerCase();
            const matchesSearch = !searchTerm || 
                alarm.name.toLowerCase().includes(searchTerm) ||
                alarm.description.toLowerCase().includes(searchTerm);

            return matchesSeverity && matchesStatus && matchesSource && matchesSearch;
        });
    }
}

const alarmFilters = new AlarmFilters();
