import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID', 'test')
    KAFKA_API_KEY = os.getenv('KAFKA_API_KEY', 'test')
    KAFKA_API_SECRET = os.getenv('KAFKA_API_SECRET', 'test')
    KAFKA_TOPICS = os.getenv('KAFKA_TOPICS', 'test').split(',')
    SCHEMA_REGISTRY_URL="https://psrc-42jp1.westus2.azure.confluent.cloud/"
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/kafka_dashboard')