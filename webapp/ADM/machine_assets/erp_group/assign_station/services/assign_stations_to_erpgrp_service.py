# services/assign_stations_to_erpgrp_service.py

from typing import List, Optional
from webapp.ADM.machine_assets.erp_group.assign_station.repositories.assign_stations_to_erpgrp_repository import AssignStationsToErpGrpRepository
from webapp.ADM.machine_assets.erp_group.assign_station.schemas.assign_stations_to_erpgrp_schema import AssignStationsToErpGrpResponse

class AssignStationsToErpGrpService:
    def __init__(self, assign_stations_to_erpgrp_repository: AssignStationsToErpGrpRepository) -> None:
        self.assign_stations_to_erpgrp_repository = assign_stations_to_erpgrp_repository

    def get_all_assignments(self) -> List[AssignStationsToErpGrpResponse]:
        """Get all station assignments."""
        assignments = self.assign_stations_to_erpgrp_repository.get_all()
        return [AssignStationsToErpGrpResponse(**assignment) for assignment in assignments]

    def get_assignment_by_id(self, assign_id: int) -> Optional[AssignStationsToErpGrpResponse]:
        """Get a station assignment by ID."""
        assignment = self.assign_stations_to_erpgrp_repository.get_by_id(assign_id)
        if assignment:
            return AssignStationsToErpGrpResponse(**assignment)
        return None

    def get_assignments_by_station_id(self, station_id: int) -> List[AssignStationsToErpGrpResponse]:
        """Get all assignments for a specific station."""
        assignments = self.assign_stations_to_erpgrp_repository.get_by_station_id(station_id)
        return [AssignStationsToErpGrpResponse(**assignment) for assignment in assignments]

    def add_assignment(self, station_id: int, erp_group_id: int, station_type: str, user_id: int) -> AssignStationsToErpGrpResponse:
        """Add a new station assignment."""
        assignment = self.assign_stations_to_erpgrp_repository.add(station_id, erp_group_id, station_type, user_id)
        return AssignStationsToErpGrpResponse(**assignment)

    def delete_assignment(self, assign_id: int) -> bool:
        """Delete a station assignment."""
        return self.assign_stations_to_erpgrp_repository.delete_by_id(assign_id)
