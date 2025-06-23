from fastapi import APIRouter, Depends, HTTPException, Security
from typing import List, Dict, Any
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordBearer

from webapp.ADM.master_data.workplan_data.workplan_type.schemas.workplan_type_schema import (
    WorkPlanTypeCreate,
    WorkPlanTypeUpdate,
    WorkPlanTypeResponse,
)
from webapp.ADM.master_data.workplan_data.workplan_type.services.workplan_type_service import WorkPlanTypeService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(
    prefix="/workplan-types",
    tags=["Work Plan Types"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}}
)

# Permission constants
WORKPLAN_TYPE_READ_PERM = "workplan_type:read"
WORKPLAN_TYPE_CREATE_PERM = "workplan_type:create"
WORKPLAN_TYPE_UPDATE_PERM = "workplan_type:update"
WORKPLAN_TYPE_DELETE_PERM = "workplan_type:delete"

@router.get("/", response_model=List[WorkPlanTypeResponse], summary="Get All Work Plan Types")
@inject
def get_workplan_types(
    workplan_type_service: WorkPlanTypeService = Depends(Provide[Container.workplan_type_service]),
    current_user: Dict[str, Any] = Depends(permission_required(WORKPLAN_TYPE_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all work plan types.
    
    Requires workplan_type:read permission.
    """
    return workplan_type_service.get_all_workplan_types()

@router.get("/{workplan_type_id}", response_model=WorkPlanTypeResponse, summary="Get Work Plan Type")
@inject
def get_workplan_type(
    workplan_type_id: int,
    workplan_type_service: WorkPlanTypeService = Depends(Provide[Container.workplan_type_service]),
    current_user: Dict[str, Any] = Depends(permission_required(WORKPLAN_TYPE_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific work plan type by ID.
    
    Requires workplan_type:read permission.
    """
    workplan_type = workplan_type_service.get_workplan_type_by_id(workplan_type_id)
    if not workplan_type:
        raise HTTPException(status_code=404, detail="WorkPlanType not found")
    return workplan_type

@router.post("/", response_model=WorkPlanTypeResponse, status_code=201, summary="Create Work Plan Type")
@inject
def create_workplan_type(
    workplan_type_data: WorkPlanTypeCreate,
    workplan_type_service: WorkPlanTypeService = Depends(Provide[Container.workplan_type_service]),
    current_user: Dict[str, Any] = Depends(permission_required(WORKPLAN_TYPE_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new work plan type.
    
    Requires workplan_type:create permission.
    """
    return workplan_type_service.add_workplan_type(**workplan_type_data.dict())

@router.put("/{workplan_type_id}", response_model=WorkPlanTypeResponse, summary="Update Work Plan Type")
@inject
def update_workplan_type(
    workplan_type_id: int,
    workplan_type_data: WorkPlanTypeUpdate,
    workplan_type_service: WorkPlanTypeService = Depends(Provide[Container.workplan_type_service]),
    current_user: Dict[str, Any] = Depends(permission_required(WORKPLAN_TYPE_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a work plan type.
    
    Requires workplan_type:update permission.
    """
    updated_workplan_type = workplan_type_service.update_workplan_type(workplan_type_id, **workplan_type_data.dict())
    if not updated_workplan_type:
        raise HTTPException(status_code=404, detail="WorkPlanType not found")
    return updated_workplan_type

@router.delete("/{workplan_type_id}", status_code=204, summary="Delete Work Plan Type")
@inject
def delete_workplan_type(
    workplan_type_id: int,
    workplan_type_service: WorkPlanTypeService = Depends(Provide[Container.workplan_type_service]),
    current_user: Dict[str, Any] = Depends(permission_required(WORKPLAN_TYPE_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a work plan type.
    
    Requires workplan_type:delete permission.
    """
    success = workplan_type_service.delete_workplan_type(workplan_type_id)
    if not success:
        raise HTTPException(status_code=404, detail="WorkPlanType not found")
    return {"message": "WorkPlanType deleted successfully"}
