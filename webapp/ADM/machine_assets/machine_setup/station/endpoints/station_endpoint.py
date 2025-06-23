# endpoints/station_endpoint.py

from fastapi import APIRouter, Depends, HTTPException, Security
from typing import List, Dict, Any
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordBearer

from webapp.ADM.machine_assets.machine_setup.station.schemas.station_schema import StationCreate, StationUpdate, StationResponse
from webapp.ADM.master_data.workorder.schemas.workorder_schema import WorkOrderResponse
from webapp.ADM.machine_assets.machine_setup.station.services.station_service import StationService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

router = APIRouter(
    prefix="/stations",
    tags=["Stations"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}}
)

# Permission constants
STATION_READ_PERM = "station:read"
STATION_CREATE_PERM = "station:create"
STATION_UPDATE_PERM = "station:update"
STATION_DELETE_PERM = "station:delete"

@router.get("/", response_model=List[StationResponse], summary="Get All Stations")
@inject
def get_stations(
    station_service: StationService = Depends(Provide[Container.station_service]),
    current_user: Dict[str, Any] = Depends(permission_required(STATION_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all stations.
    
    Requires station:read permission.
    """
    return station_service.get_all_stations()

@router.get("/{station_id}", response_model=StationResponse, summary="Get Station")
@inject
def get_station(
    station_id: int,
    station_service: StationService = Depends(Provide[Container.station_service]),
    current_user: Dict[str, Any] = Depends(permission_required(STATION_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific station by ID.
    
    Requires station:read permission.
    """
    station = station_service.get_station_by_id(station_id)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    return station

@router.post("/", response_model=StationResponse, status_code=201, summary="Create Station")
@inject
def create_station(
    station_data: StationCreate,
    station_service: StationService = Depends(Provide[Container.station_service]),
    current_user: Dict[str, Any] = Depends(permission_required(STATION_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new station.
    
    Requires station:create permission.
    """
    return station_service.add_station(**station_data.dict())

@router.put("/{station_id}", response_model=StationResponse, summary="Update Station")
@inject
def update_station(
    station_id: int,
    station_data: StationUpdate,
    station_service: StationService = Depends(Provide[Container.station_service]),
    current_user: Dict[str, Any] = Depends(permission_required(STATION_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a station.
    
    Requires station:update permission.
    """
    updated_station = station_service.update_station(station_id, **station_data.dict())
    if not updated_station:
        raise HTTPException(status_code=404, detail="Station not found")
    return updated_station

@router.delete("/{station_id}", status_code=204, summary="Delete Station")
@inject
def delete_station(
    station_id: int,
    station_service: StationService = Depends(Provide[Container.station_service]),
    current_user: Dict[str, Any] = Depends(permission_required(STATION_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a station.
    
    Requires station:delete permission.
    """
    success = station_service.delete_station(station_id)
    if not success:
        raise HTTPException(status_code=404, detail="Station not found")
    return {"message": "Station deleted successfully"}

@router.get("/line/name/{line_name}", response_model=List[StationResponse], summary="Get Stations By Line Name")
@inject
def get_stations_by_line_name(
    line_name: str,
    station_service: StationService = Depends(Provide[Container.station_service]),
    current_user: Dict[str, Any] = Depends(permission_required(STATION_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all stations associated with a specific line name, regardless of line IDs.
    
    This endpoint retrieves all stations that have lines with the specified name assigned to them,
    even if the lines have different IDs. The search is case-insensitive and ignores
    leading/trailing whitespace.
    
    Args:
        line_name: The name of the line to search for
    
    Returns:
        List of station objects that have lines with the specified name assigned to them
    
    Raises:
        400 Bad Request: If the line name is empty
        404 Not Found: If no stations are found with the specified line name
    
    Requires station:read permission.
    """
    try:
        stations = station_service.get_stations_by_line_name(line_name)
        if not stations:
            raise HTTPException(status_code=404, detail=f"No stations found with line name: {line_name}")
        return stations
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{station_id}/workorders", response_model=List[WorkOrderResponse], summary="Get Work Orders By Station")
@inject
def get_workorders_by_station(
    station_id: int,
    station_service: StationService = Depends(Provide[Container.station_service]),
    current_user: Dict[str, Any] = Depends(permission_required(STATION_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all work orders for a specific station.
    
    Requires station:read permission.
    """
    try:
        return station_service.get_workorders_by_station_id(station_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
