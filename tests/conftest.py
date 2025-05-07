import pytest
from unittest.mock import MagicMock
from login_server.domain.adapters import AbstractSQLAdapter
from login_server.infra.repositories import SQLUserRepository
from login_server.domain.repositories import UserRepository


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


class DummyRepo(UserRepository):
    def __init__(self):
        self._store = {}

    def is_available(self, username: str) -> bool:
        return username not in self._store

    def add(self, username: str, password_hash: str) -> None:
        self._store[username] = password_hash

    def get_password_hash(self, username: str) -> str | None:
        return self._store.get(username)
