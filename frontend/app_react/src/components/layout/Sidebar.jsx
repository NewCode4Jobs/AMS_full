// src/components/layout/Sidebar.jsx
import { Nav } from 'react-bootstrap';

const navigation = [
  { name: 'Dashboard', icon: 'bi-speedometer2', href: '#' },
  { name: 'Alarms', icon: 'bi-bell', href: '#', current: true },
  { name: 'Reports', icon: 'bi-file-text', href: '#' },
  { name: 'Settings', icon: 'bi-gear', href: '#' },
];

export default function Sidebar({ open, onClose }) {
  return (
    <aside
      className={`bg-white border-end position-fixed h-100 transition-transform ${
        open ? 'translate-x-0' : '-translate-x-100'
      }`}
      style={{ width: '16rem', top: '0', zIndex: 1000 }}
    >
      <div className="d-flex flex-column h-100">
        {/* Logo */}
        <div className="p-4 border-bottom">
          <h4 className="mb-0">AMS</h4>
        </div>

        {/* Navigation */}
        <Nav className="flex-column p-3">
          {navigation.map((item) => (
            <Nav.Link
              key={item.name}
              href={item.href}
              className={`mb-2 ${item.current ? 'active' : ''}`}
            >
              <div className="d-flex align-items-center">
                <i className={`${item.icon} me-2`}></i>
                {item.name}
              </div>
            </Nav.Link>
          ))}
        </Nav>

        {/* User Profile */}
        <div className="mt-auto p-3 border-top">
          <div className="d-flex align-items-center">
            <div className="rounded-circle bg-primary text-white p-2 me-2">
              <i className="bi bi-person"></i>
            </div>
            <div>
              <div className="fw-bold">John Doe</div>
              <small className="text-muted">Administrator</small>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
}