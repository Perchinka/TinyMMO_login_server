from fastapi import APIRouter, Depends, HTTPException, status
from login_server.api.schemas import (
    RegisterRequest,
    RegisterResponse,
)
from login_server.common.exceptions import UserAlreadyExistsError
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
    try:
        service(req.username, req.password)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    return RegisterResponse(success=True)
