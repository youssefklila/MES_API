"""Active Workorder endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from dependency_injector.wiring import inject, Provide

from webapp.ADM.master_data.active_workorder.schemas.active_workorder_schema import (
    ActiveWorkorderCreate,
    ActiveWorkorderUpdate,
    ActiveWorkorderResponse
)
from webapp.ADM.master_data.active_workorder.services.active_workorder_service import ActiveWorkorderService
from webapp.auth.dependencies import permission_required, oauth2_scheme

router = APIRouter(
    prefix="/active-workorders",
    tags=["active-workorders"],
    responses={404: {"description": "Not found"}}
)

# Permission constants
ACTIVE_WORKORDER_READ_PERM = "active_workorder:read"
ACTIVE_WORKORDER_CREATE_PERM = "active_workorder:create"
ACTIVE_WORKORDER_UPDATE_PERM = "active_workorder:update"
ACTIVE_WORKORDER_DELETE_PERM = "active_workorder:delete"


@router.get("/", response_model=List[ActiveWorkorderResponse], summary="Get All Active Workorders")
@inject
def get_all_active_workorders(
    service: ActiveWorkorderService = Depends(Provide["active_workorder_service"]),
    _=Depends(permission_required(ACTIVE_WORKORDER_READ_PERM))
):
    """
    Get all active workorders.
    
    Requires permission: active_workorder:read
    """
    return service.get_all()


@router.get("/{active_workorder_id}", response_model=ActiveWorkorderResponse, summary="Get Active Workorder by ID")
@inject
def get_active_workorder_by_id(
    active_workorder_id: int,
    service: ActiveWorkorderService = Depends(Provide["active_workorder_service"]),
    _=Depends(permission_required(ACTIVE_WORKORDER_READ_PERM))
):
    """
    Get active workorder by ID.
    
    Requires permission: active_workorder:read
    """
    return service.get_by_id(active_workorder_id)


@router.get("/workorder/{workorder_id}", response_model=List[ActiveWorkorderResponse], summary="Get Active Workorders by Workorder ID")
@inject
def get_active_workorders_by_workorder_id(
    workorder_id: int,
    service: ActiveWorkorderService = Depends(Provide["active_workorder_service"]),
    _=Depends(permission_required(ACTIVE_WORKORDER_READ_PERM))
):
    """
    Get active workorders by workorder ID.
    
    Requires permission: active_workorder:read
    """
    return service.get_by_workorder_id(workorder_id)


@router.get("/station/{station_id}", response_model=List[ActiveWorkorderResponse], summary="Get Active Workorders by Station ID")
@inject
def get_active_workorders_by_station_id(
    station_id: int,
    service: ActiveWorkorderService = Depends(Provide["active_workorder_service"]),
    _=Depends(permission_required(ACTIVE_WORKORDER_READ_PERM))
):
    """
    Get active workorders by station ID.
    
    Requires permission: active_workorder:read
    """
    return service.get_by_station_id(station_id)


@router.get("/state/{state}", response_model=List[ActiveWorkorderResponse], summary="Get Active Workorders by State")
@inject
def get_active_workorders_by_state(
    state: int,
    service: ActiveWorkorderService = Depends(Provide["active_workorder_service"]),
    _=Depends(permission_required(ACTIVE_WORKORDER_READ_PERM))
):
    """
    Get active workorders by state (0 or 1).
    
    Requires permission: active_workorder:read
    """
    return service.get_by_state(state)


@router.post("/", response_model=ActiveWorkorderResponse, summary="Create Active Workorder")
@inject
def create_active_workorder(
    data: ActiveWorkorderCreate,
    service: ActiveWorkorderService = Depends(Provide["active_workorder_service"]),
    _=Depends(permission_required(ACTIVE_WORKORDER_CREATE_PERM))
):
    """
    Create a new active workorder.
    
    Requires permission: active_workorder:create
    """
    return service.create_active_workorder(
        workorder_id=data.workorder_id,
        station_id=data.station_id,
        state=data.state
    )


@router.put("/{active_workorder_id}", response_model=ActiveWorkorderResponse, summary="Update Active Workorder")
@inject
def update_active_workorder(
    active_workorder_id: int,
    data: ActiveWorkorderUpdate,
    service: ActiveWorkorderService = Depends(Provide["active_workorder_service"]),
    _=Depends(permission_required(ACTIVE_WORKORDER_UPDATE_PERM))
):
    """
    Update an active workorder.
    
    Requires permission: active_workorder:update
    """
    update_data = data.dict(exclude_unset=True)
    return service.update_active_workorder(active_workorder_id, **update_data)


@router.delete("/{active_workorder_id}", summary="Delete Active Workorder")
@inject
def delete_active_workorder(
    active_workorder_id: int,
    service: ActiveWorkorderService = Depends(Provide["active_workorder_service"]),
    _=Depends(permission_required(ACTIVE_WORKORDER_DELETE_PERM))
):
    """
    Delete an active workorder.
    
    Requires permission: active_workorder:delete
    """
    service.delete_active_workorder(active_workorder_id)
    return {"message": "Active workorder deleted successfully"}
