# endpoints/bom_endpoint.py

from fastapi import APIRouter, Depends, HTTPException, Security
from dependency_injector.wiring import inject, Provide
from typing import List, Dict, Any
from fastapi.security import OAuth2PasswordBearer

from webapp.ADM.bom.schemas.bom_schema import BomResponse, BomCreate, BomUpdate
from webapp.ADM.bom.services.bom_service import BomService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(
    prefix="/bom",
    tags=["BOM"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}}
)

# Permission constants
BOM_READ_PERM = "bom:read"
BOM_CREATE_PERM = "bom:create"
BOM_UPDATE_PERM = "bom:update"
BOM_DELETE_PERM = "bom:delete"

@router.get("/", response_model=List[BomResponse], summary="Get All BOMs")
@inject
def get_boms(
    service: BomService = Depends(Provide[Container.bom_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOM_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all BOMs.
    
    Requires bom:read permission.
    """
    return service.get_all_boms()

@router.get("/{bom_id}", response_model=BomResponse, summary="Get BOM")
@inject
def get_bom(
    bom_id: int,
    service: BomService = Depends(Provide[Container.bom_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOM_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific BOM by ID.
    
    Requires bom:read permission.
    """
    bom = service.get_bom_by_id(bom_id)
    if not bom:
        raise HTTPException(status_code=404, detail="BOM not found")
    return bom

@router.post("/", response_model=BomResponse, status_code=201, summary="Create BOM")
@inject
def create_bom(
    data: BomCreate,
    service: BomService = Depends(Provide[Container.bom_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOM_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new BOM.
    
    Requires bom:create permission.
    """
    return service.add_bom(**data.dict())

@router.put("/{bom_id}", response_model=BomResponse, summary="Update BOM")
@inject
def update_bom(
    bom_id: int,
    data: BomUpdate,
    service: BomService = Depends(Provide[Container.bom_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOM_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a BOM.
    
    Requires bom:update permission.
    """
    updated_bom = service.update_bom(bom_id, **data.dict(exclude_unset=True))
    if not updated_bom:
        raise HTTPException(status_code=404, detail="BOM not found")
    return updated_bom

@router.delete("/{bom_id}", status_code=204, summary="Delete BOM")
@inject
def delete_bom(
    bom_id: int,
    service: BomService = Depends(Provide[Container.bom_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOM_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a BOM.
    
    Requires bom:delete permission.
    """
    success = service.delete_bom(bom_id)
    if not success:
        raise HTTPException(status_code=404, detail="BOM not found")
    return {"message": "BOM deleted successfully"} 