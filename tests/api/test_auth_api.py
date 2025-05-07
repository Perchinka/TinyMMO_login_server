import pytest
from fastapi.testclient import TestClient

from login_server.app import create_app
import login_server.api.controllers as controllers
from login_server.api.dependencies import get_adapter


# Helpers to create fake UserService classes
def make_fake_service(challenge_value=None, auth_value=None):
    class FakeUserService:
        def __init__(self, users, challenge_mgr, crypto_utils):
            pass

        def generate_challenge(self, username):
            return challenge_value

        def authenticate(self, username, encrypted_challenge):
            return auth_value

    return FakeUserService


@pytest.fixture
def client(adapter_mock):
    app = create_app()
    app.dependency_overrides[get_adapter] = lambda: adapter_mock
    return TestClient(app)


def test_issue_challenge_user_not_found(monkeypatch, client):
    FakeService = make_fake_service(challenge_value=None)
    monkeypatch.setattr(controllers, "UserService", FakeService)

    response = client.post("/auth/challenge", json={"username": "alice"})
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_issue_challenge_success(monkeypatch, client):
    FakeService = make_fake_service(challenge_value="abc123")
    monkeypatch.setattr(controllers, "UserService", FakeService)

    response = client.post("/auth/challenge", json={"username": "bob"})
    assert response.status_code == 200
    assert response.json() == {"challenge": "abc123"}


def test_verify_response_invalid(monkeypatch, client):
    FakeService = make_fake_service(auth_value=False)
    monkeypatch.setattr(controllers, "UserService", FakeService)

    payload = {"username": "carol", "encrypted_challenge": "wrong"}
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired challenge response"


def test_verify_response_success(monkeypatch, client):
    FakeService = make_fake_service(auth_value=True)
    monkeypatch.setattr(controllers, "UserService", FakeService)

    payload = {"username": "dave", "encrypted_challenge": "right"}
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 200
    assert response.json() == {"success": True}


def test_register_route_unmatched_endpoint(client):
    response = client.post("/register", json={"username": "x"})
    assert response.status_code == 404
