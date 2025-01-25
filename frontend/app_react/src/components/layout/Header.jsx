// src/components/layout/Header.jsx
import { useState } from 'react';

export default function Header({ onMenuClick }) {
  const [notifications, setNotifications] = useState(3);

  return (
    <header className="sticky top-0 z-40 flex h-16 shrink-0 items-center gap-x-4 border-b border-gray-700 bg-gray-800 px-4 shadow-sm sm:gap-x-6 sm:px-6 lg:px-8">
      <button
        type="button"
        className="-m-2.5 p-2.5 text-gray-400 lg:hidden"
        onClick={onMenuClick}
      >
        <span className="sr-only">Open sidebar</span>
      </button>

      <div className="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
        <div className="relative flex flex-1"></div>
        
        <div className="flex items-center gap-x-4 lg:gap-x-6">
          <button 
            type="button" 
            className="relative -m-2.5 p-2.5 text-gray-400 hover:text-gray-300"
          >
            <span className="sr-only">View notifications</span>
            {notifications > 0 && (
              <span className="absolute -top-1 -right-1 bg-red-600 text-white rounded-full px-1.5 py-0.5 text-xs">
                {notifications}
              </span>
            )}
          </button>
        </div>
      </div>
    </header>
  );
}