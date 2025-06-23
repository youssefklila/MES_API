"""Machine Condition Data service."""
from typing import List, Dict, Any, Optional
from datetime import datetime
from webapp.ADM.MDC.machine_condition_data.repositories.machine_condition_data_repository import MachineConditionDataRepository


class MachineConditionDataService:
    """Service for Machine Condition Data operations."""

    def __init__(self, repository: MachineConditionDataRepository) -> None:
        """Initialize service with repository."""
        self.repository = repository

    def get_all_condition_data(self) -> List[Dict[str, Any]]:
        """Get all machine condition data records."""
        return self.repository.get_all()

    def get_condition_data_by_id(self, data_id: int) -> Optional[Dict[str, Any]]:
        """Get machine condition data by ID."""
        return self.repository.get_by_id(data_id)

    def get_condition_data_by_station(self, station_id: int) -> List[Dict[str, Any]]:
        """Get all machine condition data for a specific station."""
        return self.repository.get_by_station_id(station_id)

    def get_condition_data_by_condition(self, condition_id: int) -> List[Dict[str, Any]]:
        """Get all machine condition data for a specific condition."""
        return self.repository.get_by_condition_id(condition_id)

    def get_condition_data_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get all machine condition data within a date range."""
        return self.repository.get_by_date_range(start_date, end_date)

    def create_condition_data(self, date_from: datetime, station_id: int, condition_id: int, 
                              date_to: datetime = None, color_rgb: int = None, level: str = None,
                              condition_stamp: datetime = None, condition_type: str = None) -> Dict[str, Any]:
        """Create a new machine condition data record."""
        return self.repository.add(
            date_from=date_from,
            date_to=date_to,
            station_id=station_id,
            condition_id=condition_id,
            color_rgb=color_rgb,
            level=level,
            condition_stamp=condition_stamp,
            condition_type=condition_type
        )

    def update_condition_data(self, data_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """Update a machine condition data record."""
        return self.repository.update(data_id, **kwargs)

    def delete_condition_data(self, data_id: int) -> bool:
        """Delete a machine condition data record."""
        return self.repository.delete(data_id)
