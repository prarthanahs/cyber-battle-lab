import { useEffect, useRef } from 'react';
import { useSimulationStore } from '../store/simulationStore';
import type { SocketMessage } from '../types/telemetry';

export function useTelemetrySocket(url: string) {
  const socketRef = useRef<WebSocket | null>(null);
  const handleIncomingMessage = useSimulationStore((s) => s.handleIncomingMessage);

  useEffect(() => {
    const ws = new WebSocket(url);
    socketRef.current = ws;

    ws.onmessage = (event) => {
      const msg: SocketMessage = JSON.parse(event.data);
      handleIncomingMessage(msg);
    };

    ws.onopen = () => console.log('Connected to telemetry socket');
    ws.onclose = () => console.log('WebSocket closed');
    ws.onerror = (e) => console.error('WebSocket error', e);

    return () => ws.close();
  }, [url, handleIncomingMessage]);

  const sendAction = (decisionId: string, chosenOption: string, hintsUsedCount: number) => {
    socketRef.current?.send(
      JSON.stringify({ action: 'SUBMIT_DECISION', decisionId, chosenOption, hintsUsedCount })
    );
  };

  return { sendAction };
}