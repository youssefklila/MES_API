# endpoints/failure_group_type_endpoint.py

from fastapi import APIRouter, Depends, HTTPException, Security, status
from typing import List, Dict, Any
from dependency_injector.wiring import inject, Provide

# Import models and schemas directly
from webapp.ADM.TRACKING.failure_group_type.models.failure_group_type_model import FailureGroupType
from webapp.ADM.TRACKING.failure_group_type.schemas.failure_group_type_schema import (
    FailureGroupTypeCreate,
    FailureGroupTypeResponse,
    FailureGroupTypeUpdate
)

# Use a deferred import for the service to avoid circular imports
from webapp.ADM.TRACKING.failure_group_type.services.failure_group_type_service import FailureGroupTypeService

# Import auth dependencies
from webapp.auth.dependencies import permission_required, oauth2_scheme

router = APIRouter(
    prefix="/failure-group-types",
    tags=["failure-group-types"],
    responses={404: {"description": "Not found"}},
)

# Permission constants
FAILURE_GROUP_TYPE_READ_PERM = "failure_group_type:read"
FAILURE_GROUP_TYPE_CREATE_PERM = "failure_group_type:create"
FAILURE_GROUP_TYPE_UPDATE_PERM = "failure_group_type:update"
FAILURE_GROUP_TYPE_DELETE_PERM = "failure_group_type:delete"

@router.get("/", response_model=List[FailureGroupTypeResponse], summary="Get All Failure Group Types")
@inject
def get_all_failure_group_types(
    failure_group_type_service: FailureGroupTypeService = Depends(Provide["failure_group_type_service"]),
    current_user: Dict[str, Any] = Depends(permission_required(FAILURE_GROUP_TYPE_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all failure group types.
    
    Requires failure_group_type:read permission.
    """
    return failure_group_type_service.get_all_failure_group_types()

@router.get("/{id}", response_model=FailureGroupTypeResponse, summary="Get Failure Group Type")
@inject
def get_failure_group_type(
    id: int,
    failure_group_type_service: FailureGroupTypeService = Depends(Provide["failure_group_type_service"]),
    current_user: Dict[str, Any] = Depends(permission_required(FAILURE_GROUP_TYPE_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific failure group type by ID.
    
    Requires failure_group_type:read permission.
    """
    failure_group_type = failure_group_type_service.get_failure_group_type_by_id(id)
    if not failure_group_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failure group type with ID {id} not found"
        )
    return failure_group_type

@router.post("/", response_model=FailureGroupTypeResponse, status_code=status.HTTP_201_CREATED, summary="Create Failure Group Type")
@inject
def create_failure_group_type(
    failure_group_type_data: FailureGroupTypeCreate,
    failure_group_type_service: FailureGroupTypeService = Depends(Provide["failure_group_type_service"]),
    current_user: Dict[str, Any] = Depends(permission_required(FAILURE_GROUP_TYPE_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new failure group type.
    
    Requires failure_group_type:create permission.
    """
    return failure_group_type_service.create_failure_group_type(
        failure_group_name=failure_group_type_data.failure_group_name,
        failure_group_desc=failure_group_type_data.failure_group_desc
    )

@router.put("/{id}", response_model=FailureGroupTypeResponse, summary="Update Failure Group Type")
@inject
def update_failure_group_type(
    id: int,
    failure_group_type_data: FailureGroupTypeUpdate,
    failure_group_type_service: FailureGroupTypeService = Depends(Provide["failure_group_type_service"]),
    current_user: Dict[str, Any] = Depends(permission_required(FAILURE_GROUP_TYPE_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a failure group type.
    
    Requires failure_group_type:update permission.
    """
    failure_group_type = failure_group_type_service.get_failure_group_type_by_id(id)
    if not failure_group_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failure group type with ID {id} not found"
        )
    
    return failure_group_type_service.update_failure_group_type(
        id=id,
        failure_group_name=failure_group_type_data.failure_group_name,
        failure_group_desc=failure_group_type_data.failure_group_desc
    )

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Failure Group Type")
@inject
def delete_failure_group_type(
    id: int,
    failure_group_type_service: FailureGroupTypeService = Depends(Provide["failure_group_type_service"]),
    current_user: Dict[str, Any] = Depends(permission_required(FAILURE_GROUP_TYPE_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a failure group type.
    
    Requires failure_group_type:delete permission.
    """
    failure_group_type = failure_group_type_service.get_failure_group_type_by_id(id)
    if not failure_group_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failure group type with ID {id} not found"
        )
    
    failure_group_type_service.delete_failure_group_type(id)
    return None

@router.get("/name/{failure_group_name}", response_model=FailureGroupTypeResponse, summary="Get Failure Group Type by Name")
@inject
def get_failure_group_type_by_name(
    failure_group_name: str,
    failure_group_type_service: FailureGroupTypeService = Depends(Provide["failure_group_type_service"]),
    current_user: Dict[str, Any] = Depends(permission_required(FAILURE_GROUP_TYPE_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific failure group type by name.
    
    Requires failure_group_type:read permission.
    """
    failure_group_type = failure_group_type_service.get_failure_group_type_by_name(failure_group_name)
    if not failure_group_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failure group type with name {failure_group_name} not found"
        )
    return failure_group_type
