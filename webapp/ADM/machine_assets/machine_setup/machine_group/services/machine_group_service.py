# services/machine_group_service.py
from typing import List, Dict, Any, Optional

from webapp.ADM.machine_assets.machine_setup.machine_group.models.machine_group_model import MachineGroup
from webapp.ADM.machine_assets.machine_setup.machine_group.repositories.machine_group_repositorie import MachineGroupRepository
from webapp.ADM.machine_assets.machine_setup.machine_group.schemas.machine_group_schema import MachineGroup as MachineGroupResponse


class MachineGroupService:
    def __init__(self, machine_group_repository: MachineGroupRepository):
        self.machine_group_repository = machine_group_repository

    def create_machine_group(self, name: str, description: str, user_id: int, cell_id: int, is_active: bool, failure: bool) -> MachineGroupResponse:
        """Create a new machine group."""
        machine_group = self.machine_group_repository.add(name, description, user_id, cell_id, is_active, failure)
        return MachineGroupResponse(**machine_group)

    def get_machine_group_by_id(self, machine_group_id: int) -> Optional[MachineGroupResponse]:
        """Get a machine group by ID."""
        machine_group = self.machine_group_repository.get_by_id(machine_group_id)
        if machine_group:
            return MachineGroupResponse(**machine_group)
        return None

    def get_all_machine_groups(self) -> List[MachineGroupResponse]:
        """Get all machine groups."""
        machine_groups = self.machine_group_repository.get_all()
        return [MachineGroupResponse(**mg) for mg in machine_groups]

    def update_machine_group(self, machine_group_id: int, name: str, description: str, is_active: bool, failure: bool) -> Optional[MachineGroupResponse]:
        """Update a machine group."""
        machine_group = self.machine_group_repository.update(machine_group_id, name, description, is_active, failure)
        if machine_group:
            return MachineGroupResponse(**machine_group)
        return None

    def delete_machine_group(self, machine_group_id: int) -> Dict[str, Any]:
        """
        Delete a machine group.
        
        Returns:
            Dict with success status and message. If deletion fails due to associated stations,
            returns {'success': False, 'reason': 'has_stations'}. If machine group not found,
            returns {'success': False, 'reason': 'not_found'}.
        """
        result = self.machine_group_repository.delete(machine_group_id)
        if result is False:
            # Check if the machine group exists
            machine_group = self.machine_group_repository.get_by_id(machine_group_id)
            if machine_group:
                # Machine group exists but couldn't be deleted (has stations)
                return {"success": False, "reason": "has_stations"}
            else:
                # Machine group doesn't exist
                return {"success": False, "reason": "not_found"}
        return {"success": True}
