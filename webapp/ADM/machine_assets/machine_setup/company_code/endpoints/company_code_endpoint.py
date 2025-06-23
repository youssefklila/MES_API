# endpoints/company_code_endpoint.py

from fastapi import APIRouter, Depends, HTTPException, Security
from typing import List, Dict, Any
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordBearer

from webapp.ADM.machine_assets.machine_setup.company_code.schemas.company_code_schema import CompanyCodeOut, CompanyCodeCreate, \
    CompanyCodeUpdate
from webapp.ADM.machine_assets.machine_setup.company_code.services.company_code_service import CompanyCodeService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

# OAuth2 scheme for token authentication - use the centralized auth endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(
    tags=["company_codes"],
    responses={401: {"description": "Unauthorized"}}
)

# Permission constants
COMPANY_CODE_READ_PERM = "company_code:read"
COMPANY_CODE_CREATE_PERM = "company_code:create"
COMPANY_CODE_UPDATE_PERM = "company_code:update"
COMPANY_CODE_DELETE_PERM = "company_code:delete"

@router.get("/", response_model=List[CompanyCodeOut])
@inject
def get_company_codes(
    company_code_service: CompanyCodeService = Depends(Provide[Container.company_code_service]),
    current_user: Dict[str, Any] = Depends(permission_required(COMPANY_CODE_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """Get all company codes (requires company_code:read permission)."""
    return company_code_service.get_all_company_codes()

@router.get("/{company_code_id}", response_model=CompanyCodeOut)
@inject
def get_company_code(
    company_code_id: int,
    company_code_service: CompanyCodeService = Depends(Provide[Container.company_code_service]),
    current_user: Dict[str, Any] = Depends(permission_required(COMPANY_CODE_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """Get a specific company code by ID (requires company_code:read permission)."""
    company_code = company_code_service.get_company_code_by_id(company_code_id)
    if not company_code:
        raise HTTPException(status_code=404, detail="CompanyCode not found")
    return company_code

@router.post("/", response_model=CompanyCodeOut, status_code=201)
@inject
def create_company_code(
    company_code_create: CompanyCodeCreate,
    company_code_service: CompanyCodeService = Depends(Provide[Container.company_code_service]),
    current_user: Dict[str, Any] = Depends(permission_required(COMPANY_CODE_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """Create a new company code (requires company_code:create permission)."""
    return company_code_service.add_company_code(
        user_id=company_code_create.user_id,
        client_id=company_code_create.client_id,
        name=company_code_create.name,
        description=company_code_create.description
    )

@router.delete("/{company_code_id}", status_code=204)
@inject
def delete_company_code(
    company_code_id: int,
    company_code_service: CompanyCodeService = Depends(Provide[Container.company_code_service]),
    current_user: Dict[str, Any] = Depends(permission_required(COMPANY_CODE_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """Delete a company code (requires company_code:delete permission)."""
    company_code_service.delete_company_code(company_code_id)
    return {"message": "CompanyCode deleted successfully"}

@router.put("/{company_code_id}", response_model=CompanyCodeOut)
@inject
def update_company_code(
    company_code_id: int,
    company_code_update: CompanyCodeUpdate,
    company_code_service: CompanyCodeService = Depends(Provide[Container.company_code_service]),
    current_user: Dict[str, Any] = Depends(permission_required(COMPANY_CODE_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """Update a company code (requires company_code:update permission)."""
    return company_code_service.update_company_code(
        company_code_id,
        user_id=company_code_update.user_id,
        client_id=company_code_update.client_id,
        name=company_code_update.name,
        description=company_code_update.description
    )
