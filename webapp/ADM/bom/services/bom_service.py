# services/bom_service.py

from typing import List, Optional, Dict, Any
from webapp.ADM.bom.models.bom_model import Bom
from webapp.ADM.bom.repositories.bom_repository import BomRepository

class BomService:
    def __init__(self, bom_repository: BomRepository):
        self.bom_repository = bom_repository

    def get_all_boms(self) -> List[Dict[str, Any]]:
        boms = self.bom_repository.get_all_boms()
        return [self._to_dict(bom) for bom in boms]

    def get_bom_by_id(self, bom_id: int) -> Optional[Dict[str, Any]]:
        bom = self.bom_repository.get_bom_by_id(bom_id)
        return self._to_dict(bom) if bom else None

    def add_bom(self, **kwargs) -> Dict[str, Any]:
        bom = Bom(**kwargs)
        created_bom = self.bom_repository.create_bom(bom)
        return self._to_dict(created_bom)

    def update_bom(self, bom_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        updated_bom = self.bom_repository.update_bom(bom_id, **kwargs)
        return self._to_dict(updated_bom) if updated_bom else None

    def delete_bom(self, bom_id: int) -> bool:
        return self.bom_repository.delete_bom(bom_id)

    @staticmethod
    def _to_dict(bom: Bom) -> Dict[str, Any]:
        return {
            "id": bom.id,
            "state": bom.state,
            "bom_type": bom.bom_type,
            "bom_version": bom.bom_version,
            "bom_version_valid_from": bom.bom_version_valid_from,
            "bom_version_valid_to": bom.bom_version_valid_to,
            "user_id": bom.user_id,
            "part_number": bom.part_number
        }