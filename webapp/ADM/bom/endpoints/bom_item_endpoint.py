# endpoints/bom_item_endpoint.py

from fastapi import APIRouter, Depends, HTTPException, Security
from dependency_injector.wiring import inject, Provide
from typing import List, Dict, Any
from fastapi.security import OAuth2PasswordBearer

from webapp.ADM.bom.schemas.bom_item_schema import BomItemResponse, BomItemCreate, BomItemUpdate
from webapp.ADM.bom.services.bom_item_service import BomItemService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(
    prefix="/bom/items",
    tags=["BOM Items"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}}
)

# Permission constants
BOM_READ_PERM = "bom:read"
BOM_CREATE_PERM = "bom:create"
BOM_UPDATE_PERM = "bom:update"
BOM_DELETE_PERM = "bom:delete"

@router.get("/", response_model=List[BomItemResponse], summary="Get All BOM Items")
@inject
def get_bom_items(
    service: BomItemService = Depends(Provide[Container.bom_item_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOM_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all BOM Items.
    
    Requires bom:read permission.
    """
    return service.get_all_bom_items()

@router.get("/header/{bom_header_id}", response_model=List[BomItemResponse], summary="Get BOM Items by Header ID")
@inject
def get_bom_items_by_header(
    bom_header_id: int,
    service: BomItemService = Depends(Provide[Container.bom_item_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOM_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all BOM Items for a specific BOM Header.
    
    Requires bom:read permission.
    """
    return service.get_bom_items_by_header_id(bom_header_id)

@router.get("/{bom_item_id}", response_model=BomItemResponse, summary="Get BOM Item")
@inject
def get_bom_item(
    bom_item_id: int,
    service: BomItemService = Depends(Provide[Container.bom_item_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOM_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific BOM Item by ID.
    
    Requires bom:read permission.
    """
    bom_item = service.get_bom_item_by_id(bom_item_id)
    if not bom_item:
        raise HTTPException(status_code=404, detail="BOM Item not found")
    return bom_item

@router.post("/", response_model=BomItemResponse, status_code=201, summary="Create BOM Item")
@inject
def create_bom_item(
    data: BomItemCreate,
    service: BomItemService = Depends(Provide[Container.bom_item_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOM_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new BOM Item.
    
    Requires bom:create permission.
    """
    return service.create_bom_item(data)

@router.put("/{bom_item_id}", response_model=BomItemResponse, summary="Update BOM Item")
@inject
def update_bom_item(
    bom_item_id: int,
    data: BomItemUpdate,
    service: BomItemService = Depends(Provide[Container.bom_item_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOM_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a BOM Item.
    
    Requires bom:update permission.
    """
    updated_bom_item = service.update_bom_item(bom_item_id, data)
    if not updated_bom_item:
        raise HTTPException(status_code=404, detail="BOM Item not found")
    return updated_bom_item

@router.delete("/{bom_item_id}", status_code=204, summary="Delete BOM Item")
@inject
def delete_bom_item(
    bom_item_id: int,
    service: BomItemService = Depends(Provide[Container.bom_item_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOM_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a BOM Item.
    
    Requires bom:delete permission.
    """
    success = service.delete_bom_item(bom_item_id)
    if not success:
        raise HTTPException(status_code=404, detail="BOM Item not found")
    return {"message": "BOM Item deleted successfully"}
