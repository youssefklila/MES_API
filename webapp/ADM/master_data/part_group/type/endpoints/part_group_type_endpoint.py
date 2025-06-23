# endpoints/part_group_type_endpoint.py

from fastapi import APIRouter, Depends, HTTPException, Security
from dependency_injector.wiring import inject, Provide
from typing import List, Dict, Any
from fastapi.security import OAuth2PasswordBearer

from webapp.ADM.master_data.part_group.type.schemas.part_group_type_schema import PartGroupTypeResponse, \
    PartGroupTypeCreate, PartGroupTypeUpdate
from webapp.ADM.master_data.part_group.type.services.part_group_type_service import PartGroupTypeService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(
    prefix="/part-group-types",
    tags=["Part Group Types"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}}
)

# Permission constants
PART_GROUP_TYPE_READ_PERM = "part_group_type:read"
PART_GROUP_TYPE_CREATE_PERM = "part_group_type:create"
PART_GROUP_TYPE_UPDATE_PERM = "part_group_type:update"
PART_GROUP_TYPE_DELETE_PERM = "part_group_type:delete"

@router.get("/", response_model=List[PartGroupTypeResponse], summary="Get All Part Group Types")
@inject
def get_part_group_types(
    service: PartGroupTypeService = Depends(Provide[Container.part_group_type_service]),
    current_user: Dict[str, Any] = Depends(permission_required(PART_GROUP_TYPE_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all part group types.
    
    Requires part_group_type:read permission.
    """
    return service.get_all_part_group_types()

@router.get("/{part_group_type_id}", response_model=PartGroupTypeResponse, summary="Get Part Group Type")
@inject
def get_part_group_type(
    part_group_type_id: int,
    service: PartGroupTypeService = Depends(Provide[Container.part_group_type_service]),
    current_user: Dict[str, Any] = Depends(permission_required(PART_GROUP_TYPE_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific part group type by ID.
    
    Requires part_group_type:read permission.
    """
    part_group_type = service.get_part_group_type_by_id(part_group_type_id)
    if not part_group_type:
        raise HTTPException(status_code=404, detail="PartGroupType not found")
    return part_group_type

@router.post("/", response_model=PartGroupTypeResponse, status_code=201, summary="Create Part Group Type")
@inject
def create_part_group_type(
    data: PartGroupTypeCreate,
    service: PartGroupTypeService = Depends(Provide[Container.part_group_type_service]),
    current_user: Dict[str, Any] = Depends(permission_required(PART_GROUP_TYPE_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new part group type.
    
    Requires part_group_type:create permission.
    """
    return service.add_part_group_type(**data.dict())

@router.put("/{part_group_type_id}", response_model=PartGroupTypeResponse, summary="Update Part Group Type")
@inject
def update_part_group_type(
    part_group_type_id: int,
    data: PartGroupTypeUpdate,
    service: PartGroupTypeService = Depends(Provide[Container.part_group_type_service]),
    current_user: Dict[str, Any] = Depends(permission_required(PART_GROUP_TYPE_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a part group type.
    
    Requires part_group_type:update permission.
    """
    updated_part_group_type = service.update_part_group_type(part_group_type_id, **data.dict())
    if not updated_part_group_type:
        raise HTTPException(status_code=404, detail="PartGroupType not found")
    return updated_part_group_type

@router.delete("/{part_group_type_id}", status_code=204, summary="Delete Part Group Type")
@inject
def delete_part_group_type(
    part_group_type_id: int,
    service: PartGroupTypeService = Depends(Provide[Container.part_group_type_service]),
    current_user: Dict[str, Any] = Depends(permission_required(PART_GROUP_TYPE_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a part group type.
    
    Requires part_group_type:delete permission.
    """
    success = service.delete_part_group_type(part_group_type_id)
    if not success:
        raise HTTPException(status_code=404, detail="PartGroupType not found")
    return {"message": "PartGroupType deleted successfully"}
