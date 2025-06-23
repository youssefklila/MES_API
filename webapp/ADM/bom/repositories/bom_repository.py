# repositories/bom_repository.py

from typing import List, Optional
from sqlalchemy.orm import Session
from contextlib import AbstractContextManager
from webapp.ADM.bom.models.bom_model import Bom

class BomRepository:
    def __init__(self, session_factory: AbstractContextManager[Session]):
        self.session_factory = session_factory

    def get_all_boms(self) -> List[Bom]:
        with self.session_factory() as session:
            return session.query(Bom).all()

    def get_bom_by_id(self, bom_id: int) -> Optional[Bom]:
        with self.session_factory() as session:
            return session.query(Bom).filter(Bom.id == bom_id).first()

    def create_bom(self, bom: Bom) -> Bom:
        with self.session_factory() as session:
            session.add(bom)
            session.commit()
            session.refresh(bom)
            return bom

    def update_bom(self, bom_id: int, **kwargs) -> Optional[Bom]:
        with self.session_factory() as session:
            bom = session.query(Bom).filter(Bom.id == bom_id).first()
            if bom:
                for key, value in kwargs.items():
                    if value is not None:
                        setattr(bom, key, value)
                session.commit()
                session.refresh(bom)
            return bom

    def delete_bom(self, bom_id: int) -> bool:
        with self.session_factory() as session:
            bom = session.query(Bom).filter(Bom.id == bom_id).first()
            if bom:
                session.delete(bom)
                session.commit()
                return True
            return False 