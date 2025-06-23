"""Machine Condition Group repository."""
from contextlib import AbstractContextManager
from sqlalchemy.orm import Session
from typing import Callable, List, Dict, Any, Optional
from webapp.ADM.MDC.machine_condition_group.models.machine_condition_group_model import MachineConditionGroup


class MachineConditionGroupRepository:
    """Repository for Machine Condition Group operations."""

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        """Initialize repository with session factory."""
        self.session_factory = session_factory
    
    def _to_dict(self, group: MachineConditionGroup) -> Dict[str, Any]:
        """Convert MachineConditionGroup model to dictionary."""
        return {
            "id": group.id,
            "group_name": group.group_name,
            "group_description": group.group_description,
            "is_active": group.is_active
        }

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all machine condition groups."""
        with self.session_factory() as session:
            groups = session.query(MachineConditionGroup).all()
            return [self._to_dict(group) for group in groups]

    def get_by_id(self, group_id: int) -> Optional[Dict[str, Any]]:
        """Get machine condition group by ID."""
        with self.session_factory() as session:
            group = session.query(MachineConditionGroup).filter(MachineConditionGroup.id == group_id).first()
            if group:
                return self._to_dict(group)
            return None

    def get_by_name(self, group_name: str) -> Optional[Dict[str, Any]]:
        """Get machine condition group by name."""
        with self.session_factory() as session:
            group = session.query(MachineConditionGroup).filter(MachineConditionGroup.group_name == group_name).first()
            if group:
                return self._to_dict(group)
            return None

    def add(self, group_name: str, group_description: str = None, is_active: bool = True) -> Dict[str, Any]:
        """Add a new machine condition group."""
        with self.session_factory() as session:
            group = MachineConditionGroup(
                group_name=group_name,
                group_description=group_description,
                is_active=is_active
            )
            session.add(group)
            session.commit()
            session.refresh(group)
            return self._to_dict(group)

    def update(self, group_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """Update a machine condition group."""
        with self.session_factory() as session:
            group = session.query(MachineConditionGroup).filter(MachineConditionGroup.id == group_id).first()
            if group:
                for key, value in kwargs.items():
                    setattr(group, key, value)
                session.commit()
                session.refresh(group)
                return self._to_dict(group)
            return None

    def delete(self, group_id: int) -> bool:
        """Delete a machine condition group."""
        with self.session_factory() as session:
            group = session.query(MachineConditionGroup).filter(MachineConditionGroup.id == group_id).first()
            if group:
                session.delete(group)
                session.commit()
                return True
            return False
