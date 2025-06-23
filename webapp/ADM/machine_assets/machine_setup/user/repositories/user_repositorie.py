"""User repository."""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from webapp.ADM.machine_assets.machine_setup.user.models.user_model import User
from webapp.auth.utils import get_password_hash

class UserNotFoundError(Exception):
    """User not found error."""
    pass

class UserRepository:
    """User repository class."""

    def __init__(self, session_factory):
        """Initialize user repository."""
        self._session_factory = session_factory

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all users as dictionaries."""
        with self._session_factory() as session:
            users = session.query(User).all()
            return [
                {
                    "id": user.id,
                    "email": user.email,
                    "is_active": user.is_active,
                    "role": user.role,
                    "permissions": user.permissions or []
                }
                for user in users
            ]

    def get_by_id(self, user_id: int) -> Dict[str, Any]:
        """Get user by ID as dictionary."""
        with self._session_factory() as session:
            user = session.query(User).get(user_id)
            if user is None:
                raise UserNotFoundError(f"User with ID {user_id} not found")
            return {
                "id": user.id,
                "email": user.email,
                "is_active": user.is_active,
                "role": user.role,
                "permissions": user.permissions or []
            }

    def get_by_email(self, email: str) -> Dict[str, Any]:
        """Get user by email as dictionary."""
        with self._session_factory() as session:
            user = session.query(User).filter(User.email == email).first()
            if user is None:
                raise UserNotFoundError(f"User with email {email} not found")
            return {
                "id": user.id,
                "email": user.email,
                "is_active": user.is_active,
                "role": user.role,
                "permissions": user.permissions or []
            }

    def get_user_for_auth(self, email: str) -> Dict[str, Any]:
        """Get user model for authentication."""
        with self._session_factory() as session:
            user = session.query(User).filter(User.email == email).first()
            if user is None:
                raise UserNotFoundError(f"User with email {email} not found")
            # Return dictionary instead of SQLAlchemy model
            return {
                "id": user.id,
                "email": user.email,
                "hashed_password": user.hashed_password,
                "is_active": user.is_active,
                "role": user.role,
                "permissions": user.permissions or []
            }

    def add(self, email: str, password: str, is_active: bool = True, role: str = "user", permissions: List[str] = None) -> Dict[str, Any]:
        """Add a new user and return as dictionary."""
        with self._session_factory() as session:
            hashed_password = get_password_hash(password)
            user = User(
                email=email,
                hashed_password=hashed_password,
                is_active=is_active,
                role=role,
                permissions=permissions or []
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return {
                "id": user.id,
                "email": user.email,
                "is_active": user.is_active,
                "role": user.role,
                "permissions": user.permissions or []
            }

    def update(self, user_id: int, **kwargs) -> Dict[str, Any]:
        """Update user and return as dictionary."""
        with self._session_factory() as session:
            user = session.query(User).get(user_id)
            if user is None:
                raise UserNotFoundError(f"User with ID {user_id} not found")
            
            for key, value in kwargs.items():
                if key == "password":
                    user.hashed_password = get_password_hash(value)
                else:
                    setattr(user, key, value)
            
            session.commit()
            session.refresh(user)
            return {
                "id": user.id,
                "email": user.email,
                "is_active": user.is_active,
                "role": user.role,
                "permissions": user.permissions or []
            }

    def delete(self, user_id: int) -> None:
        """Delete user by ID."""
        with self._session_factory() as session:
            user = session.query(User).get(user_id)
            if user is None:
                raise UserNotFoundError(f"User with ID {user_id} not found")
            session.delete(user)
            session.commit()