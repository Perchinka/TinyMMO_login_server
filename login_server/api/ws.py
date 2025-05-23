from fastapi import WebSocket, WebSocketDisconnect
from login_server.services.user_service import (
    GenerateChallengeService,
    AuthenticateUserService,
)
from login_server.common.exceptions import UserNotFoundError, AuthenticationError

generate_challenge = GenerateChallengeService()
auth_user = AuthenticateUserService()


async def login_ws(websocket: WebSocket):
    await websocket.accept()

    try:
        init = await websocket.receive_json()
        username = init.get("username")

        try:
            challenge = generate_challenge(username)
        except UserNotFoundError:
            await websocket.send_json({"type": "failure", "reason": "user not found"})
            return

        await websocket.send_json({"type": "challenge", **challenge})

        resp = await websocket.receive_json()
        if resp.get("type") != "response":
            await websocket.send_json(
                {"type": "failure", "reason": "invalid message type"}
            )
            return

        try:
            auth_user(
                username,
                resp["client_nonce"],
                resp["ciphertext"],
                resp["salt"],
            )
        except AuthenticationError:
            await websocket.send_json(
                {"type": "failure", "reason": "authentication failed"}
            )
            return

        await websocket.send_json({"type": "success"})

    except WebSocketDisconnect:
        return
    finally:
        await websocket.close()
