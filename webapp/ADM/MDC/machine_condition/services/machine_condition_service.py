"""Machine Condition service."""
from typing import List, Dict, Any, Optional
from webapp.ADM.MDC.machine_condition.repositories.machine_condition_repository import MachineConditionRepository


class MachineConditionService:
    """Service for Machine Condition operations."""

    def __init__(self, repository: MachineConditionRepository) -> None:
        """Initialize service with repository."""
        self.repository = repository

    def get_all_conditions(self) -> List[Dict[str, Any]]:
        """Get all machine conditions."""
        return self.repository.get_all()

    def get_condition_by_id(self, condition_id: int) -> Optional[Dict[str, Any]]:
        """Get machine condition by ID."""
        return self.repository.get_by_id(condition_id)

    def get_condition_by_name(self, condition_name: str) -> Optional[Dict[str, Any]]:
        """Get machine condition by name."""
        return self.repository.get_by_name(condition_name)

    def get_conditions_by_group_id(self, group_id: int) -> List[Dict[str, Any]]:
        """Get all machine conditions for a specific group."""
        return self.repository.get_by_group_id(group_id)

    def create_condition(self, group_id: int, condition_name: str, condition_description: str = None, 
                         color_rgb: int = None, is_active: bool = True) -> Dict[str, Any]:
        """Create a new machine condition."""
        return self.repository.add(
            group_id=group_id,
            condition_name=condition_name,
            condition_description=condition_description,
            color_rgb=color_rgb,
            is_active=is_active
        )

    def update_condition(self, condition_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """Update a machine condition."""
        return self.repository.update(condition_id, **kwargs)

    def delete_condition(self, condition_id: int) -> bool:
        """Delete a machine condition."""
        return self.repository.delete(condition_id)
