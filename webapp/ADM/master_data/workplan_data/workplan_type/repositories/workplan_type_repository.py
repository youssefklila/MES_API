from contextlib import AbstractContextManager
from sqlalchemy.orm import Session
from typing import Callable, List, Dict, Any, Optional
from webapp.ADM.master_data.workplan_data.workplan_type.models.workplan_type_model import WorkPlanType

class WorkPlanTypeRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory
        
    def _to_dict(self, workplan_type: WorkPlanType) -> Dict[str, Any]:
        """Convert WorkPlanType model to dictionary"""
        return {
            "id": workplan_type.id,
            "name": workplan_type.name,
            "description": workplan_type.description,
            "is_active": workplan_type.is_active
        }

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all workplan types as dictionaries"""
        with self.session_factory() as session:
            workplan_types = session.query(WorkPlanType).all()
            return [self._to_dict(wpt) for wpt in workplan_types]

    def get_by_id(self, workplan_type_id: int) -> Optional[Dict[str, Any]]:
        """Get workplan type by ID as dictionary"""
        with self.session_factory() as session:
            workplan_type = session.query(WorkPlanType).filter(WorkPlanType.id == workplan_type_id).first()
            if workplan_type:
                return self._to_dict(workplan_type)
            return None

    def add(self, name: str, description: str, is_active: bool = True) -> Dict[str, Any]:
        """Add a new workplan type and return as dictionary"""
        with self.session_factory() as session:
            workplan_type = WorkPlanType(name=name, description=description, is_active=is_active)
            session.add(workplan_type)
            session.commit()
            session.refresh(workplan_type)
            return self._to_dict(workplan_type)

    def delete_by_id(self, workplan_type_id: int) -> bool:
        """Delete workplan type by ID and return success status"""
        with self.session_factory() as session:
            workplan_type = session.query(WorkPlanType).filter(WorkPlanType.id == workplan_type_id).first()
            if workplan_type:
                session.delete(workplan_type)
                session.commit()
                return True
            return False

    def update_workplan_type(self, workplan_type_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """Update workplan type and return as dictionary"""
        with self.session_factory() as session:
            workplan_type = session.query(WorkPlanType).filter(WorkPlanType.id == workplan_type_id).first()
            if workplan_type:
                for key, value in kwargs.items():
                    setattr(workplan_type, key, value)
                session.commit()
                session.refresh(workplan_type)
                return self._to_dict(workplan_type)
            return None
