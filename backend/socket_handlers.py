from flask_socketio import Namespace, emit
from topic_manager import TopicManager
from schema_manager import SchemaManager
import base64

class KafkaNamespace(Namespace):
    def __init__(self, topic_manager: TopicManager, schema_manager: SchemaManager):
        super().__init__('/kafka')
        self.topic_manager = topic_manager
        self.schema_manager = schema_manager
    
    def on_update_topics(self, data):
        """Handle topic configuration updates"""
        try:
            topics = data.get('topics', [])
            for topic in topics:
                name = topic.get('name')
                format = topic.get('format', 'JSON')
                schema_file = topic.get('schemaFile')
                
                if schema_file and format == 'AVRO':
                    # Extract and save schema content
                    schema_content = base64.b64decode(schema_file['content']).decode('utf-8')
                    self.schema_manager.save_schema(name, schema_content)
                    schema = self.schema_manager.get_schema(name)
                else:
                    schema = None
                
                self.topic_manager.add_topic(name, format, schema)
            
            emit('topics_updated', {'status': 'success'})
        except Exception as e:
            print(f"Error updating topics: {e}")
            emit('topics_updated', {'status': 'error', 'message': str(e)})