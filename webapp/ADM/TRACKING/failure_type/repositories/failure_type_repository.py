# repositories/failure_type_repository.py

from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Callable
from contextlib import AbstractContextManager

from webapp.ADM.TRACKING.failure_type.models.failure_type_model import FailureType

class FailureTypeRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def get_by_id(self, failure_type_id: int) -> Optional[Dict]:
        """Get a failure type by ID."""
        with self.session_factory() as session:
            failure_type = session.query(FailureType).filter(FailureType.failure_type_id == failure_type_id).first()
            if not failure_type:
                return None
            return self._to_dict(failure_type)

    def get_all(self) -> List[Dict]:
        """Get all failure types."""
        with self.session_factory() as session:
            failure_types = session.query(FailureType).all()
            return [self._to_dict(failure_type) for failure_type in failure_types]

    def add(self, failure_type_code: str, failure_type_desc: Optional[str] = None, site_id: Optional[int] = None, failure_group_id: Optional[int] = None) -> Dict:
        """Add a new failure type."""
        with self.session_factory() as session:
            failure_type = FailureType(
                failure_type_code=failure_type_code,
                failure_type_desc=failure_type_desc,
                site_id=site_id,
                failure_group_id=failure_group_id
            )
            session.add(failure_type)
            session.commit()
            session.refresh(failure_type)
            return self._to_dict(failure_type)

    def update_failure_type(self, failure_type_id: int, **kwargs) -> Optional[Dict]:
        """Update a failure type."""
        with self.session_factory() as session:
            failure_type = session.query(FailureType).filter(FailureType.failure_type_id == failure_type_id).first()
            if not failure_type:
                return None

            # Update only provided fields
            for key, value in kwargs.items():
                if value is not None and hasattr(failure_type, key):
                    setattr(failure_type, key, value)

            session.commit()
            session.refresh(failure_type)
            return self._to_dict(failure_type)

    def delete_by_id(self, failure_type_id: int) -> bool:
        """Delete a failure type by ID."""
        with self.session_factory() as session:
            failure_type = session.query(FailureType).filter(FailureType.failure_type_id == failure_type_id).first()
            if not failure_type:
                return False

            session.delete(failure_type)
            session.commit()
            return True
    
    def get_by_code(self, failure_type_code: str) -> Optional[Dict]:
        """Get a failure type by code."""
        with self.session_factory() as session:
            failure_type = session.query(FailureType).filter(FailureType.failure_type_code == failure_type_code).first()
            if not failure_type:
                return None
            return self._to_dict(failure_type)
    
    def _to_dict(self, failure_type: FailureType) -> Dict:
        """Convert a FailureType model to a dictionary."""
        return {
            "failure_type_id": failure_type.failure_type_id,
            "failure_type_code": failure_type.failure_type_code,
            "failure_type_desc": failure_type.failure_type_desc,
            "site_id": failure_type.site_id,
            "failure_group_id": failure_type.failure_group_id
        }
