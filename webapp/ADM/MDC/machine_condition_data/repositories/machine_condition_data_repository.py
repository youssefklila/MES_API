"""Machine Condition Data repository."""
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from webapp.ADM.MDC.machine_condition_data.models.machine_condition_data_model import MachineConditionData


class MachineConditionDataRepository:
    """Repository for Machine Condition Data operations."""

    def __init__(self, session_factory):
        """Initialize repository with session factory."""
        self.session_factory = session_factory

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all machine condition data records."""
        with self.session_factory() as session:
            data_records = session.query(MachineConditionData).all()
            return [self._model_to_dict(record) for record in data_records]

    def get_by_id(self, data_id: int) -> Optional[Dict[str, Any]]:
        """Get machine condition data by ID."""
        with self.session_factory() as session:
            data = session.query(MachineConditionData).filter(MachineConditionData.id == data_id).first()
            if data:
                return self._model_to_dict(data)
            return None

    def get_by_station_id(self, station_id: int) -> List[Dict[str, Any]]:
        """Get all machine condition data for a specific station."""
        with self.session_factory() as session:
            data_records = session.query(MachineConditionData).filter(
                MachineConditionData.station_id == station_id
            ).all()
            return [self._model_to_dict(record) for record in data_records]

    def get_by_condition_id(self, condition_id: int) -> List[Dict[str, Any]]:
        """Get all machine condition data for a specific condition."""
        with self.session_factory() as session:
            data_records = session.query(MachineConditionData).filter(
                MachineConditionData.condition_id == condition_id
            ).all()
            return [self._model_to_dict(record) for record in data_records]

    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get all machine condition data within a date range."""
        with self.session_factory() as session:
            data_records = session.query(MachineConditionData).filter(
                MachineConditionData.date_from >= start_date,
                MachineConditionData.date_from <= end_date
            ).all()
            return [self._model_to_dict(record) for record in data_records]

    def add(self, date_from: datetime, station_id: int, condition_id: int, 
            date_to: datetime = None, color_rgb: int = None, level: str = None,
            condition_stamp: datetime = None, condition_type: str = None) -> Dict[str, Any]:
        """Add a new machine condition data record."""
        with self.session_factory() as session:
            try:
                data = MachineConditionData(
                    date_from=date_from,
                    date_to=date_to,
                    station_id=station_id,
                    condition_id=condition_id,
                    color_rgb=color_rgb,
                    level=level,
                    condition_stamp=condition_stamp,
                    condition_type=condition_type
                )
                session.add(data)
                session.commit()
                session.refresh(data)
                return self._model_to_dict(data)
            except SQLAlchemyError as e:
                session.rollback()
                raise e

    def update(self, data_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """Update a machine condition data record."""
        with self.session_factory() as session:
            try:
                data = session.query(MachineConditionData).filter(MachineConditionData.id == data_id).first()
                if not data:
                    return None

                for key, value in kwargs.items():
                    if hasattr(data, key) and value is not None:
                        setattr(data, key, value)

                session.commit()
                session.refresh(data)
                return self._model_to_dict(data)
            except SQLAlchemyError as e:
                session.rollback()
                raise e

    def delete(self, data_id: int) -> bool:
        """Delete a machine condition data record."""
        with self.session_factory() as session:
            try:
                data = session.query(MachineConditionData).filter(MachineConditionData.id == data_id).first()
                if not data:
                    return False

                session.delete(data)
                session.commit()
                return True
            except SQLAlchemyError as e:
                session.rollback()
                raise e

    def _model_to_dict(self, data: MachineConditionData) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            "id": data.id,
            "date_from": data.date_from,
            "date_to": data.date_to,
            "station_id": data.station_id,
            "condition_id": data.condition_id,
            "color_rgb": data.color_rgb,
            "level": data.level,
            "condition_created": data.condition_created,
            "condition_stamp": data.condition_stamp,
            "condition_type": data.condition_type
        }
