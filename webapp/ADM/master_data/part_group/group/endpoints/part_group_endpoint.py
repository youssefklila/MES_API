from fastapi import APIRouter, Depends, HTTPException, Security
from typing import List, Dict, Any
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordBearer

from webapp.ADM.master_data.part_group.group.schemas.part_group_schema import PartGroupCreate, PartGroupUpdate, PartGroupResponse
from webapp.ADM.master_data.part_group.group.services.part_group_service import PartGroupService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(
    prefix="/part-groups",
    tags=["Part Groups"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}}
)

# Permission constants
PART_GROUP_READ_PERM = "part_group:read"
PART_GROUP_CREATE_PERM = "part_group:create"
PART_GROUP_UPDATE_PERM = "part_group:update"
PART_GROUP_DELETE_PERM = "part_group:delete"

@router.get("/", response_model=List[PartGroupResponse], summary="Get All Part Groups")
@inject
def get_part_groups(
    part_group_service: PartGroupService = Depends(Provide[Container.part_group_service]),
    current_user: Dict[str, Any] = Depends(permission_required(PART_GROUP_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all part groups.
    
    Requires part_group:read permission.
    """
    return part_group_service.get_all_part_groups()

@router.get("/{part_group_id}", response_model=PartGroupResponse, summary="Get Part Group")
@inject
def get_part_group(
    part_group_id: int,
    part_group_service: PartGroupService = Depends(Provide[Container.part_group_service]),
    current_user: Dict[str, Any] = Depends(permission_required(PART_GROUP_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific part group by ID.
    
    Requires part_group:read permission.
    """
    part_group = part_group_service.get_part_group_by_id(part_group_id)
    if not part_group:
        raise HTTPException(status_code=404, detail="Part group not found")
    return part_group

@router.post("/", response_model=PartGroupResponse, status_code=201, summary="Create Part Group")
@inject
def create_part_group(
    part_group_data: PartGroupCreate,
    part_group_service: PartGroupService = Depends(Provide[Container.part_group_service]),
    current_user: Dict[str, Any] = Depends(permission_required(PART_GROUP_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new part group.
    
    Requires part_group:create permission.
    """
    return part_group_service.add_part_group(**part_group_data.dict())

@router.put("/{part_group_id}", response_model=PartGroupResponse, summary="Update Part Group")
@inject
def update_part_group(
    part_group_id: int,
    part_group_data: PartGroupUpdate,
    part_group_service: PartGroupService = Depends(Provide[Container.part_group_service]),
    current_user: Dict[str, Any] = Depends(permission_required(PART_GROUP_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a part group.
    
    Requires part_group:update permission.
    """
    updated_part_group = part_group_service.update_part_group(part_group_id, **part_group_data.dict())
    if not updated_part_group:
        raise HTTPException(status_code=404, detail="Part group not found")
    return updated_part_group

@router.delete("/{part_group_id}", status_code=204, summary="Delete Part Group")
@inject
def delete_part_group(
    part_group_id: int,
    part_group_service: PartGroupService = Depends(Provide[Container.part_group_service]),
    current_user: Dict[str, Any] = Depends(permission_required(PART_GROUP_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a part group.
    
    Requires part_group:delete permission.
    """
    success = part_group_service.delete_part_group(part_group_id)
    if not success:
        raise HTTPException(status_code=404, detail="Part group not found")
    return None
