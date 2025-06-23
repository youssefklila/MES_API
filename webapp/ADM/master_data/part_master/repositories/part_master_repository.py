from typing import Callable, List, Dict, Optional
from sqlalchemy.orm import Session
from contextlib import AbstractContextManager
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import text
from webapp.ADM.master_data.part_master.models.part_master_model import PartMaster


class PartMasterRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def _to_dict(self, part_master: PartMaster) -> Dict:
        """Convert SQLAlchemy model to dictionary while session is active."""
        return {
            'id': part_master.id,
            'part_number': part_master.part_number,
            'description': part_master.description,
            'part_status': part_master.part_status,
            'parttype_id': part_master.parttype_id,
            'partgroup_id': part_master.partgroup_id,
            'case_type': part_master.case_type,
            'product': part_master.product,
            'panel': part_master.panel,
            'variant': part_master.variant,
            'machine_group_id': part_master.machine_group_id,
            'material_info': part_master.material_info,
            'parts_index': part_master.parts_index,
            'edit_order_based_bom': part_master.edit_order_based_bom,
            'site_id': part_master.site_id,
            'unit_id': part_master.unit_id,
            'material_code': part_master.material_code,
            'no_of_panels': part_master.no_of_panels,
            'customer_material_number': part_master.customer_material_number,
            'created_on': part_master.created_on,
            'modified_on': part_master.modified_on
        }

    def get_all(self) -> List[Dict]:
        with self.session_factory() as session:
            part_masters = session.query(PartMaster).all()
            return [self._to_dict(part_master) for part_master in part_masters]

    def get_by_id(self, part_master_id: int) -> Optional[Dict]:
        with self.session_factory() as session:
            part_master = session.query(PartMaster).filter(PartMaster.id == part_master_id).first()
            return self._to_dict(part_master) if part_master else None

    def get_by_part_number(self, part_number: str) -> Optional[Dict]:
        with self.session_factory() as session:
            part_master = session.query(PartMaster).filter(PartMaster.part_number == part_number).first()
            return self._to_dict(part_master) if part_master else None

    def create(self, **kwargs) -> Dict:
        with self.session_factory() as session:
            new_part_master = PartMaster(**kwargs)
            session.add(new_part_master)
            session.flush()  # Ensures IDs are assigned before commit
            session.commit()  # Commit the transaction to save to the database
            session.refresh(new_part_master)  # Refresh to ensure all attributes are loaded
            return self._to_dict(new_part_master)

    def update(self, part_master_id: int, **kwargs) -> Optional[Dict]:
        with self.session_factory() as session:
            part_master = session.query(PartMaster).filter(PartMaster.id == part_master_id).first()
            if part_master:
                for key, value in kwargs.items():
                    setattr(part_master, key, value)
                session.commit()  # Commit the transaction to permanently save changes
                session.refresh(part_master)  # Refresh to ensure all attributes are loaded
                return self._to_dict(part_master)
            return None

    def delete(self, part_master_id: int) -> bool:
        with self.session_factory() as session:
            try:
                # Get the part master to retrieve its part number
                part_master = session.query(PartMaster).filter(PartMaster.id == part_master_id).first()
                if not part_master:
                    return False
                
                # First, handle work orders that reference this part master
                # Option 1: Delete the work orders
                session.execute(
                    text("DELETE FROM work_orders WHERE part_number = :part_number"),
                    {"part_number": str(part_master.part_number)}
                )
                
                # Option 2 (alternative): Set a default part number instead of deleting
                # session.execute(
                #     text("UPDATE work_orders SET part_number = 'DELETED' WHERE part_number = :part_number"),
                #     {"part_number": str(part_master.part_number)}
                # )
                
                # Delete any BOM items that reference this part master
                session.execute(
                    text("DELETE FROM bom_items WHERE part_master_id = :id"),
                    {"id": part_master_id}
                )
                
                # Delete any BOM headers that reference this part master
                session.execute(
                    text("DELETE FROM bom_headers WHERE part_master_id = :id"),
                    {"id": part_master_id}
                )
                
                # Finally, delete the part master itself
                session.delete(part_master)
                session.commit()
                return True
            except ProgrammingError as e:
                if "relation \"boms\" does not exist" in str(e):
                    # If BOM table doesn't exist, use raw SQL to delete
                    session.rollback()
                    part_exists = session.query(PartMaster).filter(PartMaster.id == part_master_id).first() is not None
                    if not part_exists:
                        return False
                    session.execute(
                        text("DELETE FROM part_master WHERE id = :id"),
                        {"id": part_master_id}
                    )
                    session.commit()
                    return True
                else:
                    raise
            except Exception:
                session.rollback()
                return False
