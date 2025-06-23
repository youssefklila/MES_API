# endpoints/local_storage_endpoint.py

from fastapi import APIRouter, Depends, HTTPException, Security
from dependency_injector.wiring import inject, Provide
from typing import List, Dict, Any
from fastapi.security import OAuth2PasswordBearer

from webapp.ADM.maintenance.localStorage.schemas.local_storage_schema import (
    LocalStorageResponse, 
    LocalStorageCreate, 
    LocalStorageUpdate
)
from webapp.ADM.maintenance.localStorage.services.local_storage_service import LocalStorageService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(
    prefix="/maintenance/localStorage",
    tags=["Maintenance LocalStorage"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}}
)

# Permission constants
STORAGE_READ_PERM = "maintenance:localStorage:read"
STORAGE_CREATE_PERM = "maintenance:localStorage:create"
STORAGE_UPDATE_PERM = "maintenance:localStorage:update"
STORAGE_DELETE_PERM = "maintenance:localStorage:delete"

@router.get("/", response_model=List[LocalStorageResponse], summary="Get All LocalStorage Items")
@inject
def get_all_items(
    service: LocalStorageService = Depends(Provide[Container.maintenance_local_storage_service]),
    current_user: Dict[str, Any] = Depends(permission_required(STORAGE_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all localStorage items.
    
    Requires maintenance:localStorage:read permission.
    """
    return service.get_all_items()

@router.get("/{item_id}", response_model=LocalStorageResponse, summary="Get LocalStorage Item by ID")
@inject
def get_item_by_id(
    item_id: int,
    service: LocalStorageService = Depends(Provide[Container.maintenance_local_storage_service]),
    current_user: Dict[str, Any] = Depends(permission_required(STORAGE_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific localStorage item by ID.
    
    Requires maintenance:localStorage:read permission.
    """
    item = service.get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="LocalStorage item not found")
    return item

@router.get("/key/{key}", response_model=LocalStorageResponse, summary="Get LocalStorage Item by Key")
@inject
def get_item_by_key(
    key: str,
    service: LocalStorageService = Depends(Provide[Container.maintenance_local_storage_service]),
    current_user: Dict[str, Any] = Depends(permission_required(STORAGE_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific localStorage item by key.
    
    Requires maintenance:localStorage:read permission.
    """
    item = service.get_item_by_key(key)
    if not item:
        raise HTTPException(status_code=404, detail="LocalStorage item not found")
    return item

@router.post("/", response_model=LocalStorageResponse, status_code=201, summary="Create LocalStorage Item")
@inject
def create_item(
    data: LocalStorageCreate,
    service: LocalStorageService = Depends(Provide[Container.maintenance_local_storage_service]),
    current_user: Dict[str, Any] = Depends(permission_required(STORAGE_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new localStorage item.
    
    Requires maintenance:localStorage:create permission.
    """
    return service.add_item(**data.dict())

@router.put("/{item_id}", response_model=LocalStorageResponse, summary="Update LocalStorage Item")
@inject
def update_item(
    item_id: int,
    data: LocalStorageUpdate,
    service: LocalStorageService = Depends(Provide[Container.maintenance_local_storage_service]),
    current_user: Dict[str, Any] = Depends(permission_required(STORAGE_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a localStorage item by ID.
    
    Requires maintenance:localStorage:update permission.
    """
    updated_item = service.update_item(item_id, **data.dict(exclude_unset=True))
    if not updated_item:
        raise HTTPException(status_code=404, detail="LocalStorage item not found")
    return updated_item

@router.put("/key/{key}", response_model=LocalStorageResponse, summary="Update LocalStorage Item by Key")
@inject
def update_item_by_key(
    key: str,
    data: LocalStorageUpdate,
    service: LocalStorageService = Depends(Provide[Container.maintenance_local_storage_service]),
    current_user: Dict[str, Any] = Depends(permission_required(STORAGE_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a localStorage item by key.
    
    Requires maintenance:localStorage:update permission.
    """
    updated_item = service.update_item_by_key(key, **data.dict(exclude_unset=True))
    if not updated_item:
        raise HTTPException(status_code=404, detail="LocalStorage item not found")
    return updated_item

@router.delete("/{item_id}", status_code=204, summary="Delete LocalStorage Item")
@inject
def delete_item(
    item_id: int,
    service: LocalStorageService = Depends(Provide[Container.maintenance_local_storage_service]),
    current_user: Dict[str, Any] = Depends(permission_required(STORAGE_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a localStorage item by ID.
    
    Requires maintenance:localStorage:delete permission.
    """
    success = service.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="LocalStorage item not found")
    return {"message": "LocalStorage item deleted successfully"}

@router.delete("/key/{key}", status_code=204, summary="Delete LocalStorage Item by Key")
@inject
def delete_item_by_key(
    key: str,
    service: LocalStorageService = Depends(Provide[Container.maintenance_local_storage_service]),
    current_user: Dict[str, Any] = Depends(permission_required(STORAGE_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a localStorage item by key.
    
    Requires maintenance:localStorage:delete permission.
    """
    success = service.delete_item_by_key(key)
    if not success:
        raise HTTPException(status_code=404, detail="LocalStorage item not found")
    return {"message": "LocalStorage item deleted successfully"}
