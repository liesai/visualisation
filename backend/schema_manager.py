import os
import json
from typing import Optional, Dict

class SchemaManager:
    def __init__(self, schema_dir: str = "schemas"):
        self.schema_dir = schema_dir
        self.schemas: Dict[str, dict] = {}
        self._ensure_schema_dir()
    
    def _ensure_schema_dir(self):
        """Ensure the schema directory exists"""
        if not os.path.exists(self.schema_dir):
            os.makedirs(self.schema_dir)
    
    def save_schema(self, topic: str, schema_content: str) -> bool:
        """Save a schema file for a topic"""
        try:
            # Validate JSON schema
            schema = json.loads(schema_content)
            
            # Save schema file
            schema_path = os.path.join(self.schema_dir, f"{topic}_schema.json")
            with open(schema_path, 'w') as f:
                json.dump(schema, f, indent=2)
            
            # Cache schema
            self.schemas[topic] = schema
            return True
        except Exception as e:
            print(f"Error saving schema for topic {topic}: {e}")
            return False
    
    def get_schema(self, topic: str) -> Optional[dict]:
        """Get schema for a topic"""
        if topic in self.schemas:
            return self.schemas[topic]
        
        schema_path = os.path.join(self.schema_dir, f"{topic}_schema.json")
        if os.path.exists(schema_path):
            try:
                with open(schema_path, 'r') as f:
                    schema = json.load(f)
                self.schemas[topic] = schema
                return schema
            except Exception as e:
                print(f"Error loading schema for topic {topic}: {e}")
        return None