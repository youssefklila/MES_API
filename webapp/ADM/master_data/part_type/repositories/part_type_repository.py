from sqlalchemy.orm import Session
from typing import List, Optional, Callable, Dict, Any
from webapp.ADM.master_data.part_type.models.part_type_model import PartType
from contextlib import AbstractContextManager

class PartTypeRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def _to_dict(self, part_type: PartType) -> Dict[str, Any]:
        return {
            "id": part_type.id,
            "name": part_type.name,
            "description": part_type.description,
            "user_id": part_type.user_id,
            "is_active": part_type.is_active,
            "date_of_creation": part_type.date_of_creation,
            "date_of_change": part_type.date_of_change
        }

    def get_all(self) -> List[Dict[str, Any]]:
        with self.session_factory() as session:
            part_types = session.query(PartType).all()
            return [self._to_dict(pt) for pt in part_types]

    def get_by_id(self, part_type_id: int) -> Optional[Dict[str, Any]]:
        with self.session_factory() as session:
            part_type = session.query(PartType).filter(PartType.id == part_type_id).first()
            return self._to_dict(part_type) if part_type else None

    def add(self, name: str, description: Optional[str] = None, user_id: Optional[int] = None, is_active: bool = True) -> Dict[str, Any]:
        with self.session_factory() as session:
            part_type = PartType(
                name=name,
                description=description,
                user_id=user_id,
                is_active=is_active,
            )
            session.add(part_type)
            session.commit()
            session.refresh(part_type)
            return self._to_dict(part_type)

    def update(self, part_type_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        with self.session_factory() as session:
            part_type = session.query(PartType).filter(PartType.id == part_type_id).first()
            if part_type:
                for key, value in kwargs.items():
                    setattr(part_type, key, value)
                session.commit()
                session.refresh(part_type)
                return self._to_dict(part_type)
            return None

    def delete(self, part_type_id: int) -> bool:
        with self.session_factory() as session:
            part_type = session.query(PartType).filter(PartType.id == part_type_id).first()
            if part_type:
                # Check if there are any part_master records associated with this part_type
                if part_type.part_masters:
                    # Cannot delete part_type with associated part_master records
                    return False
                session.delete(part_type)
                session.commit()
                return True
            return False
