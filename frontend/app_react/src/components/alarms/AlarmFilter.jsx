// src/components/alarms/AlarmFilters.jsx
import { useState } from 'react';
import { Button } from '../ui/Button';

export function AlarmFilters() {
  const [filters, setFilters] = useState({
    severity: 'all',
    source: 'all',
    status: 'all'
  });

  const severityOptions = [
    { value: 'all', label: 'All Severities' },
    { value: 'critical', label: 'Critical' },
    { value: 'high', label: 'High' },
    { value: 'medium', label: 'Medium' },
    { value: 'low', label: 'Low' }
  ];

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  return (
    <div className="bg-gray-800 p-4 rounded-lg">
      <div className="flex flex-wrap items-center gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            Severity
          </label>
          <select
            value={filters.severity}
            onChange={(e) => handleFilterChange('severity', e.target.value)}
            className="w-full bg-gray-700 text-white rounded-md border-gray-600 focus:ring-blue-500 focus:border-blue-500"
          >
            {severityOptions.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        <div className="flex items-end gap-2">
          <Button 
            variant="primary" 
            onClick={() => {/* Apply filters */}}
          >
            Apply Filters
          </Button>
          <Button 
            variant="secondary" 
            onClick={() => setFilters({
              severity: 'all',
              source: 'all',
              status: 'all'
            })}
          >
            Reset
          </Button>
        </div>
      </div>
    </div>
  );
}