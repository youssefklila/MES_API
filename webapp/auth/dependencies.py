# webapp/auth/dependencies.py
from typing import List, Optional, Any, Dict
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from dependency_injector.wiring import inject, Provide
from functools import wraps

# Local imports
# Use deferred import to avoid circular imports
# Container will be imported inside the functions
from webapp.ADM.machine_assets.machine_setup.user.services.user_service import UserService, AVAILABLE_PERMISSIONS
from webapp.ADM.machine_assets.machine_setup.user.repositories.user_repositorie import UserNotFoundError
from webapp.ADM.machine_assets.machine_setup.user.models.user_model import User
from webapp.auth.config import SECRET_KEY, ALGORITHM
from webapp.auth.utils import verify_token

# Use the centralized auth endpoint for token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class TokenData:
    """Token data model."""
    def __init__(self, email: Optional[str] = None, role: Optional[str] = "user", permissions: List[str] = None):
        self.email = email
        self.role = role
        self.permissions = permissions or []


def validate_permissions(permissions: List[str]) -> List[str]:
    """Validate that all permissions exist in our system"""
    valid_permissions = {
        # Cell permissions
        "cell:create", "cell:read", "cell:update", "cell:delete",
        # Client permissions
        "client:create", "client:read", "client:update", "client:delete",
        # User permissions
        "user:create", "user:read", "user:update", "user:delete",
        # Machine Condition Group permissions
        "machine_condition_group:create", "machine_condition_group:read", 
        "machine_condition_group:update", "machine_condition_group:delete",
        # Machine Condition permissions
        "machine_condition:create", "machine_condition:read", 
        "machine_condition:update", "machine_condition:delete",
        # Machine Condition Data permissions
        "machine_condition_data:create", "machine_condition_data:read", 
        "machine_condition_data:update", "machine_condition_data:delete",
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
        token: str = Depends(oauth2_scheme),
    ):
        """Check if user has required permission."""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            # Verify the token
            payload = verify_token(token)
            if payload is None:
                raise credentials_exception
                
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            
            # Get user role and permissions from token
            role = payload.get("role", "user")
            permissions = payload.get("permissions", [])
            
            # Admin role has all permissions
            if role == "admin":
                return {
                    "email": email,
                    "role": role,
                    "permissions": permissions,
                    "is_active": True
                }
                
            # Check if user has the required permission
            if required_permission not in permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"User does not have permission: {required_permission}",
                )
                
            return {
                "email": email,
                "role": role,
                "permissions": permissions,
                "is_active": True
            }
                
        except Exception as e:
            print(f"Error in permission_required: {str(e)}")
            raise credentials_exception
        
    return check_permission


@inject
async def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> Dict[str, Any]:
    """
    Get the current authenticated user from the token.
    
    Args:
        token: The JWT token
        
    Returns:
        The current user as a dictionary
        
    Raises:
        HTTPException: If the token is invalid or the user is not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Verify the token
        payload = verify_token(token)
        if payload is None:
            raise credentials_exception
            
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        
        # Get user role and permissions from token
        role = payload.get("role", "user")
        permissions = payload.get("permissions", [])
        
        # Return user data from token
        return {
            "email": email,
            "role": role,
            "permissions": permissions,
            "is_active": True
        }
        
    except Exception as e:
        print(f"Error in get_current_user: {str(e)}")
        raise credentials_exception


def role_required(role: str):
    """Dependency wrapper to check if user has required role."""
    @inject
    async def check_role(
        current_user: Dict[str, Any] = Depends(get_current_user),
    ):
        """Check if user has required role."""
        # Admin role has all permissions
        if current_user.get("role") == "admin":
            return current_user
            
        # Check if user has the required role
        if current_user.get("role") != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have required role: {role}",
            )
            
        return current_user
        
    return check_role


def validate_user_permissions(permissions: List[str]):
    """Validate a list of permissions."""
    all_permissions = []
    
    # Generate all available permissions
    for resource, actions in AVAILABLE_PERMISSIONS.items():
        for action in actions:
            all_permissions.append(f"{resource}:{action}")
    
    # Check if all permissions are valid
    invalid_permissions = [p for p in permissions if p not in all_permissions]
    if invalid_permissions:
        raise ValueError(f"Invalid permissions: {', '.join(invalid_permissions)}")
        
    return permissions