from fastapi import APIRouter, HTTPException, status, Depends

from login_server.api.schemas import (
    ChallengeRequest,
    ChallengeResponse,
    AuthRequest,
    AuthResponse,
    RegisterRequest,
    RegisterResponse
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
    challenge_manager= Depends(get_challenge_mgr),
    crypto_utils = Depends(get_crypto_utils),
):
    success: bool = False
    with UnitOfWork(adapter) as uow:
        service = UserService(uow.users, challenge_manager, crypto_utils)
        success = service.register(req.username, req.password)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    return RegisterResponse(success=True)

@router.post(
    "/auth/challenge",
    response_model=ChallengeResponse,
    status_code=status.HTTP_200_OK
)
def issue_challenge(
    req: ChallengeRequest,
    adapter       = Depends(get_adapter),
    challenge_mgr = Depends(get_challenge_mgr),
    crypto_utils  = Depends(get_crypto_utils),
):
    challenge = None
    with UnitOfWork(adapter) as uow:
        service = UserService(uow.users, challenge_mgr, crypto_utils)
        challenge = service.generate_challenge(req.username)
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return ChallengeResponse(challenge=challenge)

@router.post(
    "/auth/login",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK
)
def verify_response(
    req: AuthRequest,
    adapter       = Depends(get_adapter),
    challenge_mgr = Depends(get_challenge_mgr),
    crypto_utils  = Depends(get_crypto_utils),
):
    success: bool = False
    with UnitOfWork(adapter) as uow:
        service = UserService(uow.users, challenge_mgr, crypto_utils)
        success = service.authenticate(req.username, req.encrypted_challenge)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired challenge response"
        )
    return AuthResponse(success=True)
