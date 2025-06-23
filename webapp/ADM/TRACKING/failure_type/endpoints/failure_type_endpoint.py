# endpoints/failure_type_endpoint.py

from fastapi import APIRouter, Depends, HTTPException, Security, status
from typing import List, Dict, Any
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordBearer

from webapp.ADM.TRACKING.failure_type.schemas.failure_type_schema import FailureTypeCreate, FailureTypeUpdate, FailureTypeResponse
from webapp.ADM.TRACKING.failure_type.services.failure_type_service import FailureTypeService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

router = APIRouter(
    prefix="/failure-types",
    tags=["Failure Types"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}}
)

# Permission constants
FAILURE_TYPE_READ_PERM = "failure_type:read"
FAILURE_TYPE_CREATE_PERM = "failure_type:create"
FAILURE_TYPE_UPDATE_PERM = "failure_type:update"
FAILURE_TYPE_DELETE_PERM = "failure_type:delete"

@router.get("/", response_model=List[FailureTypeResponse], summary="Get All Failure Types")
@inject
def get_all_failure_types(
    failure_type_service: FailureTypeService = Depends(Provide[Container.failure_type_service]),
    current_user: Dict[str, Any] = Depends(permission_required(FAILURE_TYPE_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all failure types.
    
    Requires failure_type:read permission.
    """
    return failure_type_service.get_all_failure_types()

@router.get("/{failure_type_id}", response_model=FailureTypeResponse, summary="Get Failure Type")
@inject
def get_failure_type(
    failure_type_id: int,
    failure_type_service: FailureTypeService = Depends(Provide[Container.failure_type_service]),
    current_user: Dict[str, Any] = Depends(permission_required(FAILURE_TYPE_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific failure type by ID.
    
    Requires failure_type:read permission.
    """
    failure_type = failure_type_service.get_failure_type_by_id(failure_type_id)
    if not failure_type:
        raise HTTPException(status_code=404, detail="Failure Type not found")
    return failure_type

@router.post("/", response_model=FailureTypeResponse, status_code=201, summary="Create Failure Type")
@inject
def create_failure_type(
    failure_type_data: FailureTypeCreate,
    failure_type_service: FailureTypeService = Depends(Provide[Container.failure_type_service]),
    current_user: Dict[str, Any] = Depends(permission_required(FAILURE_TYPE_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new failure type.
    
    Requires failure_type:create permission.
    """
    return failure_type_service.create_failure_type(**failure_type_data.dict())

@router.put("/{failure_type_id}", response_model=FailureTypeResponse, summary="Update Failure Type")
@inject
def update_failure_type(
    failure_type_id: int,
    failure_type_data: FailureTypeUpdate,
    failure_type_service: FailureTypeService = Depends(Provide[Container.failure_type_service]),
    current_user: Dict[str, Any] = Depends(permission_required(FAILURE_TYPE_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a failure type.
    
    Requires failure_type:update permission.
    """
    updated_failure_type = failure_type_service.update_failure_type(
        failure_type_id, 
        **failure_type_data.dict(exclude_unset=True)
    )
    if not updated_failure_type:
        raise HTTPException(status_code=404, detail="Failure Type not found")
    return updated_failure_type

@router.delete("/{failure_type_id}", status_code=204, summary="Delete Failure Type")
@inject
def delete_failure_type(
    failure_type_id: int,
    failure_type_service: FailureTypeService = Depends(Provide[Container.failure_type_service]),
    current_user: Dict[str, Any] = Depends(permission_required(FAILURE_TYPE_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a failure type.
    
    Requires failure_type:delete permission.
    """
    success = failure_type_service.delete_failure_type(failure_type_id)
    if not success:
        raise HTTPException(status_code=404, detail="Failure Type not found")
    return {"message": "Failure Type deleted successfully"}

@router.get("/code/{failure_type_code}", response_model=FailureTypeResponse, summary="Get Failure Type by Code")
@inject
def get_failure_type_by_code(
    failure_type_code: str,
    failure_type_service: FailureTypeService = Depends(Provide[Container.failure_type_service]),
    current_user: Dict[str, Any] = Depends(permission_required(FAILURE_TYPE_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific failure type by code.
    
    Requires failure_type:read permission.
    """
    failure_type = failure_type_service.get_failure_type_by_code(failure_type_code)
    if not failure_type:
        raise HTTPException(status_code=404, detail="Failure Type not found")
    return failure_type
