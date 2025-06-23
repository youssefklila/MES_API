# repositories/measurement_data_repository.py

from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Callable
from datetime import datetime
from contextlib import AbstractContextManager

from webapp.ADM.TRACKING.measurement_data.models.measurement_data_model import MeasurementData

class MeasurementDataRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def get_by_id(self, measurement_id: int) -> Optional[Dict]:
        """Get a measurement data by ID."""
        with self.session_factory() as session:
            measurement = session.query(MeasurementData).filter(MeasurementData.id == measurement_id).first()
            if not measurement:
                return None
            return self._to_dict(measurement)

    def get_all(self) -> List[Dict]:
        """Get all measurement data."""
        with self.session_factory() as session:
            measurements = session.query(MeasurementData).all()
            return [self._to_dict(measurement) for measurement in measurements]

    def add(self, station_id: int, workorder_id: int, book_date: datetime, 
            measure_name: str, measure_value: str,
            lower_limit: Optional[str] = None, upper_limit: Optional[str] = None, 
            nominal: Optional[str] = None, tolerance: Optional[str] = None,
            measure_fail_code: Optional[int] = None, booking_id: Optional[int] = None,
            measure_type: Optional[str] = None) -> Dict:
        """Add a new measurement data."""
        with self.session_factory() as session:
            measurement = MeasurementData(
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
            session.add(measurement)
            session.commit()
            session.refresh(measurement)
            return self._to_dict(measurement)

    def update_measurement(self, measurement_id: int, **kwargs) -> Optional[Dict]:
        """Update a measurement data."""
        with self.session_factory() as session:
            measurement = session.query(MeasurementData).filter(MeasurementData.id == measurement_id).first()
            if not measurement:
                return None

            # Update only provided fields
            for key, value in kwargs.items():
                if value is not None and hasattr(measurement, key):
                    setattr(measurement, key, value)

            session.commit()
            session.refresh(measurement)
            return self._to_dict(measurement)

    def delete_by_id(self, measurement_id: int) -> bool:
        """Delete a measurement data by ID."""
        with self.session_factory() as session:
            measurement = session.query(MeasurementData).filter(MeasurementData.id == measurement_id).first()
            if not measurement:
                return False

            session.delete(measurement)
            session.commit()
            return True
    
    def get_by_workorder_id(self, workorder_id: int) -> List[Dict]:
        """Get measurement data by workorder ID."""
        with self.session_factory() as session:
            measurements = session.query(MeasurementData).filter(MeasurementData.workorder_id == workorder_id).all()
            return [self._to_dict(measurement) for measurement in measurements]
    
    def get_by_station_id(self, station_id: int) -> List[Dict]:
        """Get measurement data by station ID."""
        with self.session_factory() as session:
            measurements = session.query(MeasurementData).filter(MeasurementData.station_id == station_id).all()
            return [self._to_dict(measurement) for measurement in measurements]
    
    def get_by_booking_id(self, booking_id: int) -> List[Dict]:
        """Get measurement data by booking ID."""
        with self.session_factory() as session:
            measurements = session.query(MeasurementData).filter(MeasurementData.booking_id == booking_id).all()
            return [self._to_dict(measurement) for measurement in measurements]
    
    def _to_dict(self, measurement: MeasurementData) -> Dict:
        """Convert a MeasurementData model to a dictionary."""
        return {
            "id": measurement.id,
            "station_id": measurement.station_id,
            "workorder_id": measurement.workorder_id,
            "book_date": measurement.book_date,
            "measure_name": measurement.measure_name,
            "measure_value": measurement.measure_value,
            "lower_limit": measurement.lower_limit,
            "upper_limit": measurement.upper_limit,
            "nominal": measurement.nominal,
            "tolerance": measurement.tolerance,
            "measure_fail_code": measurement.measure_fail_code,
            "booking_id": measurement.booking_id,
            "measure_type": measurement.measure_type
        }
