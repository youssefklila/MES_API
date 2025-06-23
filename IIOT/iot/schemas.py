from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

class SensorData(BaseModel):
    station_id: int
    date: datetime
    value: Dict[str, Any]
    topic: Optional[str] = None  # Make topic optional with None as default
    # Add more fields as needed
    
class SensorDataResponse(SensorData):
    timestamp: str  # Example of extended response model