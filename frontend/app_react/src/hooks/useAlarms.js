import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { alarmService } from '../services/api';

const ALARMS_QUERY_KEY = ['alarms'];

export function useAlarms() {
  return useQuery({
    queryKey: ALARMS_QUERY_KEY,
    queryFn: alarmService.getAlarms,
    staleTime: 0, // Consider data stale immediately
    cacheTime: 5 * 60 * 1000, // Cache for 5 minutes
  });
}

export function useCreateAlarm(options = {}) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: alarmService.createAlarm,
    onMutate: async (newAlarm) => {
      console.log('New alarm: ', newAlarm);
      // Cancel any outgoing refetches
      await queryClient.cancelQueries(ALARMS_QUERY_KEY);

      // Snapshot the previous value
      const previousAlarms = queryClient.getQueryData(ALARMS_QUERY_KEY);

      // Optimistically update to the new value
      queryClient.setQueryData(ALARMS_QUERY_KEY, (old = []) => [...old, { ...newAlarm, id: Date.now() }]);

      // Return a context object with the snapshotted value
      return { previousAlarms };
    },
    onError: (err, newAlarm, context) => {
      // If the mutation fails, use the context returned from onMutate to roll back
      queryClient.setQueryData(ALARMS_QUERY_KEY, context.previousAlarms);
    },
    onSettled: () => {
      // Always refetch after error or success
      queryClient.invalidateQueries(ALARMS_QUERY_KEY);
      console.log('Alarms refetched');
    },
    ...options,
  });
}

export function useUpdateAlarm(options = {}) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, ...alarmData }) => alarmService.updateAlarm(id, alarmData),
    onMutate: async ({ id, ...updatedAlarm }) => {
      await queryClient.cancelQueries(ALARMS_QUERY_KEY);

      const previousAlarms = queryClient.getQueryData(ALARMS_QUERY_KEY);

      queryClient.setQueryData(ALARMS_QUERY_KEY, (old = []) =>
        old.map((alarm) => (alarm.id === id ? { ...alarm, ...updatedAlarm } : alarm))
      );

      return { previousAlarms };
    },
    onError: (err, variables, context) => {
      queryClient.setQueryData(ALARMS_QUERY_KEY, context.previousAlarms);
    },
    onSettled: () => {
      queryClient.invalidateQueries(ALARMS_QUERY_KEY);
    },
    ...options,
  });
}

export function useDeleteAlarm(options = {}) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: alarmService.deleteAlarm,
    onMutate: async (id) => {
      await queryClient.cancelQueries(ALARMS_QUERY_KEY);

      const previousAlarms = queryClient.getQueryData(ALARMS_QUERY_KEY);

      queryClient.setQueryData(ALARMS_QUERY_KEY, (old = []) =>
        old.filter((alarm) => alarm.id !== id)
      );

      return { previousAlarms };
    },
    onError: (err, id, context) => {
      queryClient.setQueryData(ALARMS_QUERY_KEY, context.previousAlarms);
    },
    onSettled: () => {
      queryClient.invalidateQueries(ALARMS_QUERY_KEY);
    },
    ...options,
  });
}

export function useAlarmStats() {
  return useQuery({
    queryKey: ['alarmStats'],
    queryFn: alarmService.getAlarmStats,
    staleTime: 30000, // Consider data stale after 30 seconds
    refetchInterval: 60000, // Refetch every minute
  });
}