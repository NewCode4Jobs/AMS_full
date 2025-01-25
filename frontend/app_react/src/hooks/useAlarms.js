import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { alarmService } from '../services/api';

export function useAlarms() {
  return useQuery({
    queryKey: ['alarms'],
    queryFn: alarmService.getAlarms,
  });
}

export function useCreateAlarm() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: alarmService.createAlarm,
    onSuccess: () => {
      queryClient.invalidateQueries(['alarms']);
    },
  });
}

export function useUpdateAlarm() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, alarm }) => alarmService.updateAlarm(id, alarm),
    onSuccess: () => {
      queryClient.invalidateQueries(['alarms']);
    },
  });
}