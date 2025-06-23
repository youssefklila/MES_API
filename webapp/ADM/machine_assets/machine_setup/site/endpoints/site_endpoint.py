# endpoints/site_endpoint.py

from fastapi import APIRouter, Depends, HTTPException, Security
from typing import List, Dict, Any
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordBearer

from webapp.ADM.machine_assets.machine_setup.site.schemas.site_schema import SiteResponse, SiteCreate, SiteUpdate
from webapp.ADM.machine_assets.machine_setup.site.services.site_service import SiteService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

router = APIRouter(
    prefix="/sites",
    tags=["Sites"],
    responses={401: {"description": "Unauthorized"}}
)

# Permission constants
SITE_READ_PERM = "site:read"
SITE_CREATE_PERM = "site:create"
SITE_UPDATE_PERM = "site:update"
SITE_DELETE_PERM = "site:delete"

@router.get("/", response_model=List[SiteResponse])
@inject
def get_sites(
    site_service: SiteService = Depends(Provide[Container.site_service]),
    current_user: Dict[str, Any] = Depends(permission_required(SITE_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """Get all sites (requires site:read permission)."""
    return site_service.get_all_sites()

@router.get("/{site_id}", response_model=SiteResponse)
@inject
def get_site(
    site_id: int,
    site_service: SiteService = Depends(Provide[Container.site_service]),
    current_user: Dict[str, Any] = Depends(permission_required(SITE_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """Get a specific site by ID (requires site:read permission)."""
    site = site_service.get_site_by_id(site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site

@router.post("/", response_model=SiteResponse, status_code=201)
@inject
def create_site(
    site_data: SiteCreate,
    site_service: SiteService = Depends(Provide[Container.site_service]),
    current_user: Dict[str, Any] = Depends(permission_required(SITE_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """Create a new site (requires site:create permission)."""
    return site_service.add_site(**site_data.dict())

@router.delete("/{site_id}", status_code=204)
@inject
def delete_site(
    site_id: int,
    site_service: SiteService = Depends(Provide[Container.site_service]),
    current_user: Dict[str, Any] = Depends(permission_required(SITE_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """Delete a site (requires site:delete permission)."""
    site_service.delete_site(site_id)
    return {"message": "Site deleted successfully"}

@router.put("/{site_id}", response_model=SiteResponse)
@inject
def update_site(
    site_id: int,
    site_data: SiteUpdate,
    site_service: SiteService = Depends(Provide[Container.site_service]),
    current_user: Dict[str, Any] = Depends(permission_required(SITE_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """Update a site (requires site:update permission)."""
    return site_service.update_site(site_id, **site_data.dict(exclude_unset=True))
