"""User endpoints with authentication and authorization."""
from fastapi import APIRouter, Depends, HTTPException, Response, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dependency_injector.wiring import inject, Provide
from typing import List, Dict, Any, Optional
from sqlalchemy.exc import IntegrityError
import traceback
from datetime import timedelta

from IIOT.auth.schemas import UserCreate, UserUpdate, UserResponse, Token
from IIOT.containers import Container
from IIOT.ADM.machine_assets.machine_setup.user.services.user_service import (
    UserService,
    AVAILABLE_PERMISSIONS
)
from IIOT.ADM.machine_assets.machine_setup.user.repositories.user_repositorie import UserNotFoundError
from IIOT.ADM.machine_assets.machine_setup.user.models.user_model import User
from IIOT.database import Database
from IIOT.auth.utils import get_password_hash, verify_password, create_access_token
from IIOT.auth.dependencies import get_current_user, permission_required

router = APIRouter(tags=["Users"], prefix="/users")

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Permission constants
USER_READ_PERM = "user:read"
USER_CREATE_PERM = "user:create"
USER_UPDATE_PERM = "user:update"
USER_DELETE_PERM = "user:delete"

@router.get("/")
@inject
async def get_list(
    user_service: UserService = Depends(Provide[Container.user_service]),
    current_user: Dict[str, Any] = Depends(permission_required(USER_READ_PERM))
):
    """Get all users (requires user:read permission)."""
    try:
        return user_service.get_all_users()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{user_id}")
@inject
async def get_by_id(
    user_id: int,
    user_service: UserService = Depends(Provide[Container.user_service]),
    current_user: Dict[str, Any] = Depends(permission_required(USER_READ_PERM))
):
    """Get user by ID (requires user:read permission)."""
    try:
        user = user_service.get_user_by_id(user_id)
        return user
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.post("/register-admin", status_code=status.HTTP_201_CREATED)
@inject
async def register_admin(
    user_data: UserCreate,
    db: Database = Depends(Provide[Container.db])
):
    """
    Register an admin user with all permissions.
    This endpoint remains public for initial setup.
    """
    try:
        with db.session() as session:
            # Check if a user with this email already exists
            existing_user = session.query(User).filter(User.email == user_data.email).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists"
                )
            
            # Generate all possible permissions
            all_permissions = [
                f"{resource}:{action}"
                for resource in AVAILABLE_PERMISSIONS
                for action in AVAILABLE_PERMISSIONS[resource]
            ]
            
            # Hash the password
            hashed_password = get_password_hash(user_data.password)
            
            # Create the admin user
            new_user = User(
                email=user_data.email,
                hashed_password=hashed_password,
                is_active=True,
                role="admin",
                permissions=all_permissions
            )
            
            # Add and commit
            session.add(new_user)
            session.commit()
            
            # Get user ID before detaching
            user_id = new_user.id
            
            # Reload the user with a fresh query to avoid detached instance issues
            fresh_user = session.query(User).get(user_id)
            
            # Extract all data we need before the session closes
            response_data = {
                "id": fresh_user.id,
                "email": fresh_user.email,
                "is_active": fresh_user.is_active,
                "role": fresh_user.role,
                "permissions": fresh_user.permissions or []
            }
            
        # Return after session is closed
        return response_data

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create admin user: {str(e)}"
        )

@router.post("/", status_code=status.HTTP_201_CREATED)
@inject
async def create_user(
    user_data: UserCreate,
    db: Database = Depends(Provide[Container.db]),
    current_user: Dict[str, Any] = Depends(permission_required(USER_CREATE_PERM))
):
    """Create new user (requires user:create permission)."""
    try:
        with db.session() as session:
            # Check if a user with this email already exists
            existing_user = session.query(User).filter(User.email == user_data.email).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists"
                )
            
            # Check if this is the first user
            users_count = session.query(User).count()
            is_first_user = users_count == 0
            
            # Set role and permissions
            role = "admin" if is_first_user else user_data.role or "user"
            
            # Set permissions based on role
            if is_first_user:
                permissions = [
                    f"{resource}:{action}"
                    for resource in AVAILABLE_PERMISSIONS
                    for action in AVAILABLE_PERMISSIONS[resource]
                ]
            else:
                permissions = user_data.permissions or []
            
            # Hash the password
            hashed_password = get_password_hash(user_data.password)
            
            # Create the user directly
            new_user = User(
                email=user_data.email,
                hashed_password=hashed_password,
                is_active=user_data.is_active,
                role=role,
                permissions=permissions
            )
            
            # Add and commit
            session.add(new_user)
            session.commit()
            
            # Get user ID before detaching
            user_id = new_user.id
            
            # Reload the user with a fresh query to avoid detached instance issues
            fresh_user = session.query(User).get(user_id)
            
            # Extract all data we need before the session closes
            response_data = {
                "id": fresh_user.id,
                "email": fresh_user.email,
                "is_active": fresh_user.is_active,
                "role": fresh_user.role,
                "permissions": fresh_user.permissions or []
            }
            
        # Return after session is closed
        return response_data

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(Provide[Container.user_service]),
    current_user: Dict[str, Any] = Depends(permission_required(USER_DELETE_PERM))
):
    """Delete user (requires user:delete permission)."""
    try:
        user_service.delete_user(user_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.put("/{user_id}")
@inject
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: UserService = Depends(Provide[Container.user_service]),
    current_user: Dict[str, Any] = Depends(permission_required(USER_UPDATE_PERM))
):
    """Update user (requires user:update permission)."""
    try:
        # Create kwargs for the update method
        update_data = {}
        if user_data.email is not None:
            update_data["email"] = user_data.email
        if user_data.password is not None:
            update_data["password"] = user_data.password
        if user_data.is_active is not None:
            update_data["is_active"] = user_data.is_active
        if user_data.role is not None:
            update_data["role"] = user_data.role
        if user_data.permissions is not None:
            update_data["permissions"] = user_data.permissions

        updated_user = user_service.update_user(user_id, **update_data)
        return updated_user
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.get("/email/{email}")
@inject
async def get_by_email(
    email: str,
    user_service: UserService = Depends(Provide[Container.user_service]),
    current_user: Dict[str, Any] = Depends(permission_required(USER_READ_PERM))
):
    """Get user by email (requires user:read permission)."""
    try:
        user = user_service.get_user_by_email(email)
        return user
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.get("/me")
@inject
async def read_users_me(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get current user's profile (requires authentication)."""
    return current_user 