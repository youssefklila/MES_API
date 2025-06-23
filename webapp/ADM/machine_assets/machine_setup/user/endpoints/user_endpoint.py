"""User endpoints with authentication and authorization."""
from fastapi import APIRouter, Depends, HTTPException, Response, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dependency_injector.wiring import inject, Provide
from typing import List, Dict, Any, Optional
from sqlalchemy.exc import IntegrityError
import traceback
from datetime import timedelta

from webapp.auth.schemas import UserCreate, UserUpdate, UserResponse, Token
from webapp.containers import Container
from webapp.ADM.machine_assets.machine_setup.user.services.user_service import (
    UserService,
    AVAILABLE_PERMISSIONS
)
from webapp.ADM.machine_assets.machine_setup.user.repositories.user_repositorie import UserNotFoundError
from webapp.ADM.machine_assets.machine_setup.user.models.user_model import User
from webapp.database import Database
from webapp.auth.utils import get_password_hash, verify_password, create_access_token
from webapp.auth.dependencies import get_current_user, permission_required

router = APIRouter(tags=["users"])

# Permission constants
USER_READ_PERM = "user:read"
USER_CREATE_PERM = "user:create"
USER_UPDATE_PERM = "user:update"
USER_DELETE_PERM = "user:delete"

# OAuth2 scheme for token authentication - use the centralized auth endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Login endpoint - redirect to auth/token
@router.post(
    "/login", 
    response_model=Token, 
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Login successful"},
        401: {"description": "Incorrect email or password"}
    },
    deprecated=True
)
@inject
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Database = Depends(Provide[Container.db])
):
    """
    Login user and return access token.
    
    This endpoint is deprecated. Please use /auth/token instead.
    """
    try:
        with db.session() as session:
            # Get the user model for authentication
            user = session.query(User).filter(User.email == form_data.username).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password"
                )
            
            # Verify password
            if not verify_password(form_data.password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password"
                )
            
            # Check if user is active
            if not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Inactive user"
                )
                
            # Create access token with all necessary user data
            access_token_expires = timedelta(minutes=30)  # 30 minutes
            access_token = create_access_token(
                data={
                    "sub": user.email,
                    "role": user.role,
                    "permissions": user.permissions or []
                },
                expires_delta=access_token_expires
            )
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role,
                    "permissions": user.permissions or []
                }
            }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )


@router.get("/", response_model=List[UserResponse])
@inject
async def get_list(
    user_service: UserService = Depends(Provide[Container.user_service]),
    current_user: Dict[str, Any] = Depends(permission_required(USER_READ_PERM))
):
    """Get all users (requires user:read permission)."""
    try:
        # Get users from database
        return user_service.get_all_users()
    except Exception as e:
        print(f"Error retrieving users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving users: {str(e)}"
        )


@router.get("/{user_id}", response_model=UserResponse)
@inject
async def get_by_id(
    user_id: int,
    user_service: UserService = Depends(Provide[Container.user_service]),
    current_user: Dict[str, Any] = Depends(permission_required(USER_READ_PERM))
):
    """Get user by ID (requires user:read permission)."""
    try:
        return user_service.get_user_by_id(user_id)
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/register-admin", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@inject
async def register_user(
    user_data: UserCreate,
    db: Database = Depends(Provide[Container.db])
):
    """
    Register a new user with all permissions.
    Users created through this endpoint will have all available permissions,
    regardless of the specified role.
    This endpoint remains public for initial setup.
    """
    try:
        with db.session() as session:
            # Check if user already exists
            existing_user = session.query(User).filter(User.email == user_data.email).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

# Always generate all available permissions for users created through this endpoint
            permissions = []
            for resource, actions in AVAILABLE_PERMISSIONS.items():
                for action in actions:
                    permissions.append(f"{resource}:{action}")

            # Create new user
            hashed_password = get_password_hash(user_data.password)
            new_user = User(
                email=user_data.email,
                hashed_password=hashed_password,
                is_active=user_data.is_active,
                role=user_data.role,
                permissions=permissions
            )

            # Add to database
            session.add(new_user)
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

            # Refresh to get the ID
            session.refresh(new_user)

            # Return user data
            return {
                "id": new_user.id,
                "email": new_user.email,
                "is_active": new_user.is_active,
                "role": new_user.role,
                "permissions": new_user.permissions
            }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error registering user: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@inject
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(Provide[Container.user_service]),
    current_user: Dict[str, Any] = Depends(permission_required(USER_CREATE_PERM))
):
    """Create new user (requires user:create permission)."""
    try:
        # If permissions is an empty list, pass None to use the defaults
        permissions = None if not user_data.permissions else user_data.permissions
        
        try:
            # Create user using the service which handles default permissions
            new_user = user_service.create_user(
                email=user_data.email,
                password=user_data.password,
                is_active=user_data.is_active,
                role=user_data.role,
                permissions=permissions
            )
            
            return new_user
            
        except ValueError as e:
            # Handle validation errors from service
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
            
            # Return user data
            return {
                "id": new_user.id,
                "email": new_user.email,
                "is_active": new_user.is_active,
                "role": new_user.role,
                "permissions": new_user.permissions
            }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during user creation"
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
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/{user_id}", response_model=UserResponse)
@inject
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: UserService = Depends(Provide[Container.user_service]),
    current_user: Dict[str, Any] = Depends(permission_required(USER_UPDATE_PERM))
):
    """Update user (requires user:update permission)."""
    try:
        # Validate permissions if provided
        if user_data.permissions:
            for permission in user_data.permissions:
                try:
                    resource, action = permission.split(":")
                    if resource not in AVAILABLE_PERMISSIONS or action not in AVAILABLE_PERMISSIONS[resource]:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid permission: {permission}"
                        )
                except ValueError:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Invalid permission format: {permission}"
                    )
        
        return user_service.update_user(user_id, **user_data.dict(exclude_unset=True))
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/email/{email}", response_model=UserResponse)
@inject
async def get_by_email(
    email: str,
    user_service: UserService = Depends(Provide[Container.user_service]),
    current_user: Dict[str, Any] = Depends(permission_required(USER_READ_PERM))
):
    """Get user by email (requires user:read permission)."""
    try:
        return user_service.get_user_by_email(email)
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/me/id")
@inject
async def get_current_user_id(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Database = Depends(Provide[Container.db])
):
    """Get the ID of the currently logged-in user (requires authentication)."""
    try:
        # The token only contains email, not ID, so we need to fetch the user from DB
        with db.session() as session:
            user = session.query(User).filter(User.email == current_user["email"]).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return {"id": user.id}
    except Exception as e:
        print(f"Error getting user ID: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user ID"
        )