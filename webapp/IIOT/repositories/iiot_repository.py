"""IIOT Sensor Data repository."""
from contextlib import AbstractContextManager
from sqlalchemy.orm import Session
from typing import Callable, List, Dict, Any, Optional
from datetime import datetime

from webapp.IIOT.models.iiot_model import IIOTSensorData
from webapp.ADM.machine_assets.machine_setup.station.models.station_model import Station  # Correct import path for Station model


class IIOTSensorDataRepository:
    """Repository for IIOT Sensor Data operations."""

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        """Initialize repository with session factory."""
        self.session_factory = session_factory
    
    def _to_dict(self, sensor_data: IIOTSensorData) -> Dict[str, Any]:
        """Convert IIOTSensorData model to dictionary."""
        return {
            "id": sensor_data.id,
            "station_id": sensor_data.station_id,
            "date": sensor_data.date,
            "value": sensor_data.value
        }

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all IIOT sensor data."""
        with self.session_factory() as session:
            sensor_data_list = session.query(IIOTSensorData).all()
            # Only return rows where value is a dictionary
            result = []
            for sensor_data in sensor_data_list:
                data = self._to_dict(sensor_data)
                if isinstance(data.get("value"), dict):
                    result.append(data)
                else:
                    # Optionally log or collect invalid rows
                    pass
            return result

    def get_by_id(self, sensor_data_id: int) -> Optional[Dict[str, Any]]:
        """Get IIOT sensor data by ID."""
        with self.session_factory() as session:
            sensor_data = session.query(IIOTSensorData).filter(IIOTSensorData.id == sensor_data_id).first()
            if sensor_data:
                return self._to_dict(sensor_data)
            return None

    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get all IIOT sensor data within a date range.
        
        Args:
            start_date: Start date of the range (inclusive)
            end_date: End date of the range (inclusive)
            
        Returns:
            List of sensor data dictionaries
        """
        with self.session_factory() as session:
            query = session.query(IIOTSensorData).filter(
                IIOTSensorData.date >= start_date,
                IIOTSensorData.date <= end_date
            )
                
            sensor_data_list = query.order_by(IIOTSensorData.date).all()
            return [self._to_dict(sensor_data) for sensor_data in sensor_data_list]

    def add(self, value: Dict[str, Any], date: datetime = None, station_id: int = None) -> Dict[str, Any]:
        """Add new IIOT sensor data."""
        with self.session_factory() as session:
            # Check if station_id exists
            if station_id is not None:
                station = session.query(Station).filter(Station.id == station_id).exists()
                if not session.query(station).scalar():
                    raise ValueError(f"Station with id {station_id} does not exist.")
            # Ensure value is a dictionary
            if not isinstance(value, dict):
                raise ValueError(f"The 'value' field must be a dictionary, got {type(value).__name__}")
            sensor_data = IIOTSensorData(
                value=value,
                date=date,
                station_id=station_id
            )
            session.add(sensor_data)
            session.commit()
            session.refresh(sensor_data)
            return self._to_dict(sensor_data)

    def update(self, sensor_data_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """Update IIOT sensor data."""
        with self.session_factory() as session:
            sensor_data = session.query(IIOTSensorData).filter(IIOTSensorData.id == sensor_data_id).first()
            if sensor_data:
                for key, value in kwargs.items():
                    setattr(sensor_data, key, value)
                session.commit()
                session.refresh(sensor_data)
                return self._to_dict(sensor_data)
            return None

    def delete(self, sensor_data_id: int) -> bool:
        """Delete IIOT sensor data."""
        with self.session_factory() as session:
            sensor_data = session.query(IIOTSensorData).filter(IIOTSensorData.id == sensor_data_id).first()
            if sensor_data:
                session.delete(sensor_data)
                session.commit()
                return True
            return False
