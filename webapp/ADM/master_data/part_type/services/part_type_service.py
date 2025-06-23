# services/part_type_service.py

from typing import List, Optional, Dict, Any
from datetime import datetime

from webapp.ADM.master_data.part_type.models.part_type_model import PartType
from webapp.ADM.master_data.part_type.repositories.part_type_repository import PartTypeRepository


class PartTypeService:
    def __init__(self, repository: PartTypeRepository):
        self.repository = repository

    def get_all_part_types(self) -> List[Dict[str, Any]]:
        return self.repository.get_all()

    def get_part_type_by_id(self, part_type_id: int) -> Optional[Dict[str, Any]]:
        return self.repository.get_by_id(part_type_id)

    def add_part_type(self, name: str, description: Optional[str] = None, user_id: int = None, is_active: bool = True) -> Dict[str, Any]:
        return self.repository.add(name=name, description=description, user_id=user_id, is_active=is_active)

    def update_part_type(self, part_type_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        return self.repository.update(part_type_id, **kwargs)

    def delete_part_type(self, part_type_id: int) -> Dict[str, Any]:
        """
        Delete a part type.
        
        Returns:
            Dict with success status and message. If deletion fails due to associated part_master records,
            returns {'success': False, 'reason': 'has_part_masters'}. If part type not found,
            returns {'success': False, 'reason': 'not_found'}.
        """
        result = self.repository.delete(part_type_id)
        if result is False:
            # Check if the part type exists
            part_type = self.repository.get_by_id(part_type_id)
            if part_type:
                # Part type exists but couldn't be deleted (has part_masters)
                return {"success": False, "reason": "has_part_masters"}
            else:
                # Part type doesn't exist
                return {"success": False, "reason": "not_found"}
        return {"success": True}
