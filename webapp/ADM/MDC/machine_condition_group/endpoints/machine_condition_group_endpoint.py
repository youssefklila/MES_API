"""Machine Condition Group endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Security, status
from typing import List, Dict, Any
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordBearer

from webapp.ADM.MDC.machine_condition_group.schemas.machine_condition_group_schema import (
    MachineConditionGroupCreate,
    MachineConditionGroupUpdate,
    MachineConditionGroupResponse
)
from webapp.ADM.MDC.machine_condition_group.services.machine_condition_group_service import MachineConditionGroupService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(
    prefix="/machine-condition-groups",
    tags=["Machine Condition Groups"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}, 404: {"description": "Not found"}}
)

# Permission constants
MCG_READ_PERM = "machine_condition_group:read"
MCG_CREATE_PERM = "machine_condition_group:create"
MCG_UPDATE_PERM = "machine_condition_group:update"
MCG_DELETE_PERM = "machine_condition_group:delete"

@router.get("/", response_model=List[MachineConditionGroupResponse], summary="Get All Machine Condition Groups")
@inject
def get_all_groups(
    service: MachineConditionGroupService = Depends(Provide[Container.machine_condition_group_service]),
    current_user: Dict[str, Any] = Depends(permission_required(MCG_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all machine condition groups.
    
    Requires machine_condition_group:read permission.
    """
    return service.get_all_groups()

@router.get("/{group_id}", response_model=MachineConditionGroupResponse, summary="Get Machine Condition Group")
@inject
def get_group_by_id(
    group_id: int,
    service: MachineConditionGroupService = Depends(Provide[Container.machine_condition_group_service]),
    current_user: Dict[str, Any] = Depends(permission_required(MCG_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific machine condition group by ID.
    
    Requires machine_condition_group:read permission.
    """
    group = service.get_group_by_id(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machine condition group not found")
    return group

@router.post("/", response_model=MachineConditionGroupResponse, status_code=status.HTTP_201_CREATED, summary="Create Machine Condition Group")
@inject
def create_group(
    group_data: MachineConditionGroupCreate,
    service: MachineConditionGroupService = Depends(Provide[Container.machine_condition_group_service]),
    current_user: Dict[str, Any] = Depends(permission_required(MCG_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new machine condition group.
    
    Requires machine_condition_group:create permission.
    """
    # Check if group with same name already exists
    existing_group = service.get_group_by_name(group_data.group_name)
    if existing_group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Machine condition group with name '{group_data.group_name}' already exists"
        )
    
    return service.create_group(
        group_name=group_data.group_name,
        group_description=group_data.group_description,
        is_active=group_data.is_active
    )

@router.put("/{group_id}", response_model=MachineConditionGroupResponse, summary="Update Machine Condition Group")
@inject
def update_group(
    group_id: int,
    group_data: MachineConditionGroupUpdate,
    service: MachineConditionGroupService = Depends(Provide[Container.machine_condition_group_service]),
    current_user: Dict[str, Any] = Depends(permission_required(MCG_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a machine condition group.
    
    Requires machine_condition_group:update permission.
    """
    # Check if group exists
    existing_group = service.get_group_by_id(group_id)
    if not existing_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Machine condition group not found"
        )
    
    # If name is being updated, check if it conflicts with another group
    if group_data.group_name and group_data.group_name != existing_group["group_name"]:
        name_check = service.get_group_by_name(group_data.group_name)
        if name_check and name_check["id"] != group_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Machine condition group with name '{group_data.group_name}' already exists"
            )
    
    # Update only the fields that are provided
    update_data = {k: v for k, v in group_data.dict().items() if v is not None}
    updated_group = service.update_group(group_id, **update_data)
    
    return updated_group

@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Machine Condition Group")
@inject
def delete_group(
    group_id: int,
    service: MachineConditionGroupService = Depends(Provide[Container.machine_condition_group_service]),
    current_user: Dict[str, Any] = Depends(permission_required(MCG_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a machine condition group.
    
    Requires machine_condition_group:delete permission.
    """
    # Check if group exists
    existing_group = service.get_group_by_id(group_id)
    if not existing_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Machine condition group not found"
        )
    
    service.delete_group(group_id)
    return None
