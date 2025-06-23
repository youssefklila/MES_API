# services/failure_group_type_service.py

from typing import Dict, List, Optional

from webapp.ADM.TRACKING.failure_group_type.repositories.failure_group_type_repository import FailureGroupTypeRepository

class FailureGroupTypeService:
    def __init__(self, failure_group_type_repository: FailureGroupTypeRepository):
        self.failure_group_type_repository = failure_group_type_repository

    def get_failure_group_type_by_id(self, id: int) -> Optional[Dict]:
        """Get a failure group type by ID."""
        return self.failure_group_type_repository.get_by_id(id)

    def get_all_failure_group_types(self) -> List[Dict]:
        """Get all failure group types."""
        return self.failure_group_type_repository.get_all()

    def create_failure_group_type(self, failure_group_name: str, failure_group_desc: Optional[str] = None) -> Dict:
        """Create a new failure group type."""
        return self.failure_group_type_repository.add(
            failure_group_name=failure_group_name,
            failure_group_desc=failure_group_desc
        )

    def update_failure_group_type(self, id: int, failure_group_name: Optional[str] = None, 
                                 failure_group_desc: Optional[str] = None) -> Optional[Dict]:
        """Update a failure group type."""
        update_data = {}
        if failure_group_name is not None:
            update_data["failure_group_name"] = failure_group_name
        if failure_group_desc is not None:
            update_data["failure_group_desc"] = failure_group_desc
        
        return self.failure_group_type_repository.update(id, **update_data)

    def delete_failure_group_type(self, id: int) -> Dict[str, bool]:
        """Delete a failure group type."""
        # Check if the failure group type exists
        failure_group_type = self.failure_group_type_repository.get_by_id(id)
        if not failure_group_type:
            return {"success": False, "reason": "not_found"}
        
        # Delete the failure group type
        result = self.failure_group_type_repository.delete(id)
        return {"success": result}

    def get_failure_group_type_by_name(self, failure_group_name: str) -> Optional[Dict]:
        """Get a failure group type by name."""
        return self.failure_group_type_repository.get_by_name(failure_group_name)
