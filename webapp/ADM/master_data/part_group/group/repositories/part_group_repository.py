from contextlib import AbstractContextManager
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Callable, List, Optional
from webapp.ADM.master_data.part_group.group.models.part_group_model import PartGroup
from webapp.ADM.master_data.part_group.type.models.part_group_type_model import PartGroupType

class PartGroupRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def _to_dict(self, part_group: PartGroup) -> dict:
        """Convert SQLAlchemy model to dictionary."""
        return {
            "id": part_group.id,
            "name": part_group.name,
            "description": part_group.description,
            "user_id": part_group.user_id,
            "part_type": part_group.part_type,
            "costs": part_group.costs,
            "is_active": part_group.is_active,
            "circulating_lot": part_group.circulating_lot,
            "automatic_emptying": part_group.automatic_emptying,
            "master_workplan": part_group.master_workplan,
            "comment": part_group.comment,
            "state": part_group.state,
            "material_transfer": part_group.material_transfer,
            "created_on": part_group.created_on,
            "edited_on": part_group.edited_on,
            "part_group_type_id": part_group.part_group_type_id
        }

    def get_all(self) -> List[dict]:
        with self.session_factory() as session:
            part_groups = session.query(PartGroup).all()
            return [self._to_dict(pg) for pg in part_groups]

    def get_by_id(self, part_group_id: int) -> Optional[dict]:
        with self.session_factory() as session:
            part_group = session.query(PartGroup).filter(PartGroup.id == part_group_id).first()
            if part_group:
                return self._to_dict(part_group)
            return None

    def add(self, name: str, description: str, user_id: int, part_type: str, costs: int, is_active: bool,
            circulating_lot: int, automatic_emptying: int, master_workplan: str, comment: str, state: int,
            material_transfer: bool, created_on: str, edited_on: str, part_group_type_id: int) -> dict:
        with self.session_factory() as session:
            # Check if part group type exists
            part_group_type = session.query(PartGroupType).filter(PartGroupType.id == part_group_type_id).first()
            if not part_group_type:
                raise ValueError(f"Part group type with ID {part_group_type_id} does not exist")

            part_group = PartGroup(
                name=name,
                description=description,
                user_id=user_id,
                part_type=part_type,
                costs=costs,
                is_active=is_active,
                circulating_lot=circulating_lot,
                automatic_emptying=automatic_emptying,
                master_workplan=master_workplan,
                comment=comment,
                state=state,
                material_transfer=material_transfer,
                created_on=created_on,
                edited_on=edited_on,
                part_group_type_id=part_group_type_id
            )
            try:
                session.add(part_group)
                session.commit()
                session.refresh(part_group)
                return self._to_dict(part_group)
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Failed to create part group: {str(e)}")

    def delete_by_id(self, part_group_id: int) -> None:
        with self.session_factory() as session:
            part_group = session.query(PartGroup).filter(PartGroup.id == part_group_id).first()
            if part_group:
                try:
                    session.delete(part_group)
                    session.commit()
                except IntegrityError as e:
                    session.rollback()
                    raise ValueError(f"Failed to delete part group: {str(e)}")

    def update_part_group(self, part_group_id: int, **kwargs) -> Optional[dict]:
        with self.session_factory() as session:
            part_group = session.query(PartGroup).filter(PartGroup.id == part_group_id).first()
            if part_group:
                # If part_group_type_id is being updated, check if it exists
                if 'part_group_type_id' in kwargs:
                    part_group_type = session.query(PartGroupType).filter(
                        PartGroupType.id == kwargs['part_group_type_id']
                    ).first()
                    if not part_group_type:
                        raise ValueError(f"Part group type with ID {kwargs['part_group_type_id']} does not exist")

                for key, value in kwargs.items():
                    setattr(part_group, key, value)
                try:
                    session.commit()
                    session.refresh(part_group)
                    return self._to_dict(part_group)
                except IntegrityError as e:
                    session.rollback()
                    raise ValueError(f"Failed to update part group: {str(e)}")
            return None
