import { useState } from 'react';
import Header from './Header';
import Sidebar from './Sidebar';

export default function Layout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="d-flex flex-column flex-grow-1">
      {/* Header */}
      <Header onMenuClick={() => setSidebarOpen(true)} />

      {/* Main content area */}
      <div className="d-flex flex-grow-1 position-relative">
        {/* Sidebar */}
        <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />

        {/* Main content */}
        <main 
          className="flex-grow-1 p-4 overflow-auto"
          style={{ 
            marginLeft: sidebarOpen ? '16rem' : '0',
            transition: 'margin-left 0.3s ease-in-out'
          }}
        >
          {children}
        </main>
      </div>
    </div>
  );
}