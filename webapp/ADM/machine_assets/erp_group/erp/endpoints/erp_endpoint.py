# endpoints/erp_group_endpoint.py

from fastapi import APIRouter, Depends, HTTPException, Security
from typing import List, Dict, Any
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordBearer

from webapp.ADM.machine_assets.erp_group.erp.schemas.erp_schema import ERPGroupCreate, ERPGroupUpdate, ERPGroupResponse
from webapp.ADM.machine_assets.erp_group.erp.services.erp_service import ERPGroupService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

router = APIRouter(
    prefix="/erp-groups",
    tags=["ERP Groups"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}}
)

# Permission constants
ERP_GROUP_READ_PERM = "erp_group:read"
ERP_GROUP_CREATE_PERM = "erp_group:create"
ERP_GROUP_UPDATE_PERM = "erp_group:update"
ERP_GROUP_DELETE_PERM = "erp_group:delete"

@router.get("/", response_model=List[ERPGroupResponse], summary="Get All ERP Groups")
@inject
def get_erp_groups(
    erp_group_service: ERPGroupService = Depends(Provide[Container.erp_group_service]),
    current_user: Dict[str, Any] = Depends(permission_required(ERP_GROUP_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all ERP groups.
    
    Requires erp_group:read permission.
    """
    return erp_group_service.get_all_erp_groups()

@router.get("/{erp_group_id}", response_model=ERPGroupResponse, summary="Get ERP Group")
@inject
def get_erp_group(
    erp_group_id: int,
    erp_group_service: ERPGroupService = Depends(Provide[Container.erp_group_service]),
    current_user: Dict[str, Any] = Depends(permission_required(ERP_GROUP_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific ERP group by ID.
    
    Requires erp_group:read permission.
    """
    erp_group = erp_group_service.get_erp_group_by_id(erp_group_id)
    if not erp_group:
        raise HTTPException(status_code=404, detail="ERP Group not found")
    return erp_group

@router.post("/", response_model=ERPGroupResponse, status_code=201, summary="Create ERP Group")
@inject
def create_erp_group(
    erp_group_data: ERPGroupCreate,
    erp_group_service: ERPGroupService = Depends(Provide[Container.erp_group_service]),
    current_user: Dict[str, Any] = Depends(permission_required(ERP_GROUP_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new ERP group.
    
    Requires erp_group:create permission.
    """
    return erp_group_service.add_erp_group(erp_group_data)

@router.put("/{erp_group_id}", response_model=ERPGroupResponse, summary="Update ERP Group")
@inject
def update_erp_group(
    erp_group_id: int,
    erp_group_data: ERPGroupUpdate,
    erp_group_service: ERPGroupService = Depends(Provide[Container.erp_group_service]),
    current_user: Dict[str, Any] = Depends(permission_required(ERP_GROUP_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update an ERP group.
    
    Requires erp_group:update permission.
    """
    updated_erp_group = erp_group_service.update_erp_group(erp_group_id, **erp_group_data.dict())
    if not updated_erp_group:
        raise HTTPException(status_code=404, detail="ERP Group not found")
    return updated_erp_group

@router.delete("/{erp_group_id}", status_code=204, summary="Delete ERP Group")
@inject
def delete_erp_group(
    erp_group_id: int,
    erp_group_service: ERPGroupService = Depends(Provide[Container.erp_group_service]),
    current_user: Dict[str, Any] = Depends(permission_required(ERP_GROUP_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete an ERP group.
    
    Requires erp_group:delete permission.
    """
    success = erp_group_service.delete_erp_group(erp_group_id)
    if not success:
        raise HTTPException(status_code=404, detail="ERP Group not found")
    return {"message": "ERP Group deleted successfully"}
