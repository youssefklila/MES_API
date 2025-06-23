"""User service implementation."""
from typing import List, Optional, Dict, Any
from webapp.ADM.machine_assets.machine_setup.user.models.user_model import User
from webapp.ADM.machine_assets.machine_setup.user.repositories.user_repositorie import UserRepository, UserNotFoundError
from webapp.auth.utils import get_password_hash
from webapp.database import Database

# Define available permissions for different roles
AVAILABLE_PERMISSIONS = {
    "cell": ["create", "read", "update", "delete"],
    "client": ["create", "read", "update", "delete"],
    "user": ["create", "read", "update", "delete"],
    "company_code": ["create", "read", "update", "delete"],
    "site": ["create", "read", "update", "delete"],
    "machine_group": ["create", "read", "update", "delete"],
    "station": ["create", "read", "update", "delete"],
    "erp_group": ["create", "read", "update", "delete"],
    "unit": ["create", "read", "update", "delete"],
    "workplan": ["create", "read", "update", "delete"],
    "workplan_type": ["create", "read", "update", "delete"],
    "workstep": ["create", "read", "update", "delete"],
    "assign_station": ["create", "read", "delete"],
    "part_group": ["create", "read", "update", "delete"],
    "part_master": ["create", "read", "update", "delete"],
    "part_type": ["create", "read", "update", "delete"],
    "part_group_type": ["create", "read", "update", "delete"],
    "workorder": ["create", "read", "update", "delete"],
    "booking": ["create", "read", "update", "delete"],
    "failure_type": ["create", "read", "update", "delete"],
    "failure_group_type": ["create", "read", "update", "delete"],
    "measurement_data": ["create", "read", "update", "delete"],
    "machine_condition_group": ["create", "read", "update", "delete"],
    "machine_condition": ["create", "read", "update", "delete"],
    "machine_condition_data": ["create", "read", "update", "delete"],
    "bom": ["create", "read", "update", "delete"],
    "bom_header": ["create", "read", "update", "delete"],
    "bom_item": ["create", "read", "update", "delete"],
    "line": ["create", "read", "update", "delete"],
    "iiot_sensor_data": ["create", "read", "update", "delete"],
    "active_workorder": ["create", "read", "update", "delete"],
    "maintenance:configuration": ["create", "read", "update", "delete"],
    "maintenance:localStorage": ["create", "read", "update", "delete"],
    "task": ["create", "read", "update", "delete"],
    "report": ["create", "read", "update", "delete"]
}

class UserService:
    """Service for handling user operations."""

    def __init__(self, user_repository: UserRepository):
        """Initialize user service."""
        self._user_repository = user_repository

    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users as dictionaries."""
        return self._user_repository.get_all()

    def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        """Get user by ID."""
        return self._user_repository.get_by_id(user_id)

    def get_user_by_email(self, email: str) -> Dict[str, Any]:
        """Get user by email."""
        return self._user_repository.get_by_email(email)

    def get_user_for_auth(self, email: str) -> User:
        """Get user model for authentication."""
        return self._user_repository.get_user_for_auth(email)

    def create_user(self, email: str, password: str, is_active: bool = True, role: str = "user", permissions: List[str] = None) -> Dict[str, Any]:
        """Create a new user."""
        # Validate role
        if role not in ["admin", "user"]:
            raise ValueError("Invalid role. Must be 'admin' or 'user'")
            
        # Set default permissions based on role if none provided
        if permissions is None:
            if role == "admin":
                # Admin gets all permissions
                permissions = []
                for resource, actions in AVAILABLE_PERMISSIONS.items():
                    for action in actions:
                        permissions.append(f"{resource}:{action}")
            else:
                # Regular user gets default read permissions
                permissions = [
                    # Basic read permissions
                    "user:read",
                    "workplan:read",
                    "workorder:read",
                    "booking:read",
                    "task:read",
                    "report:read",
                    # Add more default permissions as needed
                ]

        # Validate permissions
        if permissions:
            for permission in permissions:
                resource, action = permission.split(":")
                if resource not in AVAILABLE_PERMISSIONS or action not in AVAILABLE_PERMISSIONS[resource]:
                    raise ValueError(f"Invalid permission: {permission}")

        # Hash password
        hashed_password = get_password_hash(password)

        # Create user with hashed password
        return self._user_repository.add(
            email=email,
            password=hashed_password,  # Repository expects 'password' param but will store as 'hashed_password'
            is_active=is_active,
            role=role,
            permissions=permissions or []
        )

    def update_user(self, user_id: int, **kwargs) -> Dict[str, Any]:
        """Update user."""
        if "password" in kwargs:
            # Hash the password if it's being updated
            kwargs["password"] = get_password_hash(kwargs["password"])
        return self._user_repository.update(user_id, **kwargs)

    def delete_user(self, user_id: int) -> None:
        """Delete user."""
        self._user_repository.delete(user_id)

    def _user_to_response(self, user: User) -> Dict[str, Any]:
        """Convert user model to response schema."""
        return {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active,
            "role": user.role,
            "permissions": user.permissions or []
        }