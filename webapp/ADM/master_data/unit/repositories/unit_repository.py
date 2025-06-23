# repositories/unit_repository.py

from contextlib import AbstractContextManager
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Callable, List, Dict, Optional
from webapp.ADM.master_data.unit.models.unit_model import Unit

class UnitRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def _to_dict(self, unit: Unit) -> Dict:
        """Convert SQLAlchemy model to dictionary."""
        return {
            "id": unit.id,
            "unit_name": unit.unit_name,
            "description": unit.description
        }

    def get_all(self) -> List[Dict]:
        with self.session_factory() as session:
            units = session.query(Unit).all()
            return [self._to_dict(u) for u in units]

    def get_by_id(self, unit_id: int) -> Optional[Dict]:
        with self.session_factory() as session:
            unit = session.query(Unit).filter(Unit.id == unit_id).first()
            if unit:
                return self._to_dict(unit)
            return None

    def add(self, unit_name: str, description: str) -> Dict:
        with self.session_factory() as session:
            unit = Unit(
                unit_name=unit_name,
                description=description
            )
            try:
                session.add(unit)
                session.commit()
                session.refresh(unit)
                return self._to_dict(unit)
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Failed to create unit: {str(e)}")

    def delete_by_id(self, unit_id: int) -> None:
        with self.session_factory() as session:
            unit = session.query(Unit).filter(Unit.id == unit_id).first()
            if unit:
                try:
                    session.delete(unit)
                    session.commit()
                except IntegrityError as e:
                    session.rollback()
                    raise ValueError(f"Failed to delete unit: {str(e)}")

    def update_unit(self, unit_id: int, **kwargs) -> Optional[Dict]:
        with self.session_factory() as session:
            unit = session.query(Unit).filter(Unit.id == unit_id).first()
            if unit:
                for key, value in kwargs.items():
                    setattr(unit, key, value)
                try:
                    session.commit()
                    session.refresh(unit)
                    return self._to_dict(unit)
                except IntegrityError as e:
                    session.rollback()
                    raise ValueError(f"Failed to update unit: {str(e)}")
            return None
