"""Authentication endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from dependency_injector.wiring import inject, Provide
from typing import Dict, Any

from IIOT.containers import Container
from IIOT.auth.auth_service import AuthService

# Create router without prefix - the prefix will be added in the main app
router = APIRouter(tags=["auth"])

# Update the tokenUrl to match our endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.post("/token", response_model=Dict[str, Any])
@inject
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(Provide[Container.auth_service])
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    try:
        result = await auth_service.authenticate_user(form_data.username, form_data.password)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return result
    except Exception as e:
        print(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during authentication"
        )