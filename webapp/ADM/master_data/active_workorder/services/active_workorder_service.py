"""Active Workorder service."""
from typing import List, Dict, Any, Optional
from fastapi import HTTPException

from webapp.ADM.master_data.active_workorder.repositories.active_workorder_repository import ActiveWorkorderRepository


class ActiveWorkorderService:
    """Service for Active Workorder operations."""

    def __init__(self, active_workorder_repository: ActiveWorkorderRepository):
        """Initialize service with repository."""
        self.active_workorder_repository = active_workorder_repository

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all active workorders."""
        return self.active_workorder_repository.get_all()

    def get_by_id(self, active_workorder_id: int) -> Dict[str, Any]:
        """Get active workorder by ID."""
        active_workorder = self.active_workorder_repository.get_by_id(active_workorder_id)
        if not active_workorder:
            raise HTTPException(status_code=404, detail="Active workorder not found")
        return active_workorder

    def get_by_workorder_id(self, workorder_id: int) -> List[Dict[str, Any]]:
        """Get active workorders by workorder ID."""
        return self.active_workorder_repository.get_by_workorder_id(workorder_id)

    def get_by_station_id(self, station_id: int) -> List[Dict[str, Any]]:
        """Get active workorders by station ID."""
        return self.active_workorder_repository.get_by_station_id(station_id)

    def get_by_state(self, state: int) -> List[Dict[str, Any]]:
        """Get active workorders by state."""
        if state not in [0, 1, 2, 3, 4, 5]:
            raise HTTPException(status_code=400, detail="State must be either 0, 1, 2, 3, 4, or 5")
        return self.active_workorder_repository.get_by_state(state)

    def create_active_workorder(self, workorder_id: int, station_id: int, state: int) -> Dict[str, Any]:
        """Create new active workorder."""
        if state not in [0, 1, 2, 3, 4, 5]:
            raise HTTPException(status_code=400, detail="State must be either 0, 1, 2, 3, 4, or 5")
        
        try:
            return self.active_workorder_repository.add(
                workorder_id=workorder_id,
                station_id=station_id,
                state=state
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Could not create active workorder: {str(e)}")

    def update_active_workorder(self, active_workorder_id: int, **kwargs) -> Dict[str, Any]:
        """Update active workorder."""
        if 'state' in kwargs and kwargs['state'] is not None and kwargs['state'] not in [0, 1, 2, 3, 4, 5]:
            raise HTTPException(status_code=400, detail="State must be either 0, 1, 2, 3, 4, or 5")
        
        active_workorder = self.active_workorder_repository.update(active_workorder_id, **kwargs)
        if not active_workorder:
            raise HTTPException(status_code=404, detail="Active workorder not found")
        return active_workorder

    def delete_active_workorder(self, active_workorder_id: int) -> bool:
        """Delete active workorder."""
        success = self.active_workorder_repository.delete(active_workorder_id)
        if not success:
            raise HTTPException(status_code=404, detail="Active workorder not found")
        return True
