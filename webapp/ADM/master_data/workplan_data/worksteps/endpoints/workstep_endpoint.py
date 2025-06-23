from fastapi import APIRouter, Depends, HTTPException, Security, Query
from typing import List, Dict, Any, Optional
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordBearer

from webapp.ADM.master_data.workplan_data.worksteps.schemas.workstep_schema import WorkStep, WorkStepCreate, WorkStepUpdate, PaginatedWorkSteps
from webapp.ADM.master_data.workplan_data.worksteps.services.workstep_service import WorkStepService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(
    prefix="/worksteps",
    tags=["Work Steps"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}}
)

# Permission constants
WORKSTEP_READ_PERM = "workstep:read"
WORKSTEP_CREATE_PERM = "workstep:create"
WORKSTEP_UPDATE_PERM = "workstep:update"
WORKSTEP_DELETE_PERM = "workstep:delete"

@router.get("/", response_model=List[WorkStep], summary="Get All Work Steps")
@inject
def get_worksteps(
    workstep_service: WorkStepService = Depends(Provide[Container.workstep_service]),
    current_user: Dict[str, Any] = Depends(permission_required(WORKSTEP_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all work steps.
    
    Requires workstep:read permission.
    """
    return workstep_service.get_all_worksteps()

@router.get("/workplan/{workplan_id}", response_model=List[WorkStep], summary="Get Work Steps by WorkPlan ID")
@inject
def get_worksteps_by_workplan(
    workplan_id: int,
    workstep_service: WorkStepService = Depends(Provide[Container.workstep_service]),
    current_user: Dict[str, Any] = Depends(permission_required(WORKSTEP_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all work steps for a specific work plan.
    
    Requires workstep:read permission.
    """
    return workstep_service.get_worksteps_by_workplan_id(workplan_id)

@router.get("/{workstep_id}", response_model=WorkStep, summary="Get Work Step")
@inject
def get_workstep(
    workstep_id: int,
    workstep_service: WorkStepService = Depends(Provide[Container.workstep_service]),
    current_user: Dict[str, Any] = Depends(permission_required(WORKSTEP_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific work step by ID.
    
    Requires workstep:read permission.
    """
    workstep = workstep_service.get_workstep_by_id(workstep_id)
    if not workstep:
        raise HTTPException(status_code=404, detail="Work Step not found")
    return workstep

@router.post("/", response_model=WorkStep, status_code=201, summary="Create Work Step")
@inject
def create_workstep(
    workstep_data: WorkStepCreate,
    workstep_service: WorkStepService = Depends(Provide[Container.workstep_service]),
    current_user: Dict[str, Any] = Depends(permission_required(WORKSTEP_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new work step.
    
    Requires workstep:create permission.
    """
    return workstep_service.add_workstep(**workstep_data.dict())

@router.put("/{workstep_id}", response_model=WorkStep, summary="Update Work Step")
@inject
def update_workstep(
    workstep_id: int,
    workstep_data: WorkStepUpdate,
    workstep_service: WorkStepService = Depends(Provide[Container.workstep_service]),
    current_user: Dict[str, Any] = Depends(permission_required(WORKSTEP_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a work step.
    
    Requires workstep:update permission.
    """
    updated_workstep = workstep_service.update_workstep(workstep_id, **workstep_data.dict(exclude_unset=True))
    if not updated_workstep:
        raise HTTPException(status_code=404, detail="Work Step not found")
    return updated_workstep

@router.delete("/{workstep_id}", status_code=204, summary="Delete Work Step")
@inject
def delete_workstep(
    workstep_id: int,
    workstep_service: WorkStepService = Depends(Provide[Container.workstep_service]),
    current_user: Dict[str, Any] = Depends(permission_required(WORKSTEP_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a work step.
    
    Requires workstep:delete permission.
    """
    success = workstep_service.delete_workstep(workstep_id)
    if not success:
        raise HTTPException(status_code=404, detail="Work Step not found")
    return {"message": "Work Step deleted successfully"}
