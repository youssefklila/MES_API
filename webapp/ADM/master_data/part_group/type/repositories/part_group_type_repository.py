from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Callable, Dict, Optional
from contextlib import AbstractContextManager
from webapp.ADM.master_data.part_group.type.models.part_group_type_model import PartGroupType

class PartGroupTypeRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def _to_dict(self, part_group_type: PartGroupType) -> Dict:
        """Convert SQLAlchemy model to dictionary."""
        return {
            "id": part_group_type.id,
            "name": part_group_type.name,
            "description": part_group_type.description
        }

    def get_all(self) -> List[Dict]:
        with self.session_factory() as session:
            part_group_types = session.query(PartGroupType).all()
            return [self._to_dict(pgt) for pgt in part_group_types]

    def get_by_id(self, part_group_type_id: int) -> Optional[Dict]:
        with self.session_factory() as session:
            part_group_type = session.query(PartGroupType).filter(PartGroupType.id == part_group_type_id).first()
            if part_group_type:
                return self._to_dict(part_group_type)
            return None

    def get_by_name(self, name: str) -> Optional[Dict]:
        with self.session_factory() as session:
            part_group_type = session.query(PartGroupType).filter(PartGroupType.name == name).first()
            if part_group_type:
                return self._to_dict(part_group_type)
            return None

    def add(self, name: str, description: str) -> Dict:
        with self.session_factory() as session:
            # Check if name already exists
            existing = session.query(PartGroupType).filter(PartGroupType.name == name).first()
            if existing:
                raise ValueError(f"Part group type with name '{name}' already exists")

            part_group_type = PartGroupType(name=name, description=description)
            session.add(part_group_type)
            try:
                session.commit()
                session.refresh(part_group_type)
                return self._to_dict(part_group_type)
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Failed to create part group type: {str(e)}")

    def update(self, part_group_type_id: int, **kwargs) -> Optional[Dict]:
        with self.session_factory() as session:
            part_group_type = session.query(PartGroupType).filter(PartGroupType.id == part_group_type_id).first()
            if part_group_type:
                # If name is being updated, check if new name already exists
                if 'name' in kwargs and kwargs['name'] != part_group_type.name:
                    existing = session.query(PartGroupType).filter(
                        PartGroupType.name == kwargs['name'],
                        PartGroupType.id != part_group_type_id
                    ).first()
                    if existing:
                        raise ValueError(f"Part group type with name '{kwargs['name']}' already exists")

                for key, value in kwargs.items():
                    setattr(part_group_type, key, value)
                try:
                    session.commit()
                    session.refresh(part_group_type)
                    return self._to_dict(part_group_type)
                except IntegrityError as e:
                    session.rollback()
                    raise ValueError(f"Failed to update part group type: {str(e)}")
            return None

    def delete(self, part_group_type_id: int) -> None:
        with self.session_factory() as session:
            part_group_type = session.query(PartGroupType).filter(PartGroupType.id == part_group_type_id).first()
            if part_group_type:
                try:
                    session.delete(part_group_type)
                    session.commit()
                except IntegrityError as e:
                    session.rollback()
                    raise ValueError(f"Failed to delete part group type: {str(e)}")
