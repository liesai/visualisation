import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    KAFKA_TOPICS = os.getenv('KAFKA_TOPICS', 'test').split(',')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key')