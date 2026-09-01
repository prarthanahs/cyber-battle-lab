class PerformanceEvaluator:
    def __init__(self):
        self.hints_used = 0
        self.response_delays = []
        
    def request_hint(self, attack_state: str, level: int) -> str:
        self.hints_used += 1
        hints = {
            "BRUTE_FORCE": {
                1: "Observe the timing between consecutive /login failures.",
                2: "Request rate is 38/min with 92% failure. This is auth abuse.",
                3: "Recommendation: Apply a RATE_LIMIT or BLOCK_IP to neutralize session."
            }
        }
        return hints.get(attack_state, {}).get(level, "No further hints available.")
        
    def calculate_score(self) -> dict:
        base_score = 100
        hint_penalty = self.hints_used * 10
        avg_delay = sum(self.response_delays) / max(len(self.response_delays), 1)
        delay_penalty = avg_delay * 1.5
        
        final_score = max(0, int(base_score - hint_penalty - delay_penalty))
        
        return {
            "final_score": final_score,
            "hints_used": self.hints_used,
            "avg_response_time_sec": round(avg_delay, 1),
            "performance_rating": "EXCELLENT" if final_score > 80 else "NEEDS_IMPROVEMENT"
        }