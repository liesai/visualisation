from datetime import datetime
from typing import Dict, Any

class MetricsManager:
    def __init__(self):
        self.metrics: Dict[str, Dict[str, Any]] = {}

    def update_metrics(self, topic: str, message_size: int) -> Dict[str, Any]:
        """Update metrics for a topic"""
        if topic not in self.metrics:
            self.metrics[topic] = {
                'messageCount': 0,
                'bytesProcessed': 0,
                'lastUpdate': datetime.now().isoformat()
            }

        self.metrics[topic]['messageCount'] += 1
        self.metrics[topic]['bytesProcessed'] += message_size
        self.metrics[topic]['lastUpdate'] = datetime.now().isoformat()

        return self.metrics[topic]

    def get_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Get all metrics"""
        return self.metrics