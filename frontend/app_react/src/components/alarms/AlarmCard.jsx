import { format } from 'date-fns';
import { Card, Badge, Button } from 'react-bootstrap';

export function AlarmCard({ alarm, onEdit }) {
  const severityVariants = {
    critical: 'danger',
    high: 'warning',
    medium: 'info',
    low: 'success',
  };

  return (
    <Card bg="white" text="white" className="h-100">
      <Card.Body>
        <div className="d-flex justify-content-between align-items-start">
          <div>
            <Card.Title>{alarm.name}</Card.Title>
            <Badge bg={severityVariants[alarm.severity]} className="me-2">
              {alarm.severity}
            </Badge>
            <Badge bg="secondary">{alarm.status}</Badge>
          </div>
          <Button
            variant="outline-light"
            size="sm"
            onClick={() => onEdit(alarm)}
          >
            Edit
          </Button>
        </div>
        <Card.Text className="text-muted mt-2">
          {alarm.description}
        </Card.Text>
        <div className="d-flex justify-content-between align-items-center mt-3">
          <small className="text-muted">{alarm.source}</small>
          <small className="text-muted">
            {format(new Date(alarm.timestamp), 'PPp')}
          </small>
        </div>
      </Card.Body>
    </Card>
  );
}