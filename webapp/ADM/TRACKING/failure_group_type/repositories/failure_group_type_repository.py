# repositories/failure_group_type_repository.py

from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Callable
from contextlib import AbstractContextManager

from webapp.ADM.TRACKING.failure_group_type.models.failure_group_type_model import FailureGroupType

class FailureGroupTypeRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def get_by_id(self, id: int) -> Optional[Dict]:
        """Get a failure group type by ID."""
        with self.session_factory() as session:
            failure_group_type = session.query(FailureGroupType).filter(FailureGroupType.id == id).first()
            if not failure_group_type:
                return None
            return self._to_dict(failure_group_type)

    def get_all(self) -> List[Dict]:
        """Get all failure group types."""
        with self.session_factory() as session:
            failure_group_types = session.query(FailureGroupType).all()
            return [self._to_dict(failure_group_type) for failure_group_type in failure_group_types]

    def add(self, failure_group_name: str, failure_group_desc: Optional[str] = None) -> Dict:
        """Add a new failure group type."""
        with self.session_factory() as session:
            failure_group_type = FailureGroupType(
                failure_group_name=failure_group_name,
                failure_group_desc=failure_group_desc
            )
            session.add(failure_group_type)
            session.commit()
            session.refresh(failure_group_type)
            return self._to_dict(failure_group_type)

    def update(self, id: int, **kwargs) -> Optional[Dict]:
        """Update a failure group type."""
        with self.session_factory() as session:
            failure_group_type = session.query(FailureGroupType).filter(FailureGroupType.id == id).first()
            if not failure_group_type:
                return None

            # Update only provided fields
            for key, value in kwargs.items():
                if value is not None and hasattr(failure_group_type, key):
                    setattr(failure_group_type, key, value)

            session.commit()
            session.refresh(failure_group_type)
            return self._to_dict(failure_group_type)

    def delete(self, id: int) -> bool:
        """Delete a failure group type."""
        with self.session_factory() as session:
            failure_group_type = session.query(FailureGroupType).filter(FailureGroupType.id == id).first()
            if not failure_group_type:
                return False
            
            session.delete(failure_group_type)
            session.commit()
            return True

    def get_by_name(self, failure_group_name: str) -> Optional[Dict]:
        """Get a failure group type by name."""
        with self.session_factory() as session:
            failure_group_type = session.query(FailureGroupType).filter(FailureGroupType.failure_group_name == failure_group_name).first()
            if not failure_group_type:
                return None
            return self._to_dict(failure_group_type)

    def _to_dict(self, failure_group_type: FailureGroupType) -> Dict:
        """Convert a FailureGroupType object to a dictionary."""
        return {
            "id": failure_group_type.id,
            "failure_group_name": failure_group_type.failure_group_name,
            "failure_group_desc": failure_group_type.failure_group_desc
        }
