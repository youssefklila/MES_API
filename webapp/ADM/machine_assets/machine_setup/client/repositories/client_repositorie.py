"""Repositories module."""

from contextlib import AbstractContextManager
from typing import Callable, Iterator, List, Dict, Any

from sqlalchemy.orm import Session

from webapp.ADM.machine_assets.machine_setup.cell.exceptions.client_exception import ClientNotFoundError
from webapp.ADM.machine_assets.machine_setup.client.models.client_model import Client


class ClientRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def _to_dict(self, client: Client) -> Dict[str, Any]:
        """Convert a Client model instance to a dictionary."""
        return {
            "id": client.id,
            "user_id": client.user_id,
            "company_code": client.company_code,
            "name": client.name,
            "description": client.description
        }

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all clients as dictionaries."""
        with self.session_factory() as session:
            clients = session.query(Client).all()
            return [self._to_dict(client) for client in clients]

    def get_by_id(self, client_id: int) -> Dict[str, Any]:
        """Get client by ID as dictionary."""
        with self.session_factory() as session:
            client = session.query(Client).filter(Client.id == client_id).first()
            if not client:
                raise ClientNotFoundError(client_id)
            return self._to_dict(client)

    def add(self, user_id: int, company_code: str, name: str, description: str) -> Dict[str, Any]:
        """Add a new client and return as dictionary."""
        with self.session_factory() as session:
            client = Client(user_id=user_id, company_code=company_code, name=name, description=description)
            session.add(client)
            session.commit()
            session.refresh(client)
            return self._to_dict(client)

    def delete_by_id(self, client_id: int) -> None:
        """Delete a client by ID."""
        with self.session_factory() as session:
            client = session.query(Client).filter(Client.id == client_id).first()
            if not client:
                raise ClientNotFoundError(client_id)
            session.delete(client)
            session.commit()

    def update_client(self, client_id: int, user_id: int = None, company_code: str = None, name: str = None, description: str = None) -> Dict[str, Any]:
        """Update a client and return as dictionary."""
        with self.session_factory() as session:
            client = session.query(Client).filter(Client.id == client_id).first()
            if not client:
                raise ClientNotFoundError(client_id)

            if user_id is not None:
                client.user_id = user_id
            if company_code is not None:
                client.company_code = company_code
            if name is not None:
                client.name = name
            if description is not None:
                client.description = description

            session.commit()
            session.refresh(client)
            return self._to_dict(client)