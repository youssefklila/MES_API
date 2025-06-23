from fastapi import APIRouter, Depends, HTTPException, Security
from typing import List, Dict, Any
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordBearer

from webapp.ADM.master_data.part_master.schemas.part_master_schema import PartMasterResponse, PartMasterCreate, \
    PartMasterUpdate
from webapp.ADM.master_data.part_master.services.part_master_service import PartMasterService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(
    prefix="/part-master",
    tags=["Part Master"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}}
)

# Permission constants
PART_MASTER_READ_PERM = "part_master:read"
PART_MASTER_CREATE_PERM = "part_master:create"
PART_MASTER_UPDATE_PERM = "part_master:update"
PART_MASTER_DELETE_PERM = "part_master:delete"

@router.get("/", response_model=List[PartMasterResponse], summary="Get All Part Masters")
@inject
def get_part_masters(
    part_master_service: PartMasterService = Depends(Provide[Container.part_master_service]),
    current_user: Dict[str, Any] = Depends(permission_required(PART_MASTER_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all part masters.
    
    Requires part_master:read permission.
    """
    return part_master_service.get_all_part_masters()

@router.get("/{part_master_id}", response_model=PartMasterResponse, summary="Get Part Master")
@inject
def get_part_master(
    part_master_id: int,
    part_master_service: PartMasterService = Depends(Provide[Container.part_master_service]),
    current_user: Dict[str, Any] = Depends(permission_required(PART_MASTER_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific part master by ID.
    
    Requires part_master:read permission.
    """
    part_master = part_master_service.get_part_master_by_id(part_master_id)
    if not part_master:
        raise HTTPException(status_code=404, detail="PartMaster not found")
    return part_master

@router.post("/", response_model=PartMasterResponse, status_code=201, summary="Create Part Master")
@inject
def create_part_master(
    part_master_data: PartMasterCreate,
    part_master_service: PartMasterService = Depends(Provide[Container.part_master_service]),
    current_user: Dict[str, Any] = Depends(permission_required(PART_MASTER_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new part master.
    
    Requires part_master:create permission.
    """
    return part_master_service.create_part_master(**part_master_data.dict())

@router.put("/{part_master_id}", response_model=PartMasterResponse, summary="Update Part Master")
@inject
def update_part_master(
    part_master_id: int,
    part_master_data: PartMasterUpdate,
    part_master_service: PartMasterService = Depends(Provide[Container.part_master_service]),
    current_user: Dict[str, Any] = Depends(permission_required(PART_MASTER_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a part master.
    
    Requires part_master:update permission.
    """
    updated_part_master = part_master_service.update_part_master(part_master_id, **part_master_data.dict())
    if not updated_part_master:
        raise HTTPException(status_code=404, detail="PartMaster not found")
    return updated_part_master

@router.delete("/{part_master_id}", status_code=204, summary="Delete Part Master")
@inject
def delete_part_master(
    part_master_id: int,
    part_master_service: PartMasterService = Depends(Provide[Container.part_master_service]),
    current_user: Dict[str, Any] = Depends(permission_required(PART_MASTER_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a part master.
    
    Requires part_master:delete permission.
    """
    success = part_master_service.delete_part_master(part_master_id)
    if not success:
        raise HTTPException(status_code=404, detail="PartMaster not found")
    return {"message": "PartMaster deleted successfully"}
