import pytest
from fastapi.testclient import TestClient
from login_server.app import create_app


@pytest.fixture
def test_app():
    """Create and return a fresh FastAPI app instance."""
    return create_app()


@pytest.fixture
def test_client(test_app):
    """Wrap the FastAPI app in a TestClient."""
    return TestClient(test_app)
