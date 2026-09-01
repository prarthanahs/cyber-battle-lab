export interface TelemetryLog {
  id: string;
  timestamp: string;
  sessionId: string;
  endpoint: string;
  statusCode: number;
  ip: string;
  requestFrequency: number;
  anomalyFlag?: string;
}

export interface DecisionOption {
  id: string;
  label: string;
}

export interface DecisionPayload {
  decisionId: string;
  triggerType: string;
  currentRiskScore: number;
  prompt: string;
  options: DecisionOption[];
  hints: string[];
}

export type SocketMessage =
  | { type: "TELEMETRY"; data: TelemetryLog }
  | { type: "DECISION_REQUIRED"; data: DecisionPayload };