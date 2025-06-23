"""Authentication routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from dependency_injector.wiring import inject, Provide
from IIOT.containers import Container
from IIOT.auth.service import AuthService
from IIOT.auth.schemas import Token
from IIOT.ADM.machine_assets.machine_setup.user.services.user_service import UserService

router = APIRouter(tags=["auth"])

@router.post("/token", response_model=Token)
@inject
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(Provide[Container.user_service])
):
    """Get access token for user."""
    auth_service = AuthService.get_instance(user_service)
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return auth_service.create_user_token(user) 