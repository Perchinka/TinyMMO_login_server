import pytest
from fastapi.testclient import TestClient
import login_server.api.ws as ws_module
from login_server.app import create_app


@pytest.fixture
def client():
    return TestClient(create_app())


def test_ws_login_user_not_found(monkeypatch, client):
    # Simulate no user found by returning None
    monkeypatch.setattr(ws_module, "generate_challenge", lambda username: None)

    with client.websocket_connect("/auth/login") as ws:
        ws.send_json({"username": "ghost"})
        resp = ws.receive_json()
        assert resp["type"] == "failure"
        assert resp["reason"] == "user not found"


def test_ws_login_invalid_message_type(monkeypatch, client):
    # Fake challenge returned
    monkeypatch.setattr(
        ws_module,
        "generate_challenge",
        lambda username: {"nonce": "abc", "salt": "123"},
    )

    with client.websocket_connect("/auth/login") as ws:
        ws.send_json({"username": "mocked_user"})
        chal = ws.receive_json()
        assert chal["type"] == "challenge"
        assert chal["nonce"] == "abc"

        ws.send_json({"type": "unknown"})
        resp = ws.receive_json()
        assert resp["type"] == "failure"
        assert resp["reason"] == "invalid message type"


def test_ws_login_success(monkeypatch, client):
    # Provide mocked challenge
    monkeypatch.setattr(
        ws_module,
        "generate_challenge",
        lambda username: {"nonce": "server-nonce", "salt": "deadbeef"},
    )

    # Provide mocked authentication result
    monkeypatch.setattr(ws_module, "auth_user", lambda u, n, c, s: True)

    with client.websocket_connect("/auth/login") as ws:
        ws.send_json({"username": "test_user"})
        chal = ws.receive_json()
        assert chal["type"] == "challenge"
        assert chal["nonce"] == "server-nonce"
        assert chal["salt"] == "deadbeef"

        ws.send_json(
            {
                "type": "response",
                "client_nonce": "whatever",
                "ciphertext": "whatever",
                "salt": "deadbeef",
            }
        )
        resp = ws.receive_json()
        assert resp["type"] == "success"
