# endpoints/cell_endpoint.py
from fastapi import APIRouter, Depends, HTTPException, Security
from typing import List, Dict, Any
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordBearer

from ..services.cell_service import CellService
from ..schemas.cell_schema import CellCreate, CellUpdate, CellResponse
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required
from webapp.ADM.machine_assets.machine_setup.user.services.user_service import UserService

# OAuth2 scheme for token authentication - use the centralized auth endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(
    tags=["cells"],
    responses={401: {"description": "Unauthorized"}}
)

# Permission constants
CELL_READ_PERM = "cell:read"
CELL_CREATE_PERM = "cell:create"
CELL_UPDATE_PERM = "cell:update"
CELL_DELETE_PERM = "cell:delete"

@router.get("/", response_model=List[CellResponse])
@inject
def get_cells(
    cell_service: CellService = Depends(Provide[Container.cell_service]),
    current_user: Dict[str, Any] = Depends(permission_required(CELL_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """Get all cells (requires cell:read permission)."""
    return cell_service.get_cells()

@router.get("/{cell_id}", response_model=CellResponse)
@inject
def get_cell(
    cell_id: int,
    cell_service: CellService = Depends(Provide[Container.cell_service]),
    current_user: Dict[str, Any] = Depends(permission_required(CELL_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """Get a specific cell by ID (requires cell:read permission)."""
    cell = cell_service.get_cell_by_id(cell_id)
    if not cell:
        raise HTTPException(status_code=404, detail="Cell not found")
    return cell

@router.post("/", response_model=CellResponse, status_code=201)
@inject
def create_cell(
    cell_create: CellCreate,
    cell_service: CellService = Depends(Provide[Container.cell_service]),
    user_service: UserService = Depends(Provide[Container.user_service]),
    current_user: Dict[str, Any] = Depends(permission_required(CELL_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """Create a new cell (requires cell:create permission)."""
    # Get user ID from email
    email = current_user.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="User email not found in token")
    
    user = user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_id = user.get("id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID not found")
    
    return cell_service.create_cell(
        user_id=user_id,
        site_id=cell_create.site_id,
        name=cell_create.name,
        description=cell_create.description,
        info=cell_create.info,
        is_active=cell_create.is_active
    )

@router.put("/{cell_id}", response_model=CellResponse)
@inject
def update_cell(
    cell_id: int,
    cell_update: CellUpdate,
    cell_service: CellService = Depends(Provide[Container.cell_service]),
    user_service: UserService = Depends(Provide[Container.user_service]),
    current_user: Dict[str, Any] = Depends(permission_required(CELL_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """Update a cell (requires cell:update permission)."""
    # Get user ID from email
    email = current_user.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="User email not found in token")
    
    user = user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_id = user.get("id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID not found")
    
    updated_cell = cell_service.update_cell(
        cell_id=cell_id,
        user_id=user_id,
        site_id=cell_update.site_id,
        name=cell_update.name,
        description=cell_update.description,
        info=cell_update.info,
        is_active=cell_update.is_active
    )
    if not updated_cell:
        raise HTTPException(status_code=404, detail="Cell not found")
    return updated_cell

@router.delete("/{cell_id}", status_code=204)
@inject
def delete_cell(
    cell_id: int,
    cell_service: CellService = Depends(Provide[Container.cell_service]),
    current_user: Dict[str, Any] = Depends(permission_required(CELL_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """Delete a cell (requires cell:delete permission)."""
    if not cell_service.delete_cell_by_id(cell_id):
        raise HTTPException(status_code=404, detail="Cell not found")