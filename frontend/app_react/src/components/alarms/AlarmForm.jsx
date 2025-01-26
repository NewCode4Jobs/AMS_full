import { useState, useEffect } from 'react';
import { Form, Button, Modal } from 'react-bootstrap';
import { useCreateAlarm, useUpdateAlarm } from '../../hooks/useAlarms';
import toast from 'react-hot-toast';

const initialFormState = {
  name: '',
  description: '',
  severity: 'low',
  source: 'system',
  status: 'active'
};

export function AlarmForm({ show, onHide, alarm = null }) {
  const [formData, setFormData] = useState(initialFormState);

  // Reset form when modal opens/closes or alarm changes
  useEffect(() => {
    if (alarm) {
      setFormData({
        name: alarm.name,
        description: alarm.description,
        severity: alarm.severity,
        source: alarm.source,
        status: alarm.status
      });
    } else {
      setFormData(initialFormState);
    }
  }, [alarm, show]);

  const { mutate: createAlarm, isLoading: isCreating } = useCreateAlarm({
    onSuccess: () => {
      toast.success('Alarm created successfully');
      setFormData(initialFormState);
      onHide();
    },
    onError: (error) => {
      toast.error(`Error creating alarm: ${error.message}`);
    }
  });

  const { mutate: updateAlarm, isLoading: isUpdating } = useUpdateAlarm({
    onSuccess: () => {
      toast.success('Alarm updated successfully');
      onHide();
    },
    onError: (error) => {
      toast.error(`Error updating alarm: ${error.message}`);
    }
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (alarm) {
      updateAlarm({ id: alarm.id, ...formData });
    } else {
      createAlarm(formData);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <Modal show={show} onHide={onHide} centered backdrop="static">
      <Modal.Header closeButton className="text-white">
        <Modal.Title>{alarm ? 'Edit Alarm' : 'Create New Alarm'}</Modal.Title>
      </Modal.Header>
      <Modal.Body className="bg-dark text-white">
        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-3">
            <Form.Label>Name</Form.Label>
            <Form.Control
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              className="bg-dark text-white"
            />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Description</Form.Label>
            <Form.Control
              as="textarea"
              name="description"
              value={formData.description}
              onChange={handleChange}
              required
              className="bg-dark text-white"
            />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Severity</Form.Label>
            <Form.Select
              name="severity"
              value={formData.severity}
              onChange={handleChange}
              required
              className="bg-dark text-white"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="critical">Critical</option>
            </Form.Select>
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Source</Form.Label>
            <Form.Select
              name="source"
              value={formData.source}
              onChange={handleChange}
              required
              className="bg-dark text-white"
            >
              <option value="system">System</option>
              <option value="application">Application</option>
              <option value="security">Security</option>
            </Form.Select>
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Status</Form.Label>
            <Form.Select
              name="status"
              value={formData.status}
              onChange={handleChange}
              required
              className="bg-dark text-white"
            >
              <option value="active">Active</option>
              <option value="acknowledged">Acknowledged</option>
              <option value="resolved">Resolved</option>
            </Form.Select>
          </Form.Group>

          <div className="d-flex justify-content-end gap-2">
            <Button variant="secondary" onClick={onHide}>
              Cancel
            </Button>
            <Button
              variant="primary"
              type="submit"
              disabled={isCreating || isUpdating}
            >
              {isCreating || isUpdating ? 'Saving...' : (alarm ? 'Update' : 'Create')}
            </Button>
          </div>
        </Form>
      </Modal.Body>
    </Modal>
  );
}
