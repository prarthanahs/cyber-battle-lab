from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import json

from backend.attacker import AIAttacker
from backend.telemetry import TelemetryGenerator

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Cyber Battle Lab Engine Running"}

@app.websocket("/ws/telemetry")
async def simulation_websocket(websocket: WebSocket):
    await websocket.accept()
    attacker = AIAttacker()
    log_counter = 1000

    print("🔌 Frontend connected to Simulation Engine!")

    try:
        while True:
            log_counter += 1
            step_data = attacker.execute_step()

            log_payload = TelemetryGenerator.create_log(
                log_id=f"log_{log_counter}",
                endpoint=step_data["endpoint"],
                status_code=step_data["statusCode"],
                ip=attacker.ip,
                frequency=step_data["frequency"],
                anomaly_flag=step_data["anomaly"]
            )

            # 1. Send live telemetry log
            await websocket.send_text(json.dumps(log_payload))

            # 2. Trigger Decision Interrupt when state threshold is reached
            if attacker.state == "BRUTE_FORCE" and attacker.attempts == 4:
                interrupt_payload = {
                    "type": "DECISION_REQUIRED",
                    "data": {
                        "decisionId": f"dec_{log_counter}",
                        "prompt": f"Anomalous authentication burst detected on /login from IP {attacker.ip}.",
                        "metrics": {
                            "requestFrequency": f"{step_data['frequency']} req/sec",
                            "failedRate": "92%"
                        },
                        "options": [
                            {"id": "ALLOW", "label": "Allow & Continue Monitoring"},
                            {"id": "THROTTLE", "label": "Rate Limit Session (Throttle)"},
                            {"id": "BLOCK", "label": "Block IP Address"}
                        ],
                        "hints": [
                            "Observe the relationship between failure rate and frequency.",
                            "The request count exceeds standard human threshold (1 req/sec).",
                            "Throttling slows down brute-force scripts while keeping systems accessible."
                        ]
                    }
                }
                await websocket.send_text(json.dumps(interrupt_payload))

                # 3. Pause and wait for defender choice from frontend
                raw_response = await websocket.receive_text()
                action_data = json.loads(raw_response)

                print(f"🛡️ Defender Action Received: {action_data.get('chosenOption')}")

                attacker.apply_mitigation(action_data.get("chosenOption"))

            await asyncio.sleep(1)

    except WebSocketDisconnect:
        print("❌ Frontend disconnected.")