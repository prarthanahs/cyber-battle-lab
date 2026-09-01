import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from backend.attacker import AIAttacker
from backend.telemetry import TelemetryGenerator
from backend.scoring import PerformanceEvaluator

app = FastAPI()
attacker = AIAttacker()
telemetry_gen = TelemetryGenerator()
evaluator = PerformanceEvaluator()

@app.websocket("/ws/telemetry")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("🔌 Frontend connected to Simulation Engine!")
    
    try:
        while True:
            # Generate and stream log packet
            log = telemetry_gen.generate_packet(attacker.state)
            await websocket.send_text(json.dumps(log))
            
            # Check for incoming messages from frontend (non-blocking pause)
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=0.8)
                payload = json.loads(data)
                
                # Handle Human Defender Decisions
                if payload.get("type") == "DEFENDER_ACTION":
                    action = payload.get("action")
                    print(f"🛡️ Action received from Defender: {action}")
                    attacker.handle_human_defense(action)
                    
                    # Track response time delay for evaluation
                    evaluator.response_delays.append(payload.get("response_time_seconds", 5.0))

                # Handle Progressive Hint Requests
                elif payload.get("type") == "HINT_REQUEST":
                    level = payload.get("level", 1)
                    hint_text = evaluator.request_hint(attacker.state, level)
                    
                    response = {
                        "type": "HINT_RESPONSE",
                        "level": level,
                        "hint_text": hint_text
                    }
                    await websocket.send_text(json.dumps(response))

                # Handle Round Completion / End Game Trigger
                elif payload.get("type") == "END_SIMULATION" or attacker.state == "NEUTRALIZED":
                    score_report = evaluator.calculate_score()
                    report_payload = {
                        "type": "SIMULATION_COMPLETE",
                        "report": score_report
                    }
                    await websocket.send_text(json.dumps(report_payload))
                    
            except asyncio.TimeoutError:
                pass
                
            await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        print("Client disconnected")