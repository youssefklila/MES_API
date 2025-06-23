"""Services module."""

from typing import List, Dict, Any, Optional

from webapp.ADM.machine_assets.machine_setup.client.models.client_model import Client
from webapp.ADM.machine_assets.machine_setup.client.repositories.client_repositorie import ClientRepository
from webapp.ADM.machine_assets.machine_setup.client.schemas.client_schema import ClientResponse


class ClientService:

    def __init__(self, client_repository: ClientRepository) -> None:
        self._repository = client_repository

    def get_clients(self) -> List[ClientResponse]:
        """Get all clients."""
        clients = self._repository.get_all()
        return [ClientResponse(**client) for client in clients]

    def get_client_by_id(self, client_id: int) -> Optional[ClientResponse]:
        """Get a client by ID."""
        try:
            client = self._repository.get_by_id(client_id)
            return ClientResponse(**client) if client else None
        except Exception:
            return None

    def create_client(self, user_id: int, company_code: str, name: str, description: str) -> ClientResponse:
        """Create a new client."""
        client = self._repository.add(user_id, company_code, name, description)
        return ClientResponse(**client)

    def delete_client_by_id(self, client_id: int) -> None:
        """Delete a client by ID."""
        return self._repository.delete_by_id(client_id)

    def update_client(self, client_id: int, user_id: int, company_code: str, name: str, description: str) -> Optional[ClientResponse]:
        """Update a client."""
        try:
            client = self._repository.update_client(client_id, user_id, company_code, name, description)
            return ClientResponse(**client) if client else None
        except Exception:
            return None