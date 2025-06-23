"""Core authentication utilities."""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Type
from jose import JWTError, jwt
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from IIOT.ADM.machine_assets.machine_setup.user.models.user_model import User
from IIOT.ADM.machine_assets.machine_setup.user.repositories.user_repositorie import UserNotFoundError
from IIOT.auth.permission import API_PERMISSIONS
from IIOT.auth.utils import verify_password

SECRET_KEY = "your-secret-key-keep-it-secret"  # In production, use a secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 525600  # 365 days (365 * 24 * 60 = 525,600 minutes)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

class AuthService:
    """Service for handling authentication operations."""
    
    def __init__(self, user_service):
        self.user_service = user_service

    @classmethod
    def get_instance(cls, user_service) -> 'AuthService':
        """Get an instance of AuthService with injected dependencies."""
        return cls(user_service=user_service)

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user by username and password."""
        try:
            user = self.user_service.get_user_by_email(email=username)
            if not user.is_active:
                return None
            if not verify_password(password, user.password):
                return None
            return user
        except UserNotFoundError:
            return None

    def create_user_token(self, user: User) -> Dict[str, Any]:
        """Create an access token for a user."""
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        permissions = user.permissions if user.role == "user" else list(API_PERMISSIONS.keys())
        
        to_encode = {
            "sub": user.email,
            "role": user.role,
            "permissions": permissions
        }
        access_token = create_access_token(to_encode, expires_delta=access_token_expires)
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }