import threading
from typing import Optional
from confluent_kafka import Consumer, KafkaException
from flask_socketio import SocketIO
from .topic_manager import TopicManager
from .schema_manager import SchemaManager
from .message_deserializer import MessageDeserializer
from .metrics_manager import MetricsManager
from config import Config

class KafkaClient:
    def __init__(self, 
                 socketio: SocketIO, 
                 topic_manager: TopicManager,
                 schema_manager: SchemaManager):
        self.socketio = socketio
        self.topic_manager = topic_manager
        self.schema_manager = schema_manager
        self.metrics_manager = MetricsManager()
        self.consumer: Optional[Consumer] = None
        self.running = False
        self.stop_event = threading.Event()

    def start(self):
        """Start the Kafka client threads"""
        self.running = True
        self.consumer_thread = threading.Thread(target=self._consume_messages, daemon=True)
        self.metrics_thread = threading.Thread(target=self._emit_metrics, daemon=True)
        self.consumer_thread.start()
        self.metrics_thread.start()

    def _create_consumer(self):
        """Create a Kafka consumer with the configured settings"""
        conf = {
            'bootstrap.servers': Config.KAFKA_BOOTSTRAP_SERVERS,
            'group.id': 'kafka_dashboard',
            'auto.offset.reset': 'earliest',
        }
        
        if hasattr(Config, 'KAFKA_API_KEY') and hasattr(Config, 'KAFKA_API_SECRET'):
            conf.update({
                'security.protocol': 'SASL_SSL',
                'sasl.mechanism': 'PLAIN',
                'sasl.username': Config.KAFKA_API_KEY,
                'sasl.password': Config.KAFKA_API_SECRET,
            })

        return Consumer(conf)

    def _consume_messages(self):
        """Consume messages from Kafka topics"""
        try:
            self.consumer = self._create_consumer()
            
            while not self.stop_event.is_set():
                # Update subscribed topics
                current_topics = [topic.name for topic in self.topic_manager.get_all_topics()]
                if current_topics:
                    self.consumer.subscribe(current_topics)
                
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaException._PARTITION_EOF:
                        continue
                    print(f"Kafka error: {msg.error()}")
                    continue

                try:
                    topic_config = self.topic_manager.get_topic_config(msg.topic())
                    if not topic_config:
                        continue

                    # Get schema if needed
                    schema = None
                    if topic_config.format == 'AVRO':
                        schema = self.schema_manager.get_schema(topic_config.name)

                    # Deserialize message
                    value = MessageDeserializer.deserialize_message(
                        msg.value(),
                        topic_config.format,
                        schema
                    )

                    # Update metrics
                    metrics = self.metrics_manager.update_metrics(
                        msg.topic(),
                        len(msg.value())
                    )

                    # Emit message and updated metrics
                    self.socketio.emit('kafka_message', {
                        'topic': msg.topic(),
                        'value': value,
                        'metrics': metrics
                    })

                except Exception as e:
                    print(f"Error processing message: {e}")

        except Exception as e:
            print(f"Consumer error: {e}")
        finally:
            if self.consumer:
                self.consumer.close()

    def _emit_metrics(self):
        """Emit metrics periodically"""
        while not self.stop_event.is_set():
            metrics = self.metrics_manager.get_metrics()
            if metrics:
                self.socketio.emit('metrics', metrics)
            threading.Event().wait(1.0)

    def stop(self):
        """Stop the Kafka client"""
        self.running = False
        self.stop_event.set()
        if self.consumer:
            self.consumer.close()