// src/components/alarms/AlarmStats.jsx
import { ChartBarIcon } from '@heroicons/react/solid';

export function AlarmStats() {
  const stats = [
    { 
      name: 'Total Alarms', 
      value: 42, 
      color: 'text-blue-500' 
    },
    { 
      name: 'Critical Alarms', 
      value: 5, 
      color: 'text-red-500' 
    },
    { 
      name: 'Unacknowledged', 
      value: 12, 
      color: 'text-yellow-500' 
    }
  ];

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
      {stats.map((stat) => (
        <div 
          key={stat.name} 
          className="bg-gray-800 rounded-lg p-4 flex items-center justify-between"
        >
          <div>
            <p className="text-sm font-medium text-gray-400">{stat.name}</p>
            <p className={`text-3xl font-bold ${stat.color}`}>{stat.value}</p>
          </div>
          <ChartBarIcon className={`h-8 w-8 ${stat.color} opacity-50`} />
        </div>
      ))}
    </div>
  );
}