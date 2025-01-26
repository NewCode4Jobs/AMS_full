import { Form } from 'react-bootstrap';
import { useQueryClient } from '@tanstack/react-query';
import { useState, useEffect } from 'react';

export function AlarmFilters() {
  const queryClient = useQueryClient();
  const [filters, setFilters] = useState({
    severity: '',
    status: '',
    source: '',
    search: ''
  });

  // Apply filters with debounce
  useEffect(() => {
    const timer = setTimeout(() => {
      queryClient.setQueryData(['alarmFilters'], filters);
    }, 300);

    return () => clearTimeout(timer);
  }, [filters, queryClient]);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div>
      <h5 className="mb-4">Filters</h5>
      <Form>
        <Form.Group className="mb-3">
          <Form.Label>Search</Form.Label>
          <Form.Control
            type="text"
            name="search"
            value={filters.search}
            onChange={handleFilterChange}
            placeholder="Search by name or description"
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Severity</Form.Label>
          <Form.Select
            name="severity"
            value={filters.severity}
            onChange={handleFilterChange}
          >
            <option value="">All Severities</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </Form.Select>
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Status</Form.Label>
          <Form.Select
            name="status"
            value={filters.status}
            onChange={handleFilterChange}
          >
            <option value="">All Statuses</option>
            <option value="active">Active</option>
            <option value="acknowledged">Acknowledged</option>
            <option value="resolved">Resolved</option>
          </Form.Select>
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Source</Form.Label>
          <Form.Select
            name="source"
            value={filters.source}
            onChange={handleFilterChange}
          >
            <option value="">All Sources</option>
            <option value="system">System</option>
            <option value="application">Application</option>
            <option value="security">Security</option>
          </Form.Select>
        </Form.Group>
      </Form>
    </div>
  );
}