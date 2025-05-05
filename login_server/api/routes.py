from fastapi import FastAPI
from .controllers import router as auth_router

def include_routes(app: FastAPI) -> None:
    app.include_router(auth_router, prefix="", tags=["auth"])
