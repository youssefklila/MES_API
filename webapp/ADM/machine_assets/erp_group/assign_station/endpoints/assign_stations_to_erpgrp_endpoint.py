# endpoints/assign_stations_to_erpgrp_endpoint.py

from fastapi import APIRouter, Depends, HTTPException, Security
from typing import List, Dict, Any
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordBearer

from webapp.ADM.machine_assets.erp_group.assign_station.schemas.assign_stations_to_erpgrp_schema import (
    AssignStationsToErpGrpCreate,
    AssignStationsToErpGrpResponse,
)
from webapp.ADM.machine_assets.erp_group.assign_station.services.assign_stations_to_erpgrp_service import AssignStationsToErpGrpService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(
    prefix="/assign-stations-to-erpgrp",
    tags=["Station Assignments"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}}
)

# Permission constants
ASSIGN_STATION_READ_PERM = "assign_station:read"
ASSIGN_STATION_CREATE_PERM = "assign_station:create"
ASSIGN_STATION_DELETE_PERM = "assign_station:delete"

@router.get("/", response_model=List[AssignStationsToErpGrpResponse], summary="Get All Station Assignments")
@inject
def get_assignments(
    assign_stations_to_erpgrp_service: AssignStationsToErpGrpService = Depends(
        Provide[Container.assign_stations_to_erpgrp_service]
    ),
    current_user: Dict[str, Any] = Depends(permission_required(ASSIGN_STATION_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all station assignments.
    
    Requires assign_station:read permission.
    """
    return assign_stations_to_erpgrp_service.get_all_assignments()

@router.get("/{assign_id}", response_model=AssignStationsToErpGrpResponse, summary="Get Station Assignment")
@inject
def get_assignment(
    assign_id: int,
    assign_stations_to_erpgrp_service: AssignStationsToErpGrpService = Depends(
        Provide[Container.assign_stations_to_erpgrp_service]
    ),
    current_user: Dict[str, Any] = Depends(permission_required(ASSIGN_STATION_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific station assignment by ID.
    
    Requires assign_station:read permission.
    """
    assignment = assign_stations_to_erpgrp_service.get_assignment_by_id(assign_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment

@router.get("/station/{station_id}", response_model=List[AssignStationsToErpGrpResponse], summary="Get Station Assignments by Station")
@inject
def get_assignments_by_station(
    station_id: int,
    assign_stations_to_erpgrp_service: AssignStationsToErpGrpService = Depends(
        Provide[Container.assign_stations_to_erpgrp_service]
    ),
    current_user: Dict[str, Any] = Depends(permission_required(ASSIGN_STATION_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all assignments for a specific station.
    
    Requires assign_station:read permission.
    """
    return assign_stations_to_erpgrp_service.get_assignments_by_station_id(station_id)

@router.post("/", response_model=AssignStationsToErpGrpResponse, status_code=201, summary="Create Station Assignment")
@inject
def create_assignment(
    assignment_data: AssignStationsToErpGrpCreate,
    assign_stations_to_erpgrp_service: AssignStationsToErpGrpService = Depends(
        Provide[Container.assign_stations_to_erpgrp_service]
    ),
    current_user: Dict[str, Any] = Depends(permission_required(ASSIGN_STATION_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new station assignment.
    
    Requires assign_station:create permission.
    """
    return assign_stations_to_erpgrp_service.add_assignment(**assignment_data.dict())

@router.delete("/{assign_id}", status_code=204, summary="Delete Station Assignment")
@inject
def delete_assignment(
    assign_id: int,
    assign_stations_to_erpgrp_service: AssignStationsToErpGrpService = Depends(
        Provide[Container.assign_stations_to_erpgrp_service]
    ),
    current_user: Dict[str, Any] = Depends(permission_required(ASSIGN_STATION_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a station assignment.
    
    Requires assign_station:delete permission.
    """
    success = assign_stations_to_erpgrp_service.delete_assignment(assign_id)
    if not success:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return {"message": "Assignment deleted successfully"}
