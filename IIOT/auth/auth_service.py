"""Authentication service module."""
from typing import Optional, Dict, Any
import bcrypt
from datetime import datetime, timedelta
from jose import JWTError, jwt
import traceback
import logging

from IIOT.ADM.machine_assets.machine_setup.user.models.user_model import User
from IIOT.database import Database
from IIOT.auth.utils import verify_password, get_password_hash
from IIOT.auth.service import create_access_token
from IIOT.ADM.machine_assets.machine_setup.user.services.user_service import UserService
from IIOT.ADM.machine_assets.machine_setup.user.repositories.user_repositorie import UserNotFoundError
from IIOT.auth.permission import API_PERMISSIONS
from IIOT.auth.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

logger = logging.getLogger(__name__)

class AuthService:
    """Service for handling authentication operations."""

    def __init__(self, db: Database, user_service: UserService) -> None:
        self.db = db
        self._user_service = user_service

    async def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate a user and return the user object if successful."""
        try:
            print(f"Authenticating user: {email}")
            
            with self.db.session() as session:
                # Query for the user and keep the session open
                user = session.query(User).filter(User.email == email).first()
                
                if not user:
                    print("User not found")
                    return None
                
                if not user.is_active:
                    print("User is not active")
                    return None
                
                # Get the stored hash while session is still open
                stored_hash = user.hashed_password
                
                # Verify the password
                password_bytes = password.encode('utf-8')
                stored_hash_bytes = stored_hash.encode('utf-8')
                
                is_valid = bcrypt.checkpw(password_bytes, stored_hash_bytes)
                print(f"Password verification result: {is_valid}")
                
                if not is_valid:
                    print("Invalid password")
                    return None
                
                # Create access token with all necessary user data
                access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = self.create_access_token(
                    data={
                        "sub": user.email,
                        "role": user.role,
                        "permissions": user.permissions or []
                    },
                    expires_delta=access_token_expires
                )
                
                # Return user data while session is still open
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
                
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            traceback.print_exc()
            return None

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a new JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[dict]:
        """Verify a JWT token and return the decoded payload."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None

    def create_user_token(self, user: User) -> Dict[str, Any]:
        """Generate JWT token for authenticated user."""
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        permissions = user.permissions if user.role == "user" else list(API_PERMISSIONS.keys())

        return {
            "access_token": create_access_token(
                data={
                    "sub": user.email,
                    "role": user.role,
                    "permissions": permissions
                },
                expires_delta=access_token_expires
            ),
            "token_type": "bearer"
        }