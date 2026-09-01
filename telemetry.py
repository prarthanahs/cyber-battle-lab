import time

class TelemetryGenerator:
    @staticmethod
    def create_log(log_id: str, endpoint: str, status_code: int, ip: str, frequency: int, anomaly_flag: str):
        return {
            "type": "TELEMETRY",
            "data": {
                "id": log_id,
                "timestamp": time.strftime("%H:%M:%S"),
                "endpoint": endpoint,
                "statusCode": status_code,
                "ip": ip,
                "requestFrequency": frequency,
                "anomalyFlag": anomaly_flag
            }
        }