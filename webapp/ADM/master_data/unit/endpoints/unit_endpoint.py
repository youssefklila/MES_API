# endpoints/unit_endpoint.py

from fastapi import APIRouter, Depends, HTTPException, Security
from typing import List, Dict, Any
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordBearer

from webapp.ADM.master_data.unit.schemas.unit_schema import UnitCreate, UnitUpdate, UnitResponse
from webapp.ADM.master_data.unit.services.unit_service import UnitService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

router = APIRouter(
    prefix="/units",
    tags=["Units"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}}
)

# Permission constants
UNIT_READ_PERM = "unit:read"
UNIT_CREATE_PERM = "unit:create"
UNIT_UPDATE_PERM = "unit:update"
UNIT_DELETE_PERM = "unit:delete"

@router.get("/", response_model=List[UnitResponse], summary="Get All Units")
@inject
def get_units(
    unit_service: UnitService = Depends(Provide[Container.unit_service]),
    current_user: Dict[str, Any] = Depends(permission_required(UNIT_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all units.
    
    Requires unit:read permission.
    """
    return unit_service.get_all_units()

@router.get("/{unit_id}", response_model=UnitResponse, summary="Get Unit")
@inject
def get_unit(
    unit_id: int,
    unit_service: UnitService = Depends(Provide[Container.unit_service]),
    current_user: Dict[str, Any] = Depends(permission_required(UNIT_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific unit by ID.
    
    Requires unit:read permission.
    """
    unit = unit_service.get_unit_by_id(unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return unit

@router.post("/", response_model=UnitResponse, status_code=201, summary="Create Unit")
@inject
def create_unit(
    unit_data: UnitCreate,
    unit_service: UnitService = Depends(Provide[Container.unit_service]),
    current_user: Dict[str, Any] = Depends(permission_required(UNIT_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new unit.
    
    Requires unit:create permission.
    """
    return unit_service.add_unit(**unit_data.dict())

@router.put("/{unit_id}", response_model=UnitResponse, summary="Update Unit")
@inject
def update_unit(
    unit_id: int,
    unit_data: UnitUpdate,
    unit_service: UnitService = Depends(Provide[Container.unit_service]),
    current_user: Dict[str, Any] = Depends(permission_required(UNIT_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a unit.
    
    Requires unit:update permission.
    """
    updated_unit = unit_service.update_unit(unit_id, **unit_data.dict())
    if not updated_unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return updated_unit

@router.delete("/{unit_id}", status_code=204, summary="Delete Unit")
@inject
def delete_unit(
    unit_id: int,
    unit_service: UnitService = Depends(Provide[Container.unit_service]),
    current_user: Dict[str, Any] = Depends(permission_required(UNIT_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a unit.
    
    Requires unit:delete permission.
    """
    success = unit_service.delete_unit(unit_id)
    if not success:
        raise HTTPException(status_code=404, detail="Unit not found")
    return {"message": "Unit deleted successfully"}
