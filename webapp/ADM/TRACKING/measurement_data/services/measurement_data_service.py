# services/measurement_data_service.py

from typing import Dict, List, Optional
from datetime import datetime

from webapp.ADM.TRACKING.measurement_data.repositories.measurement_data_repository import MeasurementDataRepository

class MeasurementDataService:
    def __init__(self, measurement_data_repository: MeasurementDataRepository):
        self.repository = measurement_data_repository

    def get_by_id(self, measurement_id: int) -> Optional[Dict]:
        """Get a measurement data by ID."""
        return self.repository.get_by_id(measurement_id)

    def get_all(self) -> List[Dict]:
        """Get all measurement data."""
        return self.repository.get_all()

    def create(self, station_id: int, workorder_id: int, book_date: datetime, 
               measure_name: str, measure_value: str,
               lower_limit: Optional[str] = None, upper_limit: Optional[str] = None, 
               nominal: Optional[str] = None, tolerance: Optional[str] = None,
               measure_fail_code: Optional[int] = None, booking_id: Optional[int] = None,
               measure_type: Optional[str] = None) -> Dict:
        """Create a new measurement data."""
        # Fix: treat booking_id=0 as None to avoid FK violation
        if booking_id == 0:
            booking_id = None
        return self.repository.add(
            station_id=station_id,
            workorder_id=workorder_id,
            book_date=book_date,
            measure_name=measure_name,
            measure_value=measure_value,
            lower_limit=lower_limit,
            upper_limit=upper_limit,
            nominal=nominal,
            tolerance=tolerance,
            measure_fail_code=measure_fail_code,
            booking_id=booking_id,
            measure_type=measure_type
        )

    def update(self, measurement_id: int, **kwargs) -> Optional[Dict]:
        """Update a measurement data."""
        return self.repository.update_measurement(measurement_id, **kwargs)

    def delete(self, measurement_id: int) -> bool:
        """Delete a measurement data by ID."""
        return self.repository.delete_by_id(measurement_id)
    
    def get_by_workorder_id(self, workorder_id: int) -> List[Dict]:
        """Get measurement data by workorder ID."""
        return self.repository.get_by_workorder_id(workorder_id)
    
    def get_by_station_id(self, station_id: int) -> List[Dict]:
        """Get measurement data by station ID."""
        return self.repository.get_by_station_id(station_id)
    
    def get_by_booking_id(self, booking_id: int) -> List[Dict]:
        """Get measurement data by booking ID."""
        return self.repository.get_by_booking_id(booking_id)
