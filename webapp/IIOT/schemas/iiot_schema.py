"""IIOT Sensor Data schemas."""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class IIOTSensorDataBase(BaseModel):
    """Base schema for IIOT Sensor Data."""
    station_id: Optional[int] = Field(None, description="ID of the associated station")
    date: Optional[datetime] = Field(None, description="Date and time of the sensor reading")
    value: Dict[str, Any] = Field(..., description="Sensor data as a dictionary of key-value pairs")


class IIOTSensorDataCreate(IIOTSensorDataBase):
    """Schema for creating IIOT Sensor Data."""
    pass


class IIOTSensorDataUpdate(BaseModel):
    """Schema for updating IIOT Sensor Data."""
    station_id: Optional[int] = Field(None, description="ID of the associated station")
    date: Optional[datetime] = Field(None, description="Date and time of the sensor reading")
    value: Optional[Dict[str, Any]] = Field(None, description="Sensor data as a dictionary of key-value pairs")


class IIOTSensorDataResponse(IIOTSensorDataBase):
    """Schema for IIOT Sensor Data response."""
    id: int
    date: datetime  # Make date required in the response

    class Config:
        """Pydantic config."""
        from_attributes = True
