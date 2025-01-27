import { useState } from 'react';
import { Button, Row, Col } from 'react-bootstrap';
import { AlarmCard } from './AlarmCard';
import { AlarmForm } from './AlarmForm';
import { useAlarms } from '../../hooks/useAlarms';
import { useQueryClient } from '@tanstack/react-query';

export function AlarmGrid() {
  const [showForm, setShowForm] = useState(false);
  const [selectedAlarm, setSelectedAlarm] = useState(null);
  const { data: alarms, isLoading, error } = useAlarms();
  const queryClient = useQueryClient();
  const filters = queryClient.getQueryData(['alarmFilters']);
  console.log('AlarmGrid: ', filters);

  const handleEdit = (alarm) => {
    setSelectedAlarm(alarm);
    setShowForm(true);
  };

  const handleClose = () => {
    setSelectedAlarm(null);
    setShowForm(false);
  };

  if (isLoading) {
    return (
      <div className="text-center py-5">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-5 text-danger">
        <i className="bi bi-exclamation-triangle fs-1"></i>
        <p className="mt-3">Error loading alarms: {error.message}</p>
      </div>
    );
  }

  const hasActiveFilters = filters && Object.values(filters).some(value => value !== '');
  const noAlarmsMessage = hasActiveFilters 
    ? "No alarms match the current filters"
    : "No alarms found";

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h5 className="mb-0">Alarms</h5>
        <Button variant="primary" size="sm" onClick={() => setShowForm(true)}>
          <i className="bi bi-plus-lg me-1"></i>
          New Alarm
        </Button>
      </div>

      {alarms.length === 0 ? (
        <div className="text-center py-5 text-muted">
          <i className="bi bi-inbox fs-1"></i>
          <p className="mt-3">{noAlarmsMessage}</p>
          {hasActiveFilters && (
            <Button 
              variant="link" 
              onClick={() => queryClient.setQueryData(['alarmFilters'], {
                severity: '',
                status: '',
                source: '',
                search: ''
              })}
            >
              Clear Filters
            </Button>
          )}
        </div>
      ) : (
        <Row xs={1} className="g-4">
          {alarms.map((alarm) => (
            <Col key={alarm.id}>
              <AlarmCard alarm={alarm} onEdit={() => handleEdit(alarm)} />
            </Col>
          ))}
        </Row>
      )}

      <AlarmForm
        show={showForm}
        onHide={handleClose}
        alarm={selectedAlarm}
      />
    </div>
  );
}