import pytest
from unittest.mock import MagicMock
from login_server.bootstrap import Bootstrap
from login_server.domain.adapters import AbstractSQLAdapter
from login_server.infra.repositories.user_sql_repository import SQLUserRepository


# --- SQL adapter / connection fixtures ---
@pytest.fixture
def connection_mock():
    conn = MagicMock()
    cursor = MagicMock()
    cursor.__enter__.return_value = cursor
    cursor.__exit__.return_value = None
    conn.cursor.return_value = cursor
    conn.commit = MagicMock()
    conn.rollback = MagicMock()
    conn.close = MagicMock()
    return conn


@pytest.fixture
def adapter_mock(connection_mock):
    adapter = MagicMock(spec=AbstractSQLAdapter)
    adapter.connect.return_value = connection_mock
    adapter.ensure_schema = MagicMock()
    return adapter


@pytest.fixture
def user_sql_repo(connection_mock):
    return SQLUserRepository(connection_mock)


# --- DummyUOW for services tests ---
class DummyUOW:
    def __init__(self):
        self.users = MagicMock()
        self.challenges = MagicMock()

        # default behaviors
        self.users.is_available.return_value = True
        self.users.get_password_hash.return_value = None

        self.users.add = MagicMock()
        self.challenges.store = MagicMock()
        self.challenges.retrieve.return_value = ""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


@pytest.fixture
def dummy_bootstrap(monkeypatch):
    """
    Patch Bootstrap.bootstraped.uow so that all services get a DummyUOW.
    Tests that need a real DB/Redis can ignore this fixture; services tests should
    import and use @pytest.mark.usefixtures("dummy_bootstrap").
    """
    monkeypatch.setattr(Bootstrap, "bootstraped", MagicMock(uow=lambda: DummyUOW()))
