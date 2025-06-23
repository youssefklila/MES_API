from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from contextlib import AbstractContextManager
from webapp.ADM.bom.models.bom_item_model import BomItem

class BomItemRepository:
    def __init__(self, session_factory: AbstractContextManager[Session]):
        self.session_factory = session_factory

    def _to_dict(self, bom_item: BomItem) -> Dict:
        return {
            'id': bom_item.id,
            'bom_header_id': bom_item.bom_header_id,
            'part_master_id': bom_item.part_master_id,
            'quantity': bom_item.quantity,
            'is_product': bom_item.is_product,
            'component_name': bom_item.component_name
        }

    def get_all(self) -> List[Dict]:
        with self.session_factory() as session:
            bom_items = session.query(BomItem).all()
            return [self._to_dict(bom_item) for bom_item in bom_items]

    def get_by_id(self, bom_item_id: int) -> Optional[Dict]:
        with self.session_factory() as session:
            bom_item = session.query(BomItem).filter(BomItem.id == bom_item_id).first()
            return self._to_dict(bom_item) if bom_item else None

    def get_by_bom_header_id(self, bom_header_id: int) -> List[Dict]:
        with self.session_factory() as session:
            bom_items = session.query(BomItem).filter(BomItem.bom_header_id == bom_header_id).all()
            return [self._to_dict(bom_item) for bom_item in bom_items]

    def create(self, **kwargs) -> Dict:
        with self.session_factory() as session:
            new_bom_item = BomItem(**kwargs)
            session.add(new_bom_item)
            session.commit()
            session.refresh(new_bom_item)
            return self._to_dict(new_bom_item)

    def update(self, bom_item_id: int, **kwargs) -> Optional[Dict]:
        with self.session_factory() as session:
            bom_item = session.query(BomItem).filter(BomItem.id == bom_item_id).first()
            if bom_item:
                for key, value in kwargs.items():
                    if value is not None:
                        setattr(bom_item, key, value)
                session.commit()
                session.refresh(bom_item)
                return self._to_dict(bom_item)
            return None

    def delete(self, bom_item_id: int) -> bool:
        with self.session_factory() as session:
            bom_item = session.query(BomItem).filter(BomItem.id == bom_item_id).first()
            if bom_item:
                session.delete(bom_item)
                session.commit()
                return True
            return False 