# endpoints/bom_header_endpoint.py

from fastapi import APIRouter, Depends, HTTPException, Security
from dependency_injector.wiring import inject, Provide
from typing import List, Dict, Any
from fastapi.security import OAuth2PasswordBearer

from webapp.ADM.bom.schemas.bom_header_schema import BomHeaderResponse, BomHeaderCreate, BomHeaderUpdate
from webapp.ADM.bom.services.bom_header_service import BomHeaderService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(
    prefix="/bom/headers",
    tags=["BOM Headers"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}}
)

# Permission constants
BOM_READ_PERM = "bom:read"
BOM_CREATE_PERM = "bom:create"
BOM_UPDATE_PERM = "bom:update"
BOM_DELETE_PERM = "bom:delete"

@router.get("/", response_model=List[BomHeaderResponse], summary="Get All BOM Headers")
@inject
def get_bom_headers(
    service: BomHeaderService = Depends(Provide[Container.bom_header_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOM_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all BOM Headers.
    
    Requires bom:read permission.
    """
    return service.get_all_bom_headers()

@router.get("/{bom_header_id}", response_model=BomHeaderResponse, summary="Get BOM Header")
@inject
def get_bom_header(
    bom_header_id: int,
    service: BomHeaderService = Depends(Provide[Container.bom_header_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOM_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific BOM Header by ID.
    
    Requires bom:read permission.
    """
    bom_header = service.get_bom_header_by_id(bom_header_id)
    if not bom_header:
        raise HTTPException(status_code=404, detail="BOM Header not found")
    return bom_header

@router.post("/", response_model=BomHeaderResponse, status_code=201, summary="Create BOM Header")
@inject
def create_bom_header(
    data: BomHeaderCreate,
    service: BomHeaderService = Depends(Provide[Container.bom_header_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOM_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new BOM Header.
    
    Requires bom:create permission.
    """
    return service.create_bom_header(data)

@router.put("/{bom_header_id}", response_model=BomHeaderResponse, summary="Update BOM Header")
@inject
def update_bom_header(
    bom_header_id: int,
    data: BomHeaderUpdate,
    service: BomHeaderService = Depends(Provide[Container.bom_header_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOM_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a BOM Header.
    
    Requires bom:update permission.
    """
    updated_bom_header = service.update_bom_header(bom_header_id, data)
    if not updated_bom_header:
        raise HTTPException(status_code=404, detail="BOM Header not found")
    return updated_bom_header

@router.delete("/{bom_header_id}", status_code=204, summary="Delete BOM Header")
@inject
def delete_bom_header(
    bom_header_id: int,
    service: BomHeaderService = Depends(Provide[Container.bom_header_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOM_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a BOM Header.
    
    Requires bom:delete permission.
    """
    success = service.delete_bom_header(bom_header_id)
    if not success:
        raise HTTPException(status_code=404, detail="BOM Header not found")
    return {"message": "BOM Header deleted successfully"}
