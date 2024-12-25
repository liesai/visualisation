from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from sqlalchemy.orm import Session
from models import Topic, SessionLocal

@dataclass
class TopicConfig:
    name: str
    format: str
    schema: Optional[dict] = None

class TopicManager:
    def __init__(self):
        self.topics: Dict[str, TopicConfig] = {}
        self._load_topics()
    
    def _load_topics(self):
        """Load topics from database"""
        with SessionLocal() as db:
            db_topics = db.query(Topic).all()
            self.topics = {
                topic.name: TopicConfig(
                    name=topic.name,
                    format=topic.format,
                    schema=topic.schema
                )
                for topic in db_topics
            }
    
    def add_topic(self, name: str, format: str, schema: Optional[dict] = None) -> bool:
        """Add or update a topic configuration"""
        try:
            with SessionLocal() as db:
                db_topic = Topic(
                    name=name,
                    format=format,
                    schema=schema,
                    updated_at=datetime.utcnow()
                )
                db.merge(db_topic)
                db.commit()
            
            self.topics[name] = TopicConfig(name=name, format=format, schema=schema)
            return True
        except Exception as e:
            print(f"Error adding topic {name}: {e}")
            return False
    
    def remove_topic(self, name: str) -> bool:
        """Remove a topic configuration"""
        try:
            with SessionLocal() as db:
                db_topic = db.query(Topic).filter(Topic.name == name).first()
                if db_topic:
                    db.delete(db_topic)
                    db.commit()
            
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