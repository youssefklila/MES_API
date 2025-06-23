from fastapi import APIRouter, Depends, HTTPException, Security, Query
from typing import List, Dict, Any, Optional
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordBearer

from webapp.ADM.master_data.workorder.schemas.workorder_schema import WorkOrderResponse as WorkOrder, WorkOrderCreate, WorkOrderUpdate, PaginatedWorkOrders
from webapp.ADM.master_data.workorder.services.workorder_service import WorkOrderService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(
    prefix="/workorders",
    tags=["Work Orders"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}}
)

# Permission constants
WORKORDER_READ_PERM = "workorder:read"
WORKORDER_CREATE_PERM = "workorder:create"
WORKORDER_UPDATE_PERM = "workorder:update"
WORKORDER_DELETE_PERM = "workorder:delete"

@router.get("/", response_model=List[WorkOrder], summary="Get All Work Orders")
@inject
def get_workorders(
    workorder_service: WorkOrderService = Depends(Provide[Container.workorder_service]),
    current_user: Dict[str, Any] = Depends(permission_required(WORKORDER_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all work orders.
    
    Requires workorder:read permission.
    """
    return workorder_service.get_all_workorders()

@router.get("/part/{part_number}", response_model=List[WorkOrder], summary="Get Work Orders by Part Number")
@inject
def get_workorders_by_part_number(
    part_number: str,
    workorder_service: WorkOrderService = Depends(Provide[Container.workorder_service]),
    current_user: Dict[str, Any] = Depends(permission_required(WORKORDER_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all work orders for a specific part number.
    
    Requires workorder:read permission.
    """
    return workorder_service.get_workorders_by_part_number(part_number)

@router.get("/{workorder_id}", response_model=WorkOrder, summary="Get Work Order by ID")
@inject
def get_workorder(
    workorder_id: int,
    workorder_service: WorkOrderService = Depends(Provide[Container.workorder_service]),
    current_user: Dict[str, Any] = Depends(permission_required(WORKORDER_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific work order by ID.
    
    Requires workorder:read permission.
    """
    workorder = workorder_service.get_workorder_by_id(workorder_id)
    if not workorder:
        raise HTTPException(status_code=404, detail="Work Order not found")
    return workorder

@router.get("/no/{workorder_no}", response_model=WorkOrder, summary="Get Work Order by Number")
@inject
def get_workorder_by_number(
    workorder_no: str,
    workorder_service: WorkOrderService = Depends(Provide[Container.workorder_service]),
    current_user: Dict[str, Any] = Depends(permission_required(WORKORDER_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific work order by its workorder number.
    
    Requires workorder:read permission.
    """
    workorder = workorder_service.get_workorder_by_workorder_no(workorder_no)
    if not workorder:
        raise HTTPException(status_code=404, detail="Work Order not found")
    return workorder

@router.post("/", response_model=WorkOrder, status_code=201, summary="Create Work Order")
@inject
def create_workorder(
    workorder_data: WorkOrderCreate,
    workorder_service: WorkOrderService = Depends(Provide[Container.workorder_service]),
    current_user: Dict[str, Any] = Depends(permission_required(WORKORDER_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new work order.
    
    Requires workorder:create permission.
    """
    return workorder_service.add_workorder(**workorder_data.dict())

@router.put("/{workorder_id}", response_model=WorkOrder, summary="Update Work Order")
@inject
def update_workorder(
    workorder_id: int,
    workorder_data: WorkOrderUpdate,
    workorder_service: WorkOrderService = Depends(Provide[Container.workorder_service]),
    current_user: Dict[str, Any] = Depends(permission_required(WORKORDER_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a work order.
    
    Requires workorder:update permission.
    """
    updated_workorder = workorder_service.update_workorder(workorder_id, **workorder_data.dict(exclude_unset=True))
    if not updated_workorder:
        raise HTTPException(status_code=404, detail="Work Order not found")
    return updated_workorder

@router.delete("/{workorder_id}", status_code=204, summary="Delete Work Order")
@inject
def delete_workorder(
    workorder_id: int,
    workorder_service: WorkOrderService = Depends(Provide[Container.workorder_service]),
    current_user: Dict[str, Any] = Depends(permission_required(WORKORDER_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a work order.
    
    Requires workorder:delete permission.
    """
    success = workorder_service.delete_workorder(workorder_id)
    if not success:
        raise HTTPException(status_code=404, detail="Work Order not found")
    return {"message": "Work Order deleted successfully"}
