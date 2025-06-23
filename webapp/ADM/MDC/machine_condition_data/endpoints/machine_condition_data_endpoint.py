"""Machine Condition Data endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Security, status, Query
from typing import List, Dict, Any, Optional
from datetime import datetime
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordBearer

from webapp.ADM.MDC.machine_condition_data.schemas.machine_condition_data_schema import (
    MachineConditionDataCreate,
    MachineConditionDataUpdate,
    MachineConditionDataResponse
)
from webapp.ADM.MDC.machine_condition_data.services.machine_condition_data_service import MachineConditionDataService
from webapp.ADM.MDC.machine_condition.services.machine_condition_service import MachineConditionService
from webapp.ADM.machine_assets.machine_setup.station.services.station_service import StationService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(
    prefix="/machine-condition-data",
    tags=["Machine Condition Data"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}, 404: {"description": "Not found"}}
)

# Permission constants
MCD_READ_PERM = "machine_condition_data:read"
MCD_CREATE_PERM = "machine_condition_data:create"
MCD_UPDATE_PERM = "machine_condition_data:update"
MCD_DELETE_PERM = "machine_condition_data:delete"

@router.get("/", response_model=List[MachineConditionDataResponse], summary="Get All Machine Condition Data")
@inject
def get_all_condition_data(
    service: MachineConditionDataService = Depends(Provide[Container.machine_condition_data_service]),
    current_user: Dict[str, Any] = Depends(permission_required(MCD_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all machine condition data records.
    
    Requires machine_condition_data:read permission.
    """
    return service.get_all_condition_data()

@router.get("/station/{station_id}", response_model=List[MachineConditionDataResponse], summary="Get Condition Data by Station")
@inject
def get_condition_data_by_station(
    station_id: int,
    service: MachineConditionDataService = Depends(Provide[Container.machine_condition_data_service]),
    station_service: StationService = Depends(Provide[Container.station_service]),
    current_user: Dict[str, Any] = Depends(permission_required(MCD_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all machine condition data for a specific station.
    
    Requires machine_condition_data:read permission.
    """
    # Check if the station exists
    station = station_service.get_station_by_id(station_id)
    if not station:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Station not found")
    
    return service.get_condition_data_by_station(station_id)

@router.get("/condition/{condition_id}", response_model=List[MachineConditionDataResponse], summary="Get Condition Data by Condition")
@inject
def get_condition_data_by_condition(
    condition_id: int,
    service: MachineConditionDataService = Depends(Provide[Container.machine_condition_data_service]),
    condition_service: MachineConditionService = Depends(Provide[Container.machine_condition_service]),
    current_user: Dict[str, Any] = Depends(permission_required(MCD_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all machine condition data for a specific condition.
    
    Requires machine_condition_data:read permission.
    """
    # Check if the condition exists
    condition = condition_service.get_condition_by_id(condition_id)
    if not condition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine condition not found")
    
    return service.get_condition_data_by_condition(condition_id)

@router.get("/date-range", response_model=List[MachineConditionDataResponse], summary="Get Condition Data by Date Range")
@inject
def get_condition_data_by_date_range(
    start_date: datetime = Query(..., description="Start date for the range"),
    end_date: datetime = Query(..., description="End date for the range"),
    service: MachineConditionDataService = Depends(Provide[Container.machine_condition_data_service]),
    current_user: Dict[str, Any] = Depends(permission_required(MCD_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all machine condition data within a date range.
    
    Requires machine_condition_data:read permission.
    """
    return service.get_condition_data_by_date_range(start_date, end_date)

@router.get("/{data_id}", response_model=MachineConditionDataResponse, summary="Get Machine Condition Data")
@inject
def get_condition_data_by_id(
    data_id: int,
    service: MachineConditionDataService = Depends(Provide[Container.machine_condition_data_service]),
    current_user: Dict[str, Any] = Depends(permission_required(MCD_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific machine condition data record by ID.
    
    Requires machine_condition_data:read permission.
    """
    data = service.get_condition_data_by_id(data_id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine condition data not found")
    return data

@router.post("/", response_model=MachineConditionDataResponse, status_code=status.HTTP_201_CREATED, summary="Create Machine Condition Data")
@inject
def create_condition_data(
    data: MachineConditionDataCreate,
    service: MachineConditionDataService = Depends(Provide[Container.machine_condition_data_service]),
    station_service: StationService = Depends(Provide[Container.station_service]),
    condition_service: MachineConditionService = Depends(Provide[Container.machine_condition_service]),
    current_user: Dict[str, Any] = Depends(permission_required(MCD_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new machine condition data record.
    
    Requires machine_condition_data:create permission.
    """
    # Check if the station exists
    station = station_service.get_station_by_id(data.station_id)
    if not station:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Station with ID {data.station_id} does not exist"
        )
    
    # Check if the condition exists
    condition = condition_service.get_condition_by_id(data.condition_id)
    if not condition:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Machine condition with ID {data.condition_id} does not exist"
        )
    
    return service.create_condition_data(
        date_from=data.date_from,
        date_to=data.date_to,
        station_id=data.station_id,
        condition_id=data.condition_id,
        color_rgb=data.color_rgb,
        level=data.level,
        condition_stamp=data.condition_stamp,
        condition_type=data.condition_type
    )

@router.put("/{data_id}", response_model=MachineConditionDataResponse, summary="Update Machine Condition Data")
@inject
def update_condition_data(
    data_id: int,
    data: MachineConditionDataUpdate,
    service: MachineConditionDataService = Depends(Provide[Container.machine_condition_data_service]),
    station_service: StationService = Depends(Provide[Container.station_service]),
    condition_service: MachineConditionService = Depends(Provide[Container.machine_condition_service]),
    current_user: Dict[str, Any] = Depends(permission_required(MCD_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a machine condition data record.
    
    Requires machine_condition_data:update permission.
    """
    # Check if the data exists
    existing_data = service.get_condition_data_by_id(data_id)
    if not existing_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine condition data not found")
    
    # If station_id is provided, check if the station exists
    if data.station_id is not None:
        station = station_service.get_station_by_id(data.station_id)
        if not station:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Station with ID {data.station_id} does not exist"
            )
    
    # If condition_id is provided, check if the condition exists
    if data.condition_id is not None:
        condition = condition_service.get_condition_by_id(data.condition_id)
        if not condition:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Machine condition with ID {data.condition_id} does not exist"
            )
    
    updated_data = service.update_condition_data(
        data_id=data_id,
        date_from=data.date_from,
        date_to=data.date_to,
        station_id=data.station_id,
        condition_id=data.condition_id,
        color_rgb=data.color_rgb,
        level=data.level,
        condition_stamp=data.condition_stamp,
        condition_type=data.condition_type
    )
    
    if not updated_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine condition data not found")
    
    return updated_data

@router.delete("/{data_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Machine Condition Data")
@inject
def delete_condition_data(
    data_id: int,
    service: MachineConditionDataService = Depends(Provide[Container.machine_condition_data_service]),
    current_user: Dict[str, Any] = Depends(permission_required(MCD_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a machine condition data record.
    
    Requires machine_condition_data:delete permission.
    """
    # Check if the data exists
    existing_data = service.get_condition_data_by_id(data_id)
    if not existing_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine condition data not found")
    
    success = service.delete_condition_data(data_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete machine condition data")
    
    return None
