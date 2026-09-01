const { WebSocketServer } = require('ws');

const wss = new WebSocketServer({ port: 8000 });
console.log('Mock telemetry server running on ws://localhost:8000');

wss.on('connection', (socket) => {
  console.log('Frontend connected');
  let count = 0;

  const interval = setInterval(() => {
    count++;

    // every 8th message, send a DECISION_REQUIRED instead of telemetry
    if (count % 8 === 0) {
      socket.send(JSON.stringify({
        type: 'DECISION_REQUIRED',
        data: {
          decisionId: `dec_${count}`,
          triggerType: 'RISK_SCORE_THRESHOLD',
          currentRiskScore: 87,
          prompt: 'Anomalous authentication burst detected on /login from IP 192.168.1.104.',
          options: [
            { id: 'ALLOW', label: 'Allow & Continue' },
            { id: 'THROTTLE', label: 'Rate Limit Session' },
            { id: 'BLOCK', label: 'Block Session IP' },
          ],
          hints: [
            'Observe the relationship between failure rate and frequency.',
            'The request count exceeds standard human threshold (1 req/sec).',
            'Apply a throttle to mitigate brute-force attempts without dropping valid users.',
          ],
        },
      }));
    } else {
      socket.send(JSON.stringify({
        type: 'TELEMETRY',
        data: {
          id: `log_${count}`,
          timestamp: new Date().toLocaleTimeString(),
          sessionId: 'sess_4821',
          endpoint: '/api/v1/auth/login',
          statusCode: [200, 401, 401, 401, 403][Math.floor(Math.random() * 5)],
          ip: '192.168.1.104',
          requestFrequency: Math.floor(Math.random() * 50),
          anomalyFlag: 'HIGH_AUTH_FAILURE',
        },
      }));
    }
  }, 1000);

  socket.on('message', (raw) => {
    console.log('Received from frontend:', raw.toString());
  });

  socket.on('close', () => {
    console.log('Frontend disconnected');
    clearInterval(interval);
  });
});