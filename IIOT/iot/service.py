# IIOT/iot/service.py
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class IoTService:
    def __init__(self, mqtt_client):
        logger.debug("Initializing IoTService")
        self.mqtt_client = mqtt_client
        
    def get_sensor_data(self, topic: Optional[str] = None) -> Dict[str, Any]:
        """Get current sensor data
        
        Args:
            topic: Optional topic to subscribe to before getting data
            
        Returns:
            Dictionary containing the current sensor data
        """
        logger.debug(f"Getting sensor data{' from topic ' + topic if topic else ''}")
        
        # If a topic is provided, subscribe to it first
        if topic:
            self.mqtt_client.subscribe(topic)
            
        data = self.mqtt_client.get_current_data(topic)
        # Add timestamp if not present
        if data and "timestamp" not in data:
            data["timestamp"] = datetime.now().isoformat()
        return data
        
    def process_sensor_data(self, data: Dict[str, Any], topic: Optional[str] = None) -> Dict[str, Any]:
        """Process and publish sensor data
        
        Args:
            data: Sensor data to process and publish
            topic: Optional topic to publish to
            
        Returns:
            Dictionary containing the processed sensor data
        """
        logger.debug(f"Processing sensor data: {data}{' for topic ' + topic if topic else ''}")
        # Add timestamp to the data
        data["timestamp"] = datetime.now().isoformat()
        
        # Process the data
        processed = {
            **data,
            "processed": True,
            "timestamp": data["timestamp"]
        }
        
        # Update the MQTT client's sensor data
        self.mqtt_client.sensor_data.update(processed)
        
        # Publish the processed data
        if topic:
            self.mqtt_client.publish(processed, topic)
        else:
            # Use the publish_to_dashboard method for backward compatibility
            self.mqtt_client.publish_to_dashboard()
        
        return processed