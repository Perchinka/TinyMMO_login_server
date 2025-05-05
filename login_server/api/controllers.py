from fastapi import APIRouter, HTTPException, status, Depends

from login_server.api.schemas import (
    RegisterRequest, RegisterResponse,
    LoginRequest,     LoginResponse
)
from login_server.services.user_service import UserService
from login_server.infra.unit_of_work import UnitOfWork
from .dependencies import get_adapter, get_challenge_mgr, get_crypto_utils

router = APIRouter(tags=["auth"])

@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    req: RegisterRequest,
    adapter      = Depends(get_adapter),
    challenge_mgr= Depends(get_challenge_mgr),
    crypto_utils = Depends(get_crypto_utils),
):
    with UnitOfWork(adapter) as uow:
        svc = UserService(uow.users, challenge_mgr, crypto_utils)
        ok = svc.register(req.username, req.password)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    return RegisterResponse(success=True)

@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK
)
def login(
    req: LoginRequest,
    adapter      = Depends(get_adapter),
    challenge_mgr= Depends(get_challenge_mgr),
    crypto_utils = Depends(get_crypto_utils),
):
    with UnitOfWork(adapter) as uow:
        svc = UserService(uow.users, challenge_mgr, crypto_utils)
        ok = svc.authenticate(req.username, req.client_response)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return LoginResponse(success=True)
