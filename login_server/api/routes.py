from fastapi import FastAPI
from .controllers import router as auth_router
from .ws import login_ws


def include_routes(app: FastAPI) -> None:
    app.include_router(auth_router, prefix="", tags=["auth"])
    app.websocket_route("/auth/login")(login_ws)
