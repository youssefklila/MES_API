# endpoints/part_type_endpoint.py

from fastapi import APIRouter, Depends, HTTPException, Security
from dependency_injector.wiring import inject, Provide
from typing import List, Dict, Any
from fastapi.security import OAuth2PasswordBearer

from webapp.ADM.master_data.part_type.schemas.part_type_schema import PartTypeResponse, PartTypeCreate, PartTypeUpdate
from webapp.ADM.master_data.part_type.services.part_type_service import PartTypeService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(
    prefix="/part-types",
    tags=["Part Types"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}}
)

# Permission constants
PART_TYPE_READ_PERM = "part_type:read"
PART_TYPE_CREATE_PERM = "part_type:create"
PART_TYPE_UPDATE_PERM = "part_type:update"
PART_TYPE_DELETE_PERM = "part_type:delete"

@router.get("/", response_model=List[PartTypeResponse], summary="Get All Part Types")
@inject
def get_part_types(
    service: PartTypeService = Depends(Provide[Container.part_type_service]),
    current_user: Dict[str, Any] = Depends(permission_required(PART_TYPE_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all part types.
    
    Requires part_type:read permission.
    """
    return service.get_all_part_types()

@router.get("/{part_type_id}", response_model=PartTypeResponse, summary="Get Part Type")
@inject
def get_part_type(
    part_type_id: int,
    service: PartTypeService = Depends(Provide[Container.part_type_service]),
    current_user: Dict[str, Any] = Depends(permission_required(PART_TYPE_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific part type by ID.
    
    Requires part_type:read permission.
    """
    part_type = service.get_part_type_by_id(part_type_id)
    if not part_type:
        raise HTTPException(status_code=404, detail="PartType not found")
    return part_type

@router.post("/", response_model=PartTypeResponse, status_code=201, summary="Create Part Type")
@inject
def create_part_type(
    data: PartTypeCreate,
    service: PartTypeService = Depends(Provide[Container.part_type_service]),
    current_user: Dict[str, Any] = Depends(permission_required(PART_TYPE_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new part type.
    
    Requires part_type:create permission.
    """
    return service.add_part_type(**data.dict())

@router.put("/{part_type_id}", response_model=PartTypeResponse, summary="Update Part Type")
@inject
def update_part_type(
    part_type_id: int,
    data: PartTypeUpdate,
    service: PartTypeService = Depends(Provide[Container.part_type_service]),
    current_user: Dict[str, Any] = Depends(permission_required(PART_TYPE_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a part type.
    
    Requires part_type:update permission.
    """
    updated_part_type = service.update_part_type(part_type_id, **data.dict())
    if not updated_part_type:
        raise HTTPException(status_code=404, detail="PartType not found")
    return updated_part_type

@router.delete("/{part_type_id}", status_code=204, summary="Delete Part Type")
@inject
def delete_part_type(
    part_type_id: int,
    service: PartTypeService = Depends(Provide[Container.part_type_service]),
    current_user: Dict[str, Any] = Depends(permission_required(PART_TYPE_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a part type.
    
    Requires part_type:delete permission.
    """
    result = service.delete_part_type(part_type_id)
    if not result["success"]:
        if result["reason"] == "not_found":
            raise HTTPException(status_code=404, detail="PartType not found")
        elif result["reason"] == "has_part_masters":
            raise HTTPException(
                status_code=409, 
                detail="Cannot delete part type because it has associated part master records. Remove the part master records first."
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to delete part type")
    return {"message": "PartType deleted successfully"}
