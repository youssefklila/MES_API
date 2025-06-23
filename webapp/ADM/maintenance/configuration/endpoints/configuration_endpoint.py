# endpoints/configuration_endpoint.py

from fastapi import APIRouter, Depends, HTTPException, Security
from dependency_injector.wiring import inject, Provide
from typing import List, Dict, Any
from fastapi.security import OAuth2PasswordBearer

from webapp.ADM.maintenance.configuration.schemas.configuration_schema import (
    ConfigurationResponse, 
    ConfigurationCreate, 
    ConfigurationUpdate
)
from webapp.ADM.maintenance.configuration.services.configuration_service import ConfigurationService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(
    prefix="/maintenance/configuration",
    tags=["Maintenance Configuration"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}}
)

# Permission constants
CONFIG_READ_PERM = "maintenance:configuration:read"
CONFIG_CREATE_PERM = "maintenance:configuration:create"
CONFIG_UPDATE_PERM = "maintenance:configuration:update"
CONFIG_DELETE_PERM = "maintenance:configuration:delete"

@router.get("/", response_model=List[ConfigurationResponse], summary="Get All Configurations")
@inject
def get_configurations(
    service: ConfigurationService = Depends(Provide[Container.maintenance_configuration_service]),
    current_user: Dict[str, Any] = Depends(permission_required(CONFIG_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all maintenance configurations.
    
    Requires maintenance:configuration:read permission.
    """
    return service.get_all_configurations()

@router.get("/{config_id}", response_model=ConfigurationResponse, summary="Get Configuration")
@inject
def get_configuration(
    config_id: int,
    service: ConfigurationService = Depends(Provide[Container.maintenance_configuration_service]),
    current_user: Dict[str, Any] = Depends(permission_required(CONFIG_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific maintenance configuration by ID.
    
    Requires maintenance:configuration:read permission.
    """
    configuration = service.get_configuration_by_id(config_id)
    if not configuration:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return configuration

@router.post("/", response_model=ConfigurationResponse, status_code=201, summary="Create Configuration")
@inject
def create_configuration(
    data: ConfigurationCreate,
    service: ConfigurationService = Depends(Provide[Container.maintenance_configuration_service]),
    current_user: Dict[str, Any] = Depends(permission_required(CONFIG_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new maintenance configuration.
    
    Requires maintenance:configuration:create permission.
    """
    return service.add_configuration(**data.dict())

@router.put("/{config_id}", response_model=ConfigurationResponse, summary="Update Configuration")
@inject
def update_configuration(
    config_id: int,
    data: ConfigurationUpdate,
    service: ConfigurationService = Depends(Provide[Container.maintenance_configuration_service]),
    current_user: Dict[str, Any] = Depends(permission_required(CONFIG_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a maintenance configuration.
    
    Requires maintenance:configuration:update permission.
    """
    updated_configuration = service.update_configuration(config_id, **data.dict(exclude_unset=True))
    if not updated_configuration:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return updated_configuration

@router.delete("/{config_id}", status_code=204, summary="Delete Configuration")
@inject
def delete_configuration(
    config_id: int,
    service: ConfigurationService = Depends(Provide[Container.maintenance_configuration_service]),
    current_user: Dict[str, Any] = Depends(permission_required(CONFIG_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a maintenance configuration.
    
    Requires maintenance:configuration:delete permission.
    """
    success = service.delete_configuration(config_id)
    if not success:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return {"message": "Configuration deleted successfully"}
