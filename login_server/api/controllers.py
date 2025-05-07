from fastapi import APIRouter, Depends, HTTPException, status
from login_server.api.schemas import (
    RegisterRequest,
    RegisterResponse,
)
from login_server.services.user_service import (
    RegisterUserService,
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
