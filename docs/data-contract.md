 # WebSocket Data Contract

## 1. TELEMETRY (server → client)
Streamed continuously into the log table.

\`\`\`json
{
  "type": "TELEMETRY",
  "data": {
    "id": "log_8921",
    "timestamp": "10:32:01.402",
    "sessionId": "sess_4821",
    "endpoint": "/api/v1/auth/login",
    "statusCode": 401,
    "ip": "192.168.1.104",
    "requestFrequency": 42,
    "anomalyFlag": "HIGH_AUTH_FAILURE"
  }
}
\`\`\`

## 2. DECISION_REQUIRED (server → client)
Fires when a risk threshold or attack stage is hit. Pauses the log stream and opens the decision modal.

\`\`\`json
{
  "type": "DECISION_REQUIRED",
  "data": {
    "decisionId": "dec_004",
    "triggerType": "RISK_SCORE_THRESHOLD",
    "currentRiskScore": 87,
    "prompt": "Anomalous authentication burst detected on /login from IP 192.168.1.104.",
    "options": [
      { "id": "ALLOW", "label": "Allow & Continue" },
      { "id": "THROTTLE", "label": "Rate Limit Session" },
      { "id": "BLOCK", "label": "Block Session IP" }
    ],
    "hints": [
      "Observe the relationship between failure rate and frequency.",
      "The request count exceeds standard human threshold (1 req/sec).",
      "Apply a throttle to mitigate brute-force attempts without dropping valid users."
    ]
  }
}
\`\`\`

## 3. SUBMIT_DECISION (client → server)
Sent when the human submits their choice in the decision modal.

\`\`\`json
{
  "action": "SUBMIT_DECISION",
  "decisionId": "dec_004",
  "chosenOption": "THROTTLE",
  "hintsUsedCount": 1
}
\`\`\`