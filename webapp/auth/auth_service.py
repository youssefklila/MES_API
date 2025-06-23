"""Authentication service module."""
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from jose import JWTError, jwt
import traceback

from webapp.ADM.machine_assets.machine_setup.user.models.user_model import User
from webapp.database import Database
from webapp.auth.utils import verify_password, get_password_hash, create_access_token, verify_token
from webapp.ADM.machine_assets.machine_setup.user.services.user_service import UserService
from webapp.ADM.machine_assets.machine_setup.user.repositories.user_repositorie import UserNotFoundError
from webapp.auth.permission import API_PERMISSIONS
from webapp.auth.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

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
                
                # Verify the password using the utility function
                if not verify_password(password, user.hashed_password):
                    print("Invalid password")
                    return None
                
                # Create access token with all necessary user data
                access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                
                # Ensure permissions is a list, not None
                permissions = user.permissions if user.permissions else []
                
                # Create token payload
                token_data = {
                    "sub": user.email,
                    "role": user.role,
                    "permissions": permissions
                }
                
                print(f"Creating token with data: {token_data}")
                access_token = create_access_token(
                    data=token_data,
                    expires_delta=access_token_expires
                )
                
                # Return the token and user data
                return {
                    "access_token": access_token,
                    "token_type": "bearer",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "role": user.role,
                        "permissions": permissions
                    }
                }
                
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            traceback.print_exc()
            return None
            
    def verify_user_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify a user token and return the user data if valid."""
        try:
            # Decode the token
            payload = verify_token(token)
            if not payload:
                return None
                
            # Get the email from the token
            email = payload.get("sub")
            if not email:
                return None
                
            # Get the user from the database
            try:
                user = self._user_service.get_user_by_email(email)
                return user
            except UserNotFoundError:
                # If user not found but token is valid, return minimal user data
                return {
                    "email": email,
                    "role": payload.get("role", "user"),
                    "permissions": payload.get("permissions", []),
                    "is_active": True,
                    "id": None
                }
        except Exception as e:
            print(f"Token verification error: {str(e)}")
            return None