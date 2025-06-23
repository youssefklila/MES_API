"""Endpoints module."""

from fastapi import APIRouter, Depends, Response, status, HTTPException
from dependency_injector.wiring import inject, Provide
from typing import Dict, Any, List
import sqlalchemy.exc

from webapp.ADM.machine_assets.machine_setup.client.schemas.client_schema import ClientUpdate, ClientResponse
from webapp.ADM.machine_assets.machine_setup.client.services.client_service import ClientService
from webapp.ADM.machine_assets.machine_setup.user.repositories.user_repositorie import UserNotFoundError
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

router = APIRouter(tags=["clients"])

# Permission constants
CLIENT_READ_PERM = "client:read"
CLIENT_CREATE_PERM = "client:create"
CLIENT_UPDATE_PERM = "client:update"
CLIENT_DELETE_PERM = "client:delete"

@router.get("/clients", response_model=List[ClientResponse])
@inject
def get_clients(
    client_service: ClientService = Depends(Provide[Container.client_service]),
    current_user: Dict[str, Any] = Depends(permission_required(CLIENT_READ_PERM))
):
    """Get all clients (requires client:read permission)."""
    return client_service.get_clients()

@router.get("/clients/{client_id}", response_model=ClientResponse)
@inject
def get_client_by_id(
    client_id: int,
    client_service: ClientService = Depends(Provide[Container.client_service]),
    current_user: Dict[str, Any] = Depends(permission_required(CLIENT_READ_PERM))
):
    """Get a specific client by ID (requires client:read permission)."""
    client = client_service.get_client_by_id(client_id)
    if not client:
        raise HTTPException(status_code=404, detail=f"Client with ID {client_id} not found")
    return client

@router.post("/clients", response_model=ClientResponse, status_code=201)
@inject
def add_client(
    client: ClientUpdate,
    client_service: ClientService = Depends(Provide[Container.client_service]),
    current_user: Dict[str, Any] = Depends(permission_required(CLIENT_CREATE_PERM))
):
    """Add a new client (requires client:create permission)."""
    try:
        return client_service.create_client(
            user_id=client.user_id,
            company_code=client.company_code,
            name=client.name,
            description=client.description
        )
    except sqlalchemy.exc.IntegrityError as e:
        if "clients_company_code_key" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A client with company code '{client.company_code}' already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create client due to database constraint violation"
        )

@router.delete("/clients/{client_id}", status_code=204)
@inject
def remove_client(
    client_id: int,
    client_service: ClientService = Depends(Provide[Container.client_service]),
    current_user: Dict[str, Any] = Depends(permission_required(CLIENT_DELETE_PERM))
):
    """Delete a client by ID (requires client:delete permission)."""
    try:
        client_service.delete_client_by_id(client_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with ID {client_id} not found"
        )

@router.put("/clients/{client_id}", response_model=ClientResponse)
@inject
def update_client(
    client_id: int,
    client: ClientUpdate,
    client_service: ClientService = Depends(Provide[Container.client_service]),
    current_user: Dict[str, Any] = Depends(permission_required(CLIENT_UPDATE_PERM))
):
    """Update a client by ID (requires client:update permission)."""
    try:
        updated_client = client_service.update_client(
            client_id=client_id,
            user_id=client.user_id,
            company_code=client.company_code,
            name=client.name,
            description=client.description
        )
        if not updated_client:
            raise HTTPException(status_code=404, detail=f"Client with ID {client_id} not found")
        return updated_client
    except sqlalchemy.exc.IntegrityError as e:
        if "clients_company_code_key" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A client with company code '{client.company_code}' already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not update client due to database constraint violation"
        )
