from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class TopicConfig:
    name: str
    format: str
    schema: Optional[dict] = None

class TopicManager:
    def __init__(self):
        self.topics: Dict[str, TopicConfig] = {}
    
    def add_topic(self, name: str, format: str, schema: Optional[dict] = None) -> bool:
        """Add or update a topic configuration"""
        try:
            self.topics[name] = TopicConfig(name=name, format=format, schema=schema)
            return True
        except Exception as e:
            print(f"Error adding topic {name}: {e}")
            return False
    
    def remove_topic(self, name: str) -> bool:
        """Remove a topic configuration"""
        try:
            if name in self.topics:
                del self.topics[name]
            return True
        except Exception as e:
            print(f"Error removing topic {name}: {e}")
            return False
    
    def get_topic_config(self, name: str) -> Optional[TopicConfig]:
        """Get configuration for a specific topic"""
        return self.topics.get(name)
    
    def get_all_topics(self) -> List[TopicConfig]:
        """Get all topic configurations"""
        return list(self.topics.values())