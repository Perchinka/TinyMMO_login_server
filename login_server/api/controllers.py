from fastapi import APIRouter, Depends, HTTPException, status
from login_server.api.schemas import (
    RegisterRequest,
    RegisterResponse,
    ChallengeRequest,
    ChallengeResponse,
    AuthRequest,
    AuthResponse,
)
from login_server.services.user_service import (
    RegisterUserService,
    GenerateChallengeService,
    AuthenticateUserService,
)

router = APIRouter(tags=["auth"])


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(req: RegisterRequest, service=Depends(RegisterUserService)):
    if not service(req.username, req.password):
        raise HTTPException(400, "Username already taken")
    return RegisterResponse(success=True)


@router.post("/auth/challenge", response_model=ChallengeResponse)
def issue_challenge(req: ChallengeRequest, service=Depends(GenerateChallengeService)):
    result = service(req.username)
    if result is None:
        raise HTTPException(404, "User not found")
    return ChallengeResponse(**result)


@router.post("/auth/login", response_model=AuthResponse)
def login(req: AuthRequest, service=Depends(AuthenticateUserService)):
    if not service(req.username, req.encrypted_challenge):
        raise HTTPException(401, "Invalid or expired challenge response")
    return AuthResponse(success=True)
