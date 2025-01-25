// src/hooks/useAlarmSocket.js
import { useEffect } from 'react';
import { useQueryClient } from '@tanstack/react-query';

export function useAlarmSocket() {
  const queryClient = useQueryClient();

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');

    ws.onmessage = (event) => {
      const alarm = JSON.parse(event.data);
      queryClient.invalidateQueries(['alarms']);
    };

    return () => ws.close();
  }, [queryClient]);
}