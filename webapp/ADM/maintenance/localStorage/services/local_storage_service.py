# services/local_storage_service.py

from typing import List, Optional, Dict, Any
from webapp.ADM.maintenance.localStorage.models.local_storage_model import LocalStorage
from webapp.ADM.maintenance.localStorage.repositories.local_storage_repository import LocalStorageRepository

class LocalStorageService:
    def __init__(self, local_storage_repository: LocalStorageRepository):
        self.local_storage_repository = local_storage_repository

    def get_all_items(self) -> List[Dict[str, Any]]:
        items = self.local_storage_repository.get_all_items()
        return [self._to_dict(item) for item in items]

    def get_item_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        item = self.local_storage_repository.get_item_by_id(item_id)
        return self._to_dict(item) if item else None

    def get_item_by_key(self, key: str) -> Optional[Dict[str, Any]]:
        item = self.local_storage_repository.get_item_by_key(key)
        return self._to_dict(item) if item else None

    def add_item(self, **kwargs) -> Dict[str, Any]:
        # Check if item with this key already exists
        existing_item = self.local_storage_repository.get_item_by_key(kwargs.get('key'))
        if existing_item:
            # Update the existing item
            updated_item = self.local_storage_repository.update_item_by_key(
                kwargs.get('key'), 
                value=kwargs.get('value')
            )
            return self._to_dict(updated_item)
        
        # Create new item
        item = LocalStorage(**kwargs)
        created_item = self.local_storage_repository.create_item(item)
        return self._to_dict(created_item)

    def update_item(self, item_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        updated_item = self.local_storage_repository.update_item(item_id, **kwargs)
        return self._to_dict(updated_item) if updated_item else None

    def update_item_by_key(self, key: str, **kwargs) -> Optional[Dict[str, Any]]:
        updated_item = self.local_storage_repository.update_item_by_key(key, **kwargs)
        return self._to_dict(updated_item) if updated_item else None

    def delete_item(self, item_id: int) -> bool:
        return self.local_storage_repository.delete_item(item_id)

    def delete_item_by_key(self, key: str) -> bool:
        return self.local_storage_repository.delete_item_by_key(key)

    @staticmethod
    def _to_dict(item: LocalStorage) -> Dict[str, Any]:
        return {
            "id": item.id,
            "key": item.key,
            "value": item.value,
            "created_at": item.created_at,
            "updated_at": item.updated_at
        }
