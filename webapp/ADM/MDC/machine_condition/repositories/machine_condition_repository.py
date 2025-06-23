"""Machine Condition repository."""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from webapp.ADM.MDC.machine_condition.models.machine_condition_model import MachineCondition


class MachineConditionRepository:
    """Repository for Machine Condition operations."""

    def __init__(self, session_factory):
        """Initialize repository with session factory."""
        self.session_factory = session_factory

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all machine conditions."""
        with self.session_factory() as session:
            conditions = session.query(MachineCondition).all()
            return [self._model_to_dict(condition) for condition in conditions]

    def get_by_id(self, condition_id: int) -> Optional[Dict[str, Any]]:
        """Get machine condition by ID."""
        with self.session_factory() as session:
            condition = session.query(MachineCondition).filter(MachineCondition.id == condition_id).first()
            if condition:
                return self._model_to_dict(condition)
            return None

    def get_by_name(self, condition_name: str) -> Optional[Dict[str, Any]]:
        """Get machine condition by name."""
        with self.session_factory() as session:
            condition = session.query(MachineCondition).filter(MachineCondition.condition_name == condition_name).first()
            if condition:
                return self._model_to_dict(condition)
            return None

    def get_by_group_id(self, group_id: int) -> List[Dict[str, Any]]:
        """Get all machine conditions for a specific group."""
        with self.session_factory() as session:
            conditions = session.query(MachineCondition).filter(MachineCondition.group_id == group_id).all()
            return [self._model_to_dict(condition) for condition in conditions]

    def add(self, group_id: int, condition_name: str, condition_description: str = None, 
            color_rgb: str = None, is_active: bool = True) -> Dict[str, Any]:
        """Add a new machine condition."""
        with self.session_factory() as session:
            try:
                condition = MachineCondition(
                    group_id=group_id,
                    condition_name=condition_name,
                    condition_description=condition_description,
                    color_rgb=color_rgb,
                    is_active=is_active
                )
                session.add(condition)
                session.commit()
                session.refresh(condition)
                return self._model_to_dict(condition)
            except SQLAlchemyError as e:
                session.rollback()
                raise e

    def update(self, condition_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """Update a machine condition."""
        with self.session_factory() as session:
            try:
                condition = session.query(MachineCondition).filter(MachineCondition.id == condition_id).first()
                if not condition:
                    return None

                for key, value in kwargs.items():
                    if hasattr(condition, key) and value is not None:
                        setattr(condition, key, value)

                session.commit()
                session.refresh(condition)
                return self._model_to_dict(condition)
            except SQLAlchemyError as e:
                session.rollback()
                raise e

    def delete(self, condition_id: int) -> bool:
        """Delete a machine condition."""
        with self.session_factory() as session:
            try:
                condition = session.query(MachineCondition).filter(MachineCondition.id == condition_id).first()
                if not condition:
                    return False

                session.delete(condition)
                session.commit()
                return True
            except SQLAlchemyError as e:
                session.rollback()
                raise e

    def _model_to_dict(self, condition: MachineCondition) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            "id": condition.id,
            "group_id": condition.group_id,
            "condition_name": condition.condition_name,
            "condition_description": condition.condition_description,
            "color_rgb": condition.color_rgb,
            "is_active": condition.is_active
        }
