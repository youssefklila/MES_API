# services/station_service.py

from typing import List, Optional
from webapp.ADM.machine_assets.machine_setup.station.repositories.station_repositorie import StationRepository
from webapp.ADM.machine_assets.machine_setup.station.schemas.station_schema import StationResponse
from webapp.ADM.master_data.workorder.schemas.workorder_schema import WorkOrderResponse

class StationService:
    def __init__(self, station_repository: StationRepository) -> None:
        self.station_repository = station_repository

    def get_all_stations(self) -> List[StationResponse]:
        """Get all stations."""
        stations = self.station_repository.get_all()
        return [StationResponse(**station) for station in stations]

    def get_station_by_id(self, station_id: int) -> Optional[StationResponse]:
        """Get a station by ID."""
        station = self.station_repository.get_by_id(station_id)
        if station:
            return StationResponse(**station)
        return None

    def add_station(self, machine_group_id: int, name: str, description: str, is_active: bool, user_id: int, info: str) -> StationResponse:
        """Add a new station."""
        station = self.station_repository.add(machine_group_id, name, description, is_active, user_id, info)
        return StationResponse(**station)

    def delete_station(self, station_id: int) -> bool:
        """Delete a station by ID."""
        return self.station_repository.delete_by_id(station_id)

    def update_station(self, station_id: int, **kwargs) -> Optional[StationResponse]:
        """Update a station."""
        station = self.station_repository.update_station(station_id, **kwargs)
        if station:
            return StationResponse(**station)
        return None
        
    def get_stations_by_line_name(self, line_name: str) -> List[StationResponse]:
        """Get all stations associated with a specific line name.
        
        This method retrieves all stations that have lines with the specified name assigned to them,
        regardless of the line IDs. The search is case-insensitive and ignores leading/trailing whitespace.
        
        Args:
            line_name: The name of the line to search for
            
        Returns:
            List of station response objects that have lines with the specified name assigned to them
            
        Raises:
            ValueError: If the line name is empty or None
        """
        if not line_name or not line_name.strip():
            raise ValueError("Line name cannot be empty")
            
        stations = self.station_repository.get_by_line_name(line_name)
        return [StationResponse(**station) for station in stations]

    def get_workorders_by_station_id(self, station_id: int) -> List[WorkOrderResponse]:
        workorders = self.station_repository.get_workorders_by_station_id(station_id)
        return [WorkOrderResponse.from_orm(wo) for wo in workorders]
