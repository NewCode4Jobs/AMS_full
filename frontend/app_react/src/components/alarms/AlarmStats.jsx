import { ListGroup } from 'react-bootstrap';
import { useAlarmStats } from '../../hooks/useAlarms';

export function AlarmStats() {
  const { data: stats, isLoading, error } = useAlarmStats();

  if (isLoading) {
    return <div>Loading stats...</div>;
  }

  if (error) {
    return <div>Error loading stats: {error.message}</div>;
  }

  const statsList = [
    // Severity stats
    {
      name: 'Critical Alarms',
      value: stats.by_severity.critical,
      color: 'danger',
    },
    {
      name: 'High Priority',
      value: stats.by_severity.high,
      color: 'warning',
    },
    {
      name: 'Medium Priority',
      value: stats.by_severity.medium,
      color: 'info',
    },
    {
      name: 'Low Priority',
      value: stats.by_severity.low,
      color: 'success',
    },
    // Status stats
    {
      name: 'Active Alarms',
      value: stats.by_status.active,
      color: 'danger',
    },
    {
      name: 'Acknowledged',
      value: stats.by_status.acknowledged,
      color: 'warning',
    },
    {
      name: 'Resolved',
      value: stats.by_status.resolved,
      color: 'success',
    },
    // Source stats
    {
      name: 'System Alarms',
      value: stats.by_source.system,
      color: 'primary',
    },
    {
      name: 'Application Alarms',
      value: stats.by_source.application,
      color: 'info',
    },
    {
      name: 'Security Alarms',
      value: stats.by_source.security,
      color: 'danger',
    },
  ];

  return (
    <div>
      <h5 className="mb-4">Alarm Statistics</h5>
      <div className="mb-4">
        <div className="text-muted mb-2">Total Alarms</div>
        <h3>{stats.total}</h3>
      </div>
      <ListGroup>
        {statsList.map((stat) => (
          <ListGroup.Item
            key={stat.name}
            variant={stat.color}
            className="d-flex justify-content-between align-items-center mb-2"
          >
            <div>
              <div className="text-muted">{stat.name}</div>
              <h5 className="mb-0">{stat.value}</h5>
            </div>
            <div className={`badge bg-${stat.color} rounded-pill`}>
              {((stat.value / stats.total) * 100).toFixed(1)}%
            </div>
          </ListGroup.Item>
        ))}
      </ListGroup>
    </div>
  );
}