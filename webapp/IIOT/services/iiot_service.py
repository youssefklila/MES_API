"""IIOT Sensor Data service."""
from typing import List, Dict, Any, Optional
from datetime import datetime
from fastapi import HTTPException

from webapp.IIOT.repositories.iiot_repository import IIOTSensorDataRepository
from webapp.IIOT.schemas.iiot_schema import IIOTSensorDataResponse


class IIOTSensorDataService:
    """Service for IIOT Sensor Data operations."""

    def __init__(self, iiot_repository: IIOTSensorDataRepository):
        """Initialize service with repository."""
        self.iiot_repository = iiot_repository

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all IIOT sensor data."""
        return self.iiot_repository.get_all()

    def get_by_id(self, sensor_data_id: int) -> Dict[str, Any]:
        """Get IIOT sensor data by ID."""
        sensor_data = self.iiot_repository.get_by_id(sensor_data_id)
        if not sensor_data:
            raise HTTPException(status_code=404, detail="IIOT sensor data not found")
        return sensor_data
        
    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get all IIOT sensor data within a date range.
        
        Args:
            start_date: Start date of the range (inclusive)
            end_date: End date of the range (inclusive)
            
        Returns:
            List of sensor data dictionaries
        """
        return self.iiot_repository.get_by_date_range(start_date, end_date)

    def create_sensor_data(self, value: Dict[str, Any], date: Optional[datetime] = None, station_id: Optional[int] = None) -> Dict[str, Any]:
        """Create new IIOT sensor data."""
        return self.iiot_repository.add(value=value, date=date, station_id=station_id)

    def update_sensor_data(self, sensor_data_id: int, **kwargs) -> Dict[str, Any]:
        """Update IIOT sensor data."""
        sensor_data = self.iiot_repository.update(sensor_data_id, **kwargs)
        if not sensor_data:
            raise HTTPException(status_code=404, detail="IIOT sensor data not found")
        return sensor_data

    def delete_sensor_data(self, sensor_data_id: int) -> bool:
        """Delete IIOT sensor data."""
        success = self.iiot_repository.delete(sensor_data_id)
        if not success:
            raise HTTPException(status_code=404, detail="IIOT sensor data not found")
        return True
