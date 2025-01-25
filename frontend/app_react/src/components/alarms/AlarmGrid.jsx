import { useAlarms } from '../../hooks/useAlarms';
import { AlarmCard } from './AlarmCard';

export function AlarmGrid() {
  const { data: alarms, isLoading, error } = useAlarms();

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
      {alarms?.map((alarm) => (
        <AlarmCard key={alarm.id} alarm={alarm} />
      ))}
    </div>
  );
}