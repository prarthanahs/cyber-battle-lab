import random

class AIAttacker:
    def __init__(self):
        self.state = "RECON"
        self.attempts = 0
        self.ip = "192.168.1.104"

    def execute_step(self):
        """Advances the attacker state machine."""
        self.attempts += 1

        if self.state == "RECON":
            if self.attempts >= 3:
                self.state = "BRUTE_FORCE"
                self.attempts = 0

            return {
                "endpoint": random.choice(["/api/v1/health", "/api/v1/login"]),
                "statusCode": 200 if random.random() > 0.3 else 401,
                "frequency": random.randint(1, 3),
                "anomaly": "NORMAL"
            }

        elif self.state == "BRUTE_FORCE":
            return {
                "endpoint": "/api/v1/login",
                "statusCode": 401,
                "frequency": random.randint(35, 60),
                "anomaly": "HIGH_AUTH_FAILURE_RATE"
            }

        return {}

    def apply_mitigation(self, decision: str):
        """Responds to defender actions."""
        if decision in ["THROTTLE", "BLOCK"]:
            self.state = "RECON"
            self.attempts = 0
            return True
        return False