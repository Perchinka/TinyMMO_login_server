import pytest
from fastapi.testclient import TestClient

from login_server.app import create_app
import login_server.api.ws as ws_module


@pytest.fixture
def client():
    return TestClient(create_app())


def test_ws_login_user_not_found(monkeypatch, client):
    monkeypatch.setattr(ws_module, "generate_challenge", lambda username: None)

    with client.websocket_connect("/auth/login") as ws:
        ws.send_json({"username": "unknown"})
        resp = ws.receive_json()
        assert resp["type"] == "failure"
        assert resp["reason"] == "user not found"


def test_ws_login_invalid_message_type(monkeypatch, client):
    monkeypatch.setattr(ws_module, "generate_challenge", lambda username: "abc123")

    with client.websocket_connect("/auth/login") as ws:
        ws.send_json({"username": "alice"})
        chal = ws.receive_json()
        assert chal["type"] == "challenge"
        assert chal["challenge"] == "abc123"

        ws.send_json({"type": "foo"})
        resp = ws.receive_json()
        assert resp["type"] == "failure"
        assert resp["reason"] == "invalid message type"


def test_ws_login_success(monkeypatch, client):
    monkeypatch.setattr(ws_module, "generate_challenge", lambda username: "xyz789")
    monkeypatch.setattr(ws_module, "auth_user", lambda u, n, c, s: True)

    with client.websocket_connect("/auth/login") as ws:
        ws.send_json({"username": "alice"})
        result = ws.receive_json()
        assert result["type"] == "challenge"
        assert result["challenge"] == "xyz789"

        ws.send_json(
            {
                "type": "response",
                "client_nonce": "ignored",
                "ciphertext": "ignored",
                "salt": "ignored",
            }
        )
        resp = ws.receive_json()
        assert resp["type"] == "success"
