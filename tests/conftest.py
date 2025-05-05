import pytest
import psycopg2

from login_server.crypto.challenge import ChallengeManager
from login_server.crypto.crypto_utils import CryptoUtils
from login_server.domain.repositories.user_repository import UserRepository
from login_server.infra.repositories.user_sql_repository import UserSQLRepository
from login_server.services.user_service import UserService

# --- Fake DB and Connection Fixtures ---

class FakeCursor:
    def __init__(self):
        self.commands = []
        self._fetch = None

    def execute(self, sql, params=None):
        self.commands.append((sql.strip(), params))

    def fetchone(self):
        return self._fetch

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class FakeConnection:
    def __init__(self):
        self.cursor_obj = FakeCursor()
        self.committed = False
        self.rolled_back = False
        self.closed = False

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True

    def close(self):
        self.closed = True

@pytest.fixture(autouse=True)
def patch_psycopg2_connect(monkeypatch):
    """Globally patch psycopg2.connect to return a FakeConnection."""
    monkeypatch.setattr(psycopg2, "connect", lambda dsn: FakeConnection())
    yield

@pytest.fixture
def fake_conn():
    """Provide a fresh FakeConnection."""
    return FakeConnection()

@pytest.fixture
def user_sql_repo(fake_conn):
    """Provide a UserSQLRepository bound to a fake connection."""
    return UserSQLRepository(fake_conn)

# --- Service Layer Fixture ---

class DummyRepo(UserRepository):
    def __init__(self):
        self._store: dict[str, str] = {}

    def is_available(self, username: str) -> bool:
        return username not in self._store

    def add(self, username: str, password_hash: str) -> None:
        self._store[username] = password_hash

    def get_password_hash(self, username: str) -> str | None:
        return self._store.get(username)

@pytest.fixture
def user_service():
    """Provide a UserService with an in-memory DummyRepo."""
    repo = DummyRepo()
    challenge_manager = ChallengeManager()
    crypto_utils = CryptoUtils()
    return UserService(repo, challenge_manager, crypto_utils)
