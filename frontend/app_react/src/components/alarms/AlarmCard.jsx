import { format } from 'date-fns';
import { Badge } from '../ui/Badge';

export function AlarmCard({ alarm }) {
  const severityColors = {
    critical: 'bg-alarm-critical',
    high: 'bg-alarm-high',
    medium: 'bg-alarm-medium',
    low: 'bg-alarm-low',
  };

  return (
    <div className="rounded-lg bg-gray-800 p-4 shadow-lg transition-all hover:transform hover:scale-[1.02]">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-white">{alarm.name}</h3>
        <Badge className={severityColors[alarm.severity]}>
          {alarm.severity}
        </Badge>
      </div>
      <p className="mt-2 text-gray-300">{alarm.description}</p>
      <div className="mt-4 flex items-center justify-between text-sm text-gray-400">
        <span>{alarm.source}</span>
        <span>{format(new Date(alarm.timestamp), 'PPp')}</span>
      </div>
    </div>
  );
}