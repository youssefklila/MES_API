# repositories/local_storage_repository.py

from typing import List, Optional
from sqlalchemy.orm import Session
from contextlib import AbstractContextManager
from webapp.ADM.maintenance.localStorage.models.local_storage_model import LocalStorage

class LocalStorageRepository:
    def __init__(self, session_factory: AbstractContextManager[Session]):
        self.session_factory = session_factory

    def get_all_items(self) -> List[LocalStorage]:
        with self.session_factory() as session:
            return session.query(LocalStorage).all()

    def get_item_by_id(self, item_id: int) -> Optional[LocalStorage]:
        with self.session_factory() as session:
            return session.query(LocalStorage).filter(LocalStorage.id == item_id).first()

    def get_item_by_key(self, key: str) -> Optional[LocalStorage]:
        with self.session_factory() as session:
            return session.query(LocalStorage).filter(LocalStorage.key == key).first()

    def create_item(self, local_storage: LocalStorage) -> LocalStorage:
        with self.session_factory() as session:
            session.add(local_storage)
            session.commit()
            session.refresh(local_storage)
            return local_storage

    def update_item(self, item_id: int, **kwargs) -> Optional[LocalStorage]:
        with self.session_factory() as session:
            item = session.query(LocalStorage).filter(LocalStorage.id == item_id).first()
            if item:
                for key, value in kwargs.items():
                    if value is not None:
                        setattr(item, key, value)
                session.commit()
                session.refresh(item)
            return item

    def update_item_by_key(self, key: str, **kwargs) -> Optional[LocalStorage]:
        with self.session_factory() as session:
            item = session.query(LocalStorage).filter(LocalStorage.key == key).first()
            if item:
                for k, value in kwargs.items():
                    if value is not None:
                        setattr(item, k, value)
                session.commit()
                session.refresh(item)
            return item

    def delete_item(self, item_id: int) -> bool:
        with self.session_factory() as session:
            item = session.query(LocalStorage).filter(LocalStorage.id == item_id).first()
            if item:
                session.delete(item)
                session.commit()
                return True
            return False

    def delete_item_by_key(self, key: str) -> bool:
        with self.session_factory() as session:
            item = session.query(LocalStorage).filter(LocalStorage.key == key).first()
            if item:
                session.delete(item)
                session.commit()
                return True
            return False
