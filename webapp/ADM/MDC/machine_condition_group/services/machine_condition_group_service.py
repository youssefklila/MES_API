"""Machine Condition Group service."""
from typing import List, Dict, Any, Optional
from webapp.ADM.MDC.machine_condition_group.repositories.machine_condition_group_repository import MachineConditionGroupRepository


class MachineConditionGroupService:
    """Service for Machine Condition Group operations."""

    def __init__(self, repository: MachineConditionGroupRepository) -> None:
        """Initialize service with repository."""
        self.repository = repository

    def get_all_groups(self) -> List[Dict[str, Any]]:
        """Get all machine condition groups."""
        return self.repository.get_all()

    def get_group_by_id(self, group_id: int) -> Optional[Dict[str, Any]]:
        """Get machine condition group by ID."""
        return self.repository.get_by_id(group_id)

    def get_group_by_name(self, group_name: str) -> Optional[Dict[str, Any]]:
        """Get machine condition group by name."""
        return self.repository.get_by_name(group_name)

    def create_group(self, group_name: str, group_description: str = None, is_active: bool = True) -> Dict[str, Any]:
        """Create a new machine condition group."""
        return self.repository.add(
            group_name=group_name,
            group_description=group_description,
            is_active=is_active
        )

    def update_group(self, group_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """Update a machine condition group."""
        return self.repository.update(group_id, **kwargs)

    def delete_group(self, group_id: int) -> bool:
        """Delete a machine condition group."""
        return self.repository.delete(group_id)
