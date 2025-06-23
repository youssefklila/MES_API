# services/failure_type_service.py

from typing import Dict, List, Optional

from webapp.ADM.TRACKING.failure_type.repositories.failure_type_repository import FailureTypeRepository

class FailureTypeService:
    def __init__(self, failure_type_repository: FailureTypeRepository):
        self.failure_type_repository = failure_type_repository

    def get_failure_type_by_id(self, failure_type_id: int) -> Optional[Dict]:
        """Get a failure type by ID."""
        return self.failure_type_repository.get_by_id(failure_type_id)

    def get_all_failure_types(self) -> List[Dict]:
        """Get all failure types."""
        return self.failure_type_repository.get_all()

    def create_failure_type(self, failure_type_code: str, failure_type_desc: Optional[str] = None, site_id: Optional[int] = None, failure_group_id: Optional[int] = None) -> Dict:
        """Create a new failure type."""
        return self.failure_type_repository.add(
            failure_type_code=failure_type_code,
            failure_type_desc=failure_type_desc,
            site_id=site_id,
            failure_group_id=failure_group_id
        )

    def update_failure_type(self, failure_type_id: int, failure_type_code: Optional[str] = None, 
                           failure_type_desc: Optional[str] = None, site_id: Optional[int] = None,
                           failure_group_id: Optional[int] = None) -> Optional[Dict]:
        """Update a failure type."""
        update_data = {}
        if failure_type_code is not None:
            update_data["failure_type_code"] = failure_type_code
        if failure_type_desc is not None:
            update_data["failure_type_desc"] = failure_type_desc
        if site_id is not None:
            update_data["site_id"] = site_id
        if failure_group_id is not None:
            update_data["failure_group_id"] = failure_group_id

        return self.failure_type_repository.update_failure_type(failure_type_id, **update_data)

    def delete_failure_type(self, failure_type_id: int) -> bool:
        """Delete a failure type."""
        return self.failure_type_repository.delete_by_id(failure_type_id)
    
    def get_failure_type_by_code(self, failure_type_code: str) -> Optional[Dict]:
        """Get a failure type by code."""
        return self.failure_type_repository.get_by_code(failure_type_code)
