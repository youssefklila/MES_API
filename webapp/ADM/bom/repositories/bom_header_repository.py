from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from contextlib import AbstractContextManager
from webapp.ADM.bom.models.bom_header_model import BomHeader

class BomHeaderRepository:
    def __init__(self, session_factory: AbstractContextManager[Session]):
        self.session_factory = session_factory

    def _to_dict(self, bom_header: BomHeader) -> Dict:
        return {
            'id': bom_header.id,
            'description': bom_header.description,
            'valid_from': bom_header.valid_from,
            'valid_to': bom_header.valid_to,
            'last_updated': bom_header.last_updated,
            'part_master_id': bom_header.part_master_id
        }

    def get_all(self) -> List[Dict]:
        with self.session_factory() as session:
            bom_headers = session.query(BomHeader).all()
            return [self._to_dict(bom_header) for bom_header in bom_headers]

    def get_by_id(self, bom_header_id: int) -> Optional[Dict]:
        with self.session_factory() as session:
            bom_header = session.query(BomHeader).filter(BomHeader.id == bom_header_id).first()
            return self._to_dict(bom_header) if bom_header else None

    def create(self, **kwargs) -> Dict:
        with self.session_factory() as session:
            new_bom_header = BomHeader(**kwargs)
            session.add(new_bom_header)
            session.commit()
            session.refresh(new_bom_header)
            return self._to_dict(new_bom_header)

    def update(self, bom_header_id: int, **kwargs) -> Optional[Dict]:
        with self.session_factory() as session:
            bom_header = session.query(BomHeader).filter(BomHeader.id == bom_header_id).first()
            if bom_header:
                for key, value in kwargs.items():
                    if value is not None:
                        setattr(bom_header, key, value)
                session.commit()
                session.refresh(bom_header)
                return self._to_dict(bom_header)
            return None

    def delete(self, bom_header_id: int) -> bool:
        with self.session_factory() as session:
            bom_header = session.query(BomHeader).filter(BomHeader.id == bom_header_id).first()
            if bom_header:
                session.delete(bom_header)
                session.commit()
                return True
            return False 