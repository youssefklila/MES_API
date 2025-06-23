from contextlib import AbstractContextManager
from sqlalchemy.orm import Session
from typing import Callable, List, Dict, Any, Optional
from webapp.ADM.machine_assets.erp_group.erp.models.erp_model import ERPGroup

class ERPGroupRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self) -> List[Dict[str, Any]]:
        with self.session_factory() as session:
            erp_groups = session.query(ERPGroup).all()
            return [self._to_dict(erp_group) for erp_group in erp_groups]

    def get_by_id(self, erp_group_id: int) -> Optional[Dict[str, Any]]:
        with self.session_factory() as session:
            erp_group = session.query(ERPGroup).filter(ERPGroup.id == erp_group_id).first()
            if erp_group:
                return self._to_dict(erp_group)
            return None

    def add(self, erp_group_data: ERPGroup) -> Dict[str, Any]:
        with self.session_factory() as session:
            session.add(erp_group_data)
            session.commit()
            session.refresh(erp_group_data)
            return self._to_dict(erp_group_data)

    def delete_by_id(self, erp_group_id: int) -> bool:
        with self.session_factory() as session:
            erp_group = session.query(ERPGroup).filter(ERPGroup.id == erp_group_id).first()
            if erp_group:
                session.delete(erp_group)
                session.commit()
                return True
            return False

    def update(self, erp_group_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        with self.session_factory() as session:
            erp_group = session.query(ERPGroup).filter(ERPGroup.id == erp_group_id).first()
            if erp_group:
                for key, value in kwargs.items():
                    setattr(erp_group, key, value)
                session.commit()
                session.refresh(erp_group)
                return self._to_dict(erp_group)
            return None

    def _to_dict(self, erp_group: ERPGroup) -> Dict[str, Any]:
        """Convert an ERP Group object to a dictionary."""
        return {
            "id": erp_group.id,
            "state": erp_group.state,
            "erpgroup_no": erp_group.erpgroup_no,
            "erp_group_description": erp_group.erp_group_description,
            "erpsystem": erp_group.erpsystem,
            "sequential": erp_group.sequential,
            "separate_station": erp_group.separate_station,
            "fixed_layer": erp_group.fixed_layer,
            "created_on": erp_group.created_on,
            "edited_on": erp_group.edited_on,
            "modified_by": erp_group.modified_by,
            "user_id": erp_group.user_id,
            "cst_id": erp_group.cst_id,
            "valid": erp_group.valid
        }
