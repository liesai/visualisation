from typing import Any, Optional
from io import BytesIO
import json
from fastavro import schemaless_reader

class MessageDeserializer:
    @staticmethod
    def deserialize_message(message: bytes, format: str, schema: Optional[dict] = None) -> Any:
        """Deserialize a message based on its format and schema"""
        if format == 'AVRO':
            return MessageDeserializer._deserialize_avro(message, schema)
        return MessageDeserializer._deserialize_json(message)

    @staticmethod
    def _deserialize_avro(message: bytes, schema: Optional[dict]) -> Any:
        """Deserialize an Avro message"""
        if not schema:
            raise ValueError("Schema is required for Avro deserialization")
        
        try:
            # Skip the first 5 bytes (magic byte + schema ID) if present
            if message[0] == 0:
                data = message[5:]
            else:
                data = message
            
            bytes_io = BytesIO(data)
            return schemaless_reader(bytes_io, schema)
        except Exception as e:
            raise ValueError(f"Error deserializing Avro message: {e}")

    @staticmethod
    def _deserialize_json(message: bytes) -> Any:
        """Deserialize a JSON message"""
        try:
            return json.loads(message.decode('utf-8'))
        except Exception as e:
            raise ValueError(f"Error deserializing JSON message: {e}")