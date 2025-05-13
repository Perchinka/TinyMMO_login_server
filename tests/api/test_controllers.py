from fastapi import status
from login_server.api.controllers import RegisterUserService
from login_server.common.exceptions import UserAlreadyExistsError


def test_post_register_returns_201_for_new_username(test_app, test_client):
    """When the username is available, POST /register should return 201 and success=True."""

    class SuccessfulRegisterService:
        def __call__(self, username: str, password: str) -> None:
            # no exception => success
            return None

    test_app.dependency_overrides[RegisterUserService] = (
        lambda: SuccessfulRegisterService()
    )

    response = test_client.post(
        "/register", json={"username": "new_user", "password": "securePassword123"}
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"success": True}

    test_app.dependency_overrides.clear()


def test_post_register_returns_409_for_duplicate_username(test_app, test_client):
    """When the username is already taken, POST /register should return 409 and the proper error."""

    class DuplicateUsernameService:
        def __call__(self, username: str, password: str) -> None:
            raise UserAlreadyExistsError("Username already taken")

    test_app.dependency_overrides[RegisterUserService] = (
        lambda: DuplicateUsernameService()
    )

    response = test_client.post(
        "/register",
        json={"username": "existing_user", "password": "anotherPassword456"},
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Username already taken"

    test_app.dependency_overrides.clear()
