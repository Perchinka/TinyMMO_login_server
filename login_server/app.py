from fastapi import FastAPI
from login_server.api.routes import include_routes


def create_app() -> FastAPI:
    from login_server.bootstrap import Bootstrap

    Bootstrap()()

    app = FastAPI(title="TinyMMO Login Server")
    include_routes(app)
    return app
