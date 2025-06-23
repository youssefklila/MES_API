from typing import List, Dict, Any, Optional
from webapp.ADM.master_data.workplan_data.workplan_type.models.workplan_type_model import WorkPlanType
from webapp.ADM.master_data.workplan_data.workplan_type.repositories.workplan_type_repository import WorkPlanTypeRepository

class WorkPlanTypeService:
    def __init__(self, workplan_type_repository: WorkPlanTypeRepository) -> None:
        self.workplan_type_repository = workplan_type_repository

    def get_all_workplan_types(self) -> List[Dict[str, Any]]:
        """Get all workplan types"""
        return self.workplan_type_repository.get_all()

    def get_workplan_type_by_id(self, workplan_type_id: int) -> Optional[Dict[str, Any]]:
        """Get workplan type by ID"""
        return self.workplan_type_repository.get_by_id(workplan_type_id)

    def add_workplan_type(self, name: str, description: str, is_active: bool = True) -> Dict[str, Any]:
        """Add a new workplan type"""
        return self.workplan_type_repository.add(name, description, is_active)

    def delete_workplan_type(self, workplan_type_id: int) -> bool:
        """Delete workplan type by ID"""
        return self.workplan_type_repository.delete_by_id(workplan_type_id)

    def update_workplan_type(self, workplan_type_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """Update workplan type"""
        return self.workplan_type_repository.update_workplan_type(workplan_type_id, **kwargs)
