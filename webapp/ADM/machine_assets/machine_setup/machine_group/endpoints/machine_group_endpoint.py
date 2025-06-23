# endpoints/machine_group_endpoint.py

from fastapi import APIRouter, Depends, HTTPException, Security
from typing import List, Dict, Any
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordBearer

from webapp.ADM.machine_assets.machine_setup.machine_group.schemas.machine_group_schema import MachineGroup, MachineGroupCreate, \
    MachineGroupUpdate
from webapp.ADM.machine_assets.machine_setup.machine_group.services.machine_group_service import MachineGroupService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

router = APIRouter(
    prefix="/machine_groups",
    tags=["Machine Groups"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}}
)

# Permission constants
MACHINE_GROUP_READ_PERM = "machine_group:read"
MACHINE_GROUP_CREATE_PERM = "machine_group:create"
MACHINE_GROUP_UPDATE_PERM = "machine_group:update"
MACHINE_GROUP_DELETE_PERM = "machine_group:delete"

@router.post("/", response_model=MachineGroup, status_code=201, summary="Create Machine Group")
@inject
def create_machine_group(
    machine_group: MachineGroupCreate,
    machine_group_service: MachineGroupService = Depends(Provide[Container.machine_group_service]),
    current_user: Dict[str, Any] = Depends(permission_required(MACHINE_GROUP_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new machine group.
    
    Requires machine_group:create permission.
    """
    return machine_group_service.create_machine_group(
        name=machine_group.name,
        description=machine_group.description,
        user_id=machine_group.user_id,
        cell_id=machine_group.cell_id,
        is_active=machine_group.is_active,
        failure=machine_group.failure
    )

@router.get("/{machine_group_id}", response_model=MachineGroup, summary="Get Machine Group")
@inject
def get_machine_group(
    machine_group_id: int,
    machine_group_service: MachineGroupService = Depends(Provide[Container.machine_group_service]),
    current_user: Dict[str, Any] = Depends(permission_required(MACHINE_GROUP_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific machine group by ID.
    
    Requires machine_group:read permission.
    """
    machine_group = machine_group_service.get_machine_group_by_id(machine_group_id)
    if machine_group is None:
        raise HTTPException(status_code=404, detail="Machine group not found")
    return machine_group

@router.get("/", response_model=list[MachineGroup], summary="Get All Machine Groups")
@inject
def get_all_machine_groups(
    machine_group_service: MachineGroupService = Depends(Provide[Container.machine_group_service]),
    current_user: Dict[str, Any] = Depends(permission_required(MACHINE_GROUP_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all machine groups.
    
    Requires machine_group:read permission.
    """
    return machine_group_service.get_all_machine_groups()

@router.put("/{machine_group_id}", response_model=MachineGroup, summary="Update Machine Group")
@inject
def update_machine_group(
    machine_group_id: int,
    machine_group: MachineGroupUpdate,
    machine_group_service: MachineGroupService = Depends(Provide[Container.machine_group_service]),
    current_user: Dict[str, Any] = Depends(permission_required(MACHINE_GROUP_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a machine group.
    
    Requires machine_group:update permission.
    """
    updated_machine_group = machine_group_service.update_machine_group(
        machine_group_id,
        machine_group.name,
        machine_group.description,
        machine_group.is_active,
        machine_group.failure
    )
    if updated_machine_group is None:
        raise HTTPException(status_code=404, detail="Machine group not found")
    return updated_machine_group

@router.delete("/{machine_group_id}", status_code=204, summary="Delete Machine Group")
@inject
def delete_machine_group(
    machine_group_id: int,
    machine_group_service: MachineGroupService = Depends(Provide[Container.machine_group_service]),
    current_user: Dict[str, Any] = Depends(permission_required(MACHINE_GROUP_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a machine group.
    
    Requires machine_group:delete permission.
    """
    result = machine_group_service.delete_machine_group(machine_group_id)
    if not result["success"]:
        if result["reason"] == "not_found":
            raise HTTPException(status_code=404, detail="Machine group not found")
        elif result["reason"] == "has_stations":
            raise HTTPException(
                status_code=409, 
                detail="Cannot delete machine group because it has associated stations. Remove the stations first."
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to delete machine group")
