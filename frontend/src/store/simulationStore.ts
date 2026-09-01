import { create } from 'zustand';
import type { TelemetryLog, DecisionPayload, SocketMessage } from '../types/telemetry';

interface SimulationStore {
  logs: TelemetryLog[];
  isPaused: boolean;
  activeDecision: DecisionPayload | null;
  hintsUsedCount: number;
  handleIncomingMessage: (msg: SocketMessage) => void;
  revealHint: () => void;
  resetHints: () => void;
  resolveDecision: () => void;
}

export const useSimulationStore = create<SimulationStore>((set, get) => ({
  logs: [],
  isPaused: false,
  activeDecision: null,
  hintsUsedCount: 0,

  handleIncomingMessage: (msg) => {
    if (msg.type === 'TELEMETRY') {
      if (get().isPaused) return;
      set((state) => ({ logs: [msg.data, ...state.logs].slice(0, 100) }));
    } else if (msg.type === 'DECISION_REQUIRED') {
      set({ isPaused: true, activeDecision: msg.data });
    }
  },

  revealHint: () => set((state) => ({ hintsUsedCount: state.hintsUsedCount + 1 })),
  resetHints: () => set({ hintsUsedCount: 0 }),
  

// inside the create(...) object, alongside your other actions
resolveDecision: () => set({ isPaused: false, activeDecision: null }),
}));