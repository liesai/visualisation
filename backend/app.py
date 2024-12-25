from flask import Flask
from flask_socketio import SocketIO
from kafka_client import KafkaClient
from config import Config
from topic_manager import TopicManager
from schema_manager import SchemaManager
from socket_handlers import KafkaNamespace
from api import api

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app, cors_allowed_origins="*")

# Register API blueprint
app.register_blueprint(api)

# Initialize managers
topic_manager = TopicManager()
schema_manager = SchemaManager()

# Initialize Kafka client with managers
kafka_client = KafkaClient(socketio, topic_manager, schema_manager)

# Register socket namespace
socketio.on_namespace(KafkaNamespace(topic_manager, schema_manager))

@app.route('/health')
def health_check():
    return {'status': 'healthy'}

if __name__ == '__main__':
    kafka_client.start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)