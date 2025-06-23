"""Machine Condition endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Security, status
from typing import List, Dict, Any
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordBearer

from webapp.ADM.MDC.machine_condition.schemas.machine_condition_schema import (
    MachineConditionCreate,
    MachineConditionUpdate,
    MachineConditionResponse
)
from webapp.ADM.MDC.machine_condition.services.machine_condition_service import MachineConditionService
from webapp.ADM.MDC.machine_condition_group.services.machine_condition_group_service import MachineConditionGroupService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(
    prefix="/machine-conditions",
    tags=["Machine Conditions"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}, 404: {"description": "Not found"}}
)

# Permission constants
MC_READ_PERM = "machine_condition:read"
MC_CREATE_PERM = "machine_condition:create"
MC_UPDATE_PERM = "machine_condition:update"
MC_DELETE_PERM = "machine_condition:delete"

@router.get("/", response_model=List[MachineConditionResponse], summary="Get All Machine Conditions")
@inject
def get_all_conditions(
    service: MachineConditionService = Depends(Provide[Container.machine_condition_service]),
    current_user: Dict[str, Any] = Depends(permission_required(MC_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all machine conditions.
    
    Requires machine_condition:read permission.
    """
    return service.get_all_conditions()

@router.get("/group/{group_id}", response_model=List[MachineConditionResponse], summary="Get Conditions by Group")
@inject
def get_conditions_by_group(
    group_id: int,
    service: MachineConditionService = Depends(Provide[Container.machine_condition_service]),
    group_service: MachineConditionGroupService = Depends(Provide[Container.machine_condition_group_service]),
    current_user: Dict[str, Any] = Depends(permission_required(MC_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all machine conditions for a specific group.
    
    Requires machine_condition:read permission.
    """
    # Check if the group exists
    group = group_service.get_group_by_id(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine condition group not found")
    
    return service.get_conditions_by_group_id(group_id)

@router.get("/{condition_id}", response_model=MachineConditionResponse, summary="Get Machine Condition")
@inject
def get_condition_by_id(
    condition_id: int,
    service: MachineConditionService = Depends(Provide[Container.machine_condition_service]),
    current_user: Dict[str, Any] = Depends(permission_required(MC_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific machine condition by ID.
    
    Requires machine_condition:read permission.
    """
    condition = service.get_condition_by_id(condition_id)
    if not condition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine condition not found")
    return condition

@router.post("/", response_model=MachineConditionResponse, status_code=status.HTTP_201_CREATED, summary="Create Machine Condition")
@inject
def create_condition(
    condition_data: MachineConditionCreate,
    service: MachineConditionService = Depends(Provide[Container.machine_condition_service]),
    group_service: MachineConditionGroupService = Depends(Provide[Container.machine_condition_group_service]),
    current_user: Dict[str, Any] = Depends(permission_required(MC_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new machine condition.
    
    Requires machine_condition:create permission.
    """
    # Check if the group exists
    group = group_service.get_group_by_id(condition_data.group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Machine condition group with ID {condition_data.group_id} does not exist"
        )
    
    # Check if condition with same name already exists
    existing_condition = service.get_condition_by_name(condition_data.condition_name)
    if existing_condition:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Machine condition with name '{condition_data.condition_name}' already exists"
        )
    
    return service.create_condition(
        group_id=condition_data.group_id,
        condition_name=condition_data.condition_name,
        condition_description=condition_data.condition_description,
        color_rgb=condition_data.color_rgb,
        is_active=condition_data.is_active
    )

@router.put("/{condition_id}", response_model=MachineConditionResponse, summary="Update Machine Condition")
@inject
def update_condition(
    condition_id: int,
    condition_data: MachineConditionUpdate,
    service: MachineConditionService = Depends(Provide[Container.machine_condition_service]),
    group_service: MachineConditionGroupService = Depends(Provide[Container.machine_condition_group_service]),
    current_user: Dict[str, Any] = Depends(permission_required(MC_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a machine condition.
    
    Requires machine_condition:update permission.
    """
    # Check if the condition exists
    existing_condition = service.get_condition_by_id(condition_id)
    if not existing_condition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine condition not found")
    
    # If group_id is provided, check if the group exists
    if condition_data.group_id is not None:
        group = group_service.get_group_by_id(condition_data.group_id)
        if not group:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Machine condition group with ID {condition_data.group_id} does not exist"
            )
    
    # If condition_name is provided, check if it's already used by another condition
    if condition_data.condition_name is not None:
        existing_name = service.get_condition_by_name(condition_data.condition_name)
        if existing_name and existing_name["id"] != condition_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Machine condition with name '{condition_data.condition_name}' already exists"
            )
    
    updated_condition = service.update_condition(
        condition_id=condition_id,
        group_id=condition_data.group_id,
        condition_name=condition_data.condition_name,
        condition_description=condition_data.condition_description,
        color_rgb=condition_data.color_rgb,
        is_active=condition_data.is_active
    )
    
    if not updated_condition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine condition not found")
    
    return updated_condition

@router.delete("/{condition_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Machine Condition")
@inject
def delete_condition(
    condition_id: int,
    service: MachineConditionService = Depends(Provide[Container.machine_condition_service]),
    current_user: Dict[str, Any] = Depends(permission_required(MC_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a machine condition.
    
    Requires machine_condition:delete permission.
    """
    # Check if the condition exists
    existing_condition = service.get_condition_by_id(condition_id)
    if not existing_condition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine condition not found")
    
    success = service.delete_condition(condition_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete machine condition")
    
    return None
