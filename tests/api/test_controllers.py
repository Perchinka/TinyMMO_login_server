from login_server.api.controllers import RegisterUserService


def test_post_register_returns_201_for_new_username(test_app, test_client):
    """When the username is available, POST /register should return 201 and success=True."""

    class SuccessfulRegisterService:
        def __call__(self, username: str, password: str) -> bool:
            return True

    test_app.dependency_overrides[RegisterUserService] = (
        lambda: SuccessfulRegisterService()
    )

    response = test_client.post(
        "/register", json={"username": "new_user", "password": "securePassword123"}
    )

    assert response.status_code == 201
    assert response.json() == {"success": True}

    test_app.dependency_overrides.clear()


def test_post_register_returns_400_for_duplicate_username(test_app, test_client):
    """When the username is already taken, POST /register should return 400 and the proper error."""

    class DuplicateUsernameService:
        def __call__(self, username: str, password: str) -> bool:
            return False

    test_app.dependency_overrides[RegisterUserService] = (
        lambda: DuplicateUsernameService()
    )

    response = test_client.post(
        "/register",
        json={"username": "existing_user", "password": "anotherPassword456"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already taken"

    test_app.dependency_overrides.clear()
