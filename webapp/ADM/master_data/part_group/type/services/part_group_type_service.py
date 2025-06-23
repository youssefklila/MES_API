# services/part_group_type_service.py

from typing import List, Optional, Dict

from webapp.ADM.master_data.part_group.type.models.part_group_type_model import PartGroupType
from webapp.ADM.master_data.part_group.type.repositories.part_group_type_repository import PartGroupTypeRepository
from webapp.ADM.master_data.part_group.type.schemas.part_group_type_schema import PartGroupTypeResponse


class PartGroupTypeService:
    def __init__(self, repository: PartGroupTypeRepository):
        self.repository = repository

    def _to_response(self, part_group_type_dict: Dict) -> PartGroupTypeResponse:
        """Convert dictionary to Pydantic response model."""
        return PartGroupTypeResponse(**part_group_type_dict)

    def get_all_part_group_types(self) -> List[PartGroupTypeResponse]:
        """Get all part group types."""
        try:
            part_group_types = self.repository.get_all()
            return [self._to_response(pgt) for pgt in part_group_types]
        except Exception as e:
            raise ValueError(f"Failed to get part group types: {str(e)}")

    def get_part_group_type_by_id(self, part_group_type_id: int) -> Optional[PartGroupTypeResponse]:
        """Get a part group type by ID."""
        try:
            part_group_type = self.repository.get_by_id(part_group_type_id)
            if part_group_type:
                return self._to_response(part_group_type)
            return None
        except Exception as e:
            raise ValueError(f"Failed to get part group type: {str(e)}")

    def add_part_group_type(self, name: str, description: str) -> PartGroupTypeResponse:
        """Add a new part group type."""
        try:
            # Validate input
            if not name or not name.strip():
                raise ValueError("Name is required")
            
            part_group_type = self.repository.add(name.strip(), description)
            return self._to_response(part_group_type)
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Failed to create part group type: {str(e)}")

    def update_part_group_type(self, part_group_type_id: int, **kwargs) -> Optional[PartGroupTypeResponse]:
        """Update a part group type."""
        try:
            # Validate input
            if 'name' in kwargs and (not kwargs['name'] or not kwargs['name'].strip()):
                raise ValueError("Name cannot be empty")
            
            part_group_type = self.repository.update(part_group_type_id, **kwargs)
            if part_group_type:
                return self._to_response(part_group_type)
            return None
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Failed to update part group type: {str(e)}")

    def delete_part_group_type(self, part_group_type_id: int) -> None:
        """Delete a part group type."""
        try:
            self.repository.delete(part_group_type_id)
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Failed to delete part group type: {str(e)}")
