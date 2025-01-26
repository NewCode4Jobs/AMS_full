// src/components/layout/Header.jsx
import { Button } from 'react-bootstrap';

export default function Header({ onMenuClick }) {
  return (
    <header className="bg-white border-bottom shadow-sm">
      <div className="container-fluid">
        <div className="d-flex justify-content-between align-items-center py-3">
          <div className="d-flex align-items-center">
            <Button
              variant="link"
              className="text-dark p-0 me-3"
              onClick={onMenuClick}
            >
              <i className="bi bi-list fs-4"></i>
            </Button>
            <h5 className="mb-0">Alarm Management System</h5>
          </div>
          
          <div className="d-flex align-items-center">
            <Button variant="outline-primary" size="sm" className="me-2">
              <i className="bi bi-bell"></i>
            </Button>
            <Button variant="outline-primary" size="sm">
              <i className="bi bi-gear"></i>
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
}