from typing import List, Optional, Dict
from webapp.ADM.master_data.part_group.group.models.part_group_model import PartGroup
from webapp.ADM.master_data.part_group.group.repositories.part_group_repository import PartGroupRepository
from webapp.ADM.master_data.part_group.group.schemas.part_group_schema import PartGroupResponse

class PartGroupService:
    def __init__(self, repository: PartGroupRepository):
        self.repository = repository

    def _to_response(self, part_group_dict: Dict) -> PartGroupResponse:
        """Convert dictionary to Pydantic response model."""
        return PartGroupResponse(**part_group_dict)

    def get_all_part_groups(self) -> List[PartGroupResponse]:
        """Get all part groups."""
        try:
            part_groups = self.repository.get_all()
            return [self._to_response(pg) for pg in part_groups]
        except Exception as e:
            raise ValueError(f"Failed to get part groups: {str(e)}")

    def get_part_group_by_id(self, part_group_id: int) -> Optional[PartGroupResponse]:
        """Get a part group by ID."""
        try:
            part_group = self.repository.get_by_id(part_group_id)
            if part_group:
                return self._to_response(part_group)
            return None
        except Exception as e:
            raise ValueError(f"Failed to get part group: {str(e)}")

    def add_part_group(self, name: str, description: str, user_id: int, part_type: str, costs: int, is_active: bool,
                      circulating_lot: int, automatic_emptying: int, master_workplan: str, comment: str, state: int,
                      material_transfer: bool, created_on: str, edited_on: str, part_group_type_id: int) -> PartGroupResponse:
        """Add a new part group."""
        try:
            # Validate input
            if not name or not name.strip():
                raise ValueError("Name is required")
            if not part_group_type_id:
                raise ValueError("Part group type ID is required")
            
            part_group = self.repository.add(
                name=name.strip(),
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
            return self._to_response(part_group)
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Failed to create part group: {str(e)}")

    def update_part_group(self, part_group_id: int, **kwargs) -> Optional[PartGroupResponse]:
        """Update a part group."""
        try:
            # Validate input
            if 'name' in kwargs and (not kwargs['name'] or not kwargs['name'].strip()):
                raise ValueError("Name cannot be empty")
            if 'part_group_type_id' in kwargs and not kwargs['part_group_type_id']:
                raise ValueError("Part group type ID cannot be empty")
            
            part_group = self.repository.update_part_group(part_group_id, **kwargs)
            if part_group:
                return self._to_response(part_group)
            return None
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Failed to update part group: {str(e)}")

    def delete_part_group(self, part_group_id: int) -> bool:
        """Delete a part group.
        
        Returns:
            bool: True if deletion was successful, False if part group not found
        """
        try:
            # First check if the part group exists
            part_group = self.repository.get_by_id(part_group_id)
            if not part_group:
                return False
                
            # If it exists, delete it
            self.repository.delete_by_id(part_group_id)
            return True
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Failed to delete part group: {str(e)}")
