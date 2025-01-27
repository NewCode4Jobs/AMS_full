import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { alarmService } from '../services/api';

const ALARMS_QUERY_KEY = ['alarms'];
const FILTERS_QUERY_KEY = ['alarmFilters'];

export function useAlarms() {
  const queryClient = useQueryClient();
  // Get current filters
  const filters = queryClient.getQueryData(FILTERS_QUERY_KEY) || {
    severity: '',
    status: '',
    source: '',
    search: ''
  };

  console.log('Current filters:', filters);

  return useQuery({
    queryKey: [...ALARMS_QUERY_KEY, filters], // Include filters in query key
    queryFn: () => alarmService.getAlarms(),
    select: (alarms) => {
      console.log('Filtering alarms with:', filters);
      return alarms.filter(alarm => {
        const matchesSeverity = !filters.severity || alarm.severity === filters.severity;
        const matchesStatus = !filters.status || alarm.status === filters.status;
        const matchesSource = !filters.source || alarm.source === filters.source;
        const matchesSearch = !filters.search || 
          alarm.name.toLowerCase().includes(filters.search.toLowerCase()) ||
          alarm.description.toLowerCase().includes(filters.search.toLowerCase());

        return matchesSeverity && matchesStatus && matchesSource && matchesSearch;
      });
    }
  });
}

export function useCreateAlarm(options = {}) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: alarmService.createAlarm,
    onMutate: async (newAlarm) => {
      await queryClient.cancelQueries(ALARMS_QUERY_KEY);
      const previousAlarms = queryClient.getQueryData(ALARMS_QUERY_KEY);
      queryClient.setQueryData(ALARMS_QUERY_KEY, (old = []) => [...old, { ...newAlarm, id: Date.now() }]);
      return { previousAlarms };
    },
    onError: (err, newAlarm, context) => {
      queryClient.setQueryData(ALARMS_QUERY_KEY, context.previousAlarms);
    },
    onSettled: () => {
      queryClient.invalidateQueries(ALARMS_QUERY_KEY);
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
    staleTime: 30000,
    refetchInterval: 60000,
  });
}