# IIOT/auth/dependencies.py
from typing import List, Optional, Any, Dict
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from dependency_injector.wiring import inject, Provide
from functools import wraps

# Local imports
from IIOT.containers import Container
from IIOT.ADM.machine_assets.machine_setup.user.services.user_service import UserService
from IIOT.ADM.machine_assets.machine_setup.user.repositories.user_repositorie import UserNotFoundError
from IIOT.ADM.machine_assets.machine_setup.user.models.user_model import User
from IIOT.auth.config import SECRET_KEY, ALGORITHM
from IIOT.auth.utils import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class TokenData:
    """Token data model."""
    def __init__(self, email: Optional[str] = None, role: Optional[str] = "user", permissions: List[str] = None):
        self.email = email
        self.role = role
        self.permissions = permissions or []


def validate_permissions(permissions: List[str]) -> List[str]:
    """Validate that all permissions exist in our system"""
    valid_permissions = {
        "user:create", "user:read", "user:update", "user:delete",
        # Add other permissions as needed
    }

    invalid_perms = [p for p in permissions if p not in valid_permissions]
    if invalid_perms:
        raise ValueError(f"Invalid permissions: {', '.join(invalid_perms)}")
    return permissions


def permission_required(required_permission: str):
    """Dependency to check if user has required permission."""
    @inject
    async def check_permission(
        current_user: Dict[str, Any] = Depends(get_current_user),
        user_service: UserService = Depends(Provide[Container.user_service])
    ) -> Dict[str, Any]:
        # Get fresh user instance from database to ensure session is active
        user = user_service.get_user_for_auth(current_user["email"])
        if not user or not user.get("permissions"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        # Check if user has the required permission
        if required_permission not in user["permissions"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{required_permission}' required"
            )
        
        return user
    return check_permission


@inject
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(Provide[Container.user_service])
) -> Dict[str, Any]:
    """
    Get the current authenticated user from the token.
    
    Args:
        token: The JWT token
        user_service: The user service
        
    Returns:
        The current user as a dictionary
        
    Raises:
        HTTPException: If the token is invalid or the user is not found
    """
    try:
        # Verify the token
        payload = verify_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get the user from the database
        user = user_service.get_user_for_auth(email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Verify that the user is active
        if not user["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_current_user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def role_required(role: str):
    """Dependency wrapper to check if user has required role."""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: Dict[str, Any] = Depends(get_current_user), **kwargs):
            if not current_user["is_active"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Inactive user"
                )

            if current_user["role"] != role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Role {role} required"
                )
            return await func(*args, current_user=current_user, **kwargs)

        return wrapper

    return decorator


def validate_user_permissions(permissions: List[str]) -> List[str]:
    """Validate a list of permissions."""
    from IIOT.ADM.machine_assets.machine_setup.user.services.user_service import AVAILABLE_PERMISSIONS

    valid_permissions = []
    for permission in permissions:
        try:
            resource, action = permission.split(":")
            if resource in AVAILABLE_PERMISSIONS and action in AVAILABLE_PERMISSIONS[resource]:
                valid_permissions.append(permission)
        except ValueError:
            continue

    if not valid_permissions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid permissions provided"
        )

    return valid_permissions