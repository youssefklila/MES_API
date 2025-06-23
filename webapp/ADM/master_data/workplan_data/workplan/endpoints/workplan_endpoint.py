from fastapi import APIRouter, Depends, HTTPException, Security
from typing import List, Dict, Any
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordBearer


from webapp.ADM.master_data.workplan_data.workplan.schemas.workplan_schema import WorkPlan, WorkPlanCreate, \
    WorkPlanUpdate, PaginatedWorkPlans
from webapp.ADM.master_data.workplan_data.workplan.services.workplan_service import WorkPlanService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required



# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(
    prefix="/workplan",
    tags=["Work Plan"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}}
)

# Permission constants
WORKPLAN_READ_PERM = "workplan:read"
WORKPLAN_CREATE_PERM = "workplan:create"
WORKPLAN_UPDATE_PERM = "workplan:update"
WORKPLAN_DELETE_PERM = "workplan:delete"

@router.get("/", response_model=List[WorkPlan], summary="Get All Work Plans")
@inject
def get_work_plans(
    work_plan_service: WorkPlanService = Depends(Provide[Container.work_plan_service]),
    current_user: Dict[str, Any] = Depends(permission_required(WORKPLAN_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all work plans.
    
    Requires workplan:read permission.
    """
    return work_plan_service.get_all_work_plans()

@router.get("/{work_plan_id}", response_model=WorkPlan, summary="Get Work Plan")
@inject
def get_work_plan(
    work_plan_id: int,
    work_plan_service: WorkPlanService = Depends(Provide[Container.work_plan_service]),
    current_user: Dict[str, Any] = Depends(permission_required(WORKPLAN_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific work plan by ID.
    
    Requires workplan:read permission.
    """
    work_plan = work_plan_service.get_work_plan_by_id(work_plan_id)
    if not work_plan:
        raise HTTPException(status_code=404, detail="Work Plan not found")
    return work_plan

@router.post("/", response_model=WorkPlan, status_code=201, summary="Create Work Plan")
@inject
def create_work_plan(
    work_plan_data: WorkPlanCreate,
    work_plan_service: WorkPlanService = Depends(Provide[Container.work_plan_service]),
    current_user: Dict[str, Any] = Depends(permission_required(WORKPLAN_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new work plan.
    
    Requires workplan:create permission.
    """
    return work_plan_service.add_work_plan(**work_plan_data.dict())

@router.put("/{work_plan_id}", response_model=WorkPlan, summary="Update Work Plan")
@inject
def update_work_plan(
    work_plan_id: int,
    work_plan_data: WorkPlanUpdate,
    work_plan_service: WorkPlanService = Depends(Provide[Container.work_plan_service]),
    current_user: Dict[str, Any] = Depends(permission_required(WORKPLAN_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a work plan.
    
    Requires workplan:update permission.
    """
    updated_work_plan = work_plan_service.update_work_plan(work_plan_id, **work_plan_data.dict())
    if not updated_work_plan:
        raise HTTPException(status_code=404, detail="Work Plan not found")
    return updated_work_plan

@router.delete("/{work_plan_id}", status_code=204, summary="Delete Work Plan")
@inject
def delete_work_plan(
    work_plan_id: int,
    work_plan_service: WorkPlanService = Depends(Provide[Container.work_plan_service]),
    current_user: Dict[str, Any] = Depends(permission_required(WORKPLAN_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a work plan.
    
    Requires workplan:delete permission.
    """
    success = work_plan_service.delete_work_plan(work_plan_id)
    if not success:
        raise HTTPException(status_code=404, detail="Work Plan not found")
    return {"message": "Work Plan deleted successfully"}
