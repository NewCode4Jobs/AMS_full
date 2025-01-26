import { useState } from 'react';
import { useAlarms } from '../../hooks/useAlarms';
import { AlarmCard } from './AlarmCard';
import { AlarmForm } from './AlarmForm';
import { Spinner, Button } from 'react-bootstrap';

export function AlarmGrid() {
  const { data: alarms, isLoading, error } = useAlarms();
  const [showForm, setShowForm] = useState(false);
  const [selectedAlarm, setSelectedAlarm] = useState(null);

  const handleEdit = (alarm) => {
    setSelectedAlarm(alarm);
    setShowForm(true);
  };

  const handleCloseForm = () => {
    setShowForm(false);
    setSelectedAlarm(null);
  };

  if (isLoading) return (
    <div className="text-center p-4">
      <Spinner animation="border" variant="primary" />
    </div>
  );
  
  if (error) return (
    <div className="alert alert-danger">
      Error: {error.message}
    </div>
  );

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h4 className="mb-0">Alarms</h4>
        <Button variant="primary" onClick={() => setShowForm(true)}>
          New Alarm
        </Button>
      </div>

      <div className="overflow-auto" style={{ maxHeight: 'calc(100vh - 250px)' }}>
        {alarms?.map((alarm) => (
          <div key={alarm.id} className="mb-3">
            <AlarmCard alarm={alarm} onEdit={() => handleEdit(alarm)} />
          </div>
        ))}
      </div>

      <AlarmForm
        show={showForm}
        onHide={handleCloseForm}
        alarm={selectedAlarm}
      />
    </div>
  );
}