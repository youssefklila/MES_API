import json
import paho.mqtt.client as mqtt
from datetime import datetime
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

def _json_serialize(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

class MQTTClient:
    def __init__(self, host: str, port: int, keepalive: int, topic: str = None):
        self.client = mqtt.Client()
        self.host = host
        self.port = port
        self.keepalive = keepalive
        self.default_topic = topic  # Store as default_topic instead of topic
        # Store last message per topic
        self.topic_data = {}  # New: {topic: last_payload}
        self.sensor_data = {
            "name": "",
            "value": 0,
            "timestamp": datetime.now().isoformat()
        }
        
        # Setup callbacks
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT broker")
            # Only subscribe if default_topic is provided
            if self.default_topic:
                client.subscribe(self.default_topic)
                logger.info(f"Subscribed to default topic: {self.default_topic}")
        else:
            logger.error(f"Failed to connect to MQTT broker with code {rc}")
        
    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            logger.info(f"Sensor Data Received on topic {msg.topic} - Payload: {payload}")
            # Store last message per topic
            self.topic_data[msg.topic] = payload
            self.publish_to_dashboard()
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding MQTT message: {e}")
            
    def start(self):
        try:
            self.client.connect(self.host, self.port, self.keepalive)
            self.client.loop_start()
            logger.info("MQTT client started successfully")
        except Exception as e:
            logger.warning(f"Failed to start MQTT client: {e}")
            logger.warning("MQTT functionality will be disabled, but the API will continue to work")
            # Don't raise the exception, allow the application to continue
    
    def subscribe(self, topic: Optional[str] = None):
        """Subscribe to a specific topic or use the default topic if none provided"""
        topic_to_use = topic or self.default_topic
        
        if not topic_to_use:
            logger.error("No topic provided for subscription")
            return False
            
        try:
            self.client.subscribe(topic_to_use)
            logger.info(f"Subscribed to topic: {topic_to_use}")
            return True
        except Exception as e:
            logger.error(f"Failed to subscribe to topic {topic_to_use}: {e}")
            return False
    
    def publish(self, payload: Dict[str, Any], topic: Optional[str] = None):
        """Publish a payload to a specific topic or use the default topic if none provided"""
        topic_to_use = topic or self.default_topic
        
        if not topic_to_use:
            logger.error("No topic provided for publishing")
            return False
            
        try:
            self.client.publish(topic_to_use, json.dumps(payload, default=_json_serialize))
            # Ensure topic is set in the payload before storing
            payload_with_topic = payload.copy()
            payload_with_topic["topic"] = topic_to_use
            self.topic_data[topic_to_use] = payload_with_topic
            logger.info(f"Published data to topic: {topic_to_use}")
            return True
        except Exception as e:
            logger.error(f"Failed to publish to topic {topic_to_use}: {e}")
            return False
        
    def get_current_data(self, topic: Optional[str] = None) -> Dict[str, Any]:
        if topic and topic in self.topic_data:
            data = self.topic_data[topic].copy()
            # Ensure the topic field is correct
            data["topic"] = topic
            return data
        elif self.topic_data:
            last_topic = next(reversed(self.topic_data))
            data = self.topic_data[last_topic].copy()
            data["topic"] = last_topic
            return data
        return {}
        
    def publish_to_dashboard(self, custom_topics: Dict[str, str] = None):
        """Publish sensor data to Node-RED dashboard topics
        
        Args:
            custom_topics: Optional dictionary mapping data types to topics
        """
        try:
            topics = custom_topics or {
                "temperature": "sensor/temperature",
                "pressure": "sensor/pressure"
            }
            
            # Publish temperature
            self.client.publish(
                topics.get("temperature", "sensor/temperature"),
                json.dumps({
                    "value": self.sensor_data.get("value", 0),
                    "timestamp": datetime.now().isoformat()
                }, default=_json_serialize)
            )
            
            # Publish pressure
            self.client.publish(
                topics.get("pressure", "sensor/pressure"),
                json.dumps({
                    "value": self.sensor_data.get("value", 0),
                    "timestamp": datetime.now().isoformat()
                }, default=_json_serialize)
            )
            
            logger.debug("Published sensor data to dashboard topics")
        except Exception as e:
            logger.warning(f"Failed to publish to dashboard: {e}")
            # Don't raise the exception, just log it