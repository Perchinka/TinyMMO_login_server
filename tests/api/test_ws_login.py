import login_server.api.ws as ws_module


def test_websocket_login_fails_when_user_not_found(monkeypatch, test_client):
    """
    If generate_challenge returns None (user not found),
    the WebSocket login flow should immediately send a failure.
    """
    monkeypatch.setattr(ws_module, "generate_challenge", lambda username: None)

    with test_client.websocket_connect("/auth/login") as ws:
        ws.send_json({"username": "ghost_user"})
        response = ws.receive_json()

    assert response["type"] == "failure"
    assert response["reason"] == "user not found"


def test_websocket_login_fails_on_invalid_message_type(monkeypatch, test_client):
    """
    After issuing a challenge, if the client sends a message
    with an unexpected 'type', the server should respond with a failure.
    """
    monkeypatch.setattr(
        ws_module,
        "generate_challenge",
        lambda username: {"nonce": "server_nonce", "salt": "abab"},
    )

    with test_client.websocket_connect("/auth/login") as ws:
        ws.send_json({"username": "valid_user"})
        challenge = ws.receive_json()
        assert challenge["type"] == "challenge"
        assert "nonce" in challenge and "salt" in challenge

        ws.send_json({"type": "unexpected_type"})
        response = ws.receive_json()

    assert response["type"] == "failure"
    assert response["reason"] == "invalid message type"


def test_websocket_login_succeeds_on_valid_response(monkeypatch, test_client):
    """
    If generate_challenge and auth_user both succeed,
    the WebSocket login should conclude with a success message.
    """
    monkeypatch.setattr(
        ws_module,
        "generate_challenge",
        lambda username: {"nonce": "srv_nonce", "salt": "deadbeef"},
    )
    monkeypatch.setattr(ws_module, "auth_user", lambda u, n, c, s: True)

    with test_client.websocket_connect("/auth/login") as ws:
        ws.send_json({"username": "alice"})
        challenge = ws.receive_json()
        assert challenge["type"] == "challenge"

        ws.send_json(
            {
                "type": "response",
                "client_nonce": "client_nonce_value",
                "ciphertext": "encrypted_payload",
                "salt": challenge["salt"],
            }
        )
        response = ws.receive_json()

    assert response["type"] == "success"
