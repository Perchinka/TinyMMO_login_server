import pytest
from unittest.mock import MagicMock
from login_server.services.user_service import RegisterUserService
from login_server.bootstrap import Bootstrap


@pytest.fixture
def mock_uow_for_register(monkeypatch):
    """
    Fixture that stubs out Bootstrap.bootstraped.uow() to return a UnitOfWork
    where users.is_available returns True and users.add is a mock.
    """
    mock_uow = MagicMock()
    mock_uow.__enter__.return_value = mock_uow
    mock_uow.__exit__.return_value = None

    mock_uow.users.is_available.return_value = True
    mock_uow.users.add = MagicMock()

    mock_uow.challenges = MagicMock()

    monkeypatch.setattr(Bootstrap.bootstraped, "uow", lambda: mock_uow)
    return mock_uow


@pytest.fixture
def mock_uow_for_duplicate(monkeypatch):
    """
    Fixture that stubs out Bootstrap.bootstraped.uow() to return a UnitOfWork
    where users.is_available returns False (duplicate) and users.add is a mock.
    """
    mock_uow = MagicMock()
    mock_uow.__enter__.return_value = mock_uow
    mock_uow.__exit__.return_value = None

    mock_uow.users.is_available.return_value = False
    mock_uow.users.add = MagicMock()
    mock_uow.challenges = MagicMock()

    monkeypatch.setattr(Bootstrap.bootstraped, "uow", lambda: mock_uow)
    return mock_uow


def test_register_user_service_adds_user_and_returns_true(mock_uow_for_register):
    """
    When username is available, RegisterUserService should:
     - return True
     - call users.add(username, password_hash) exactly once
    """
    service = RegisterUserService()
    result = service("alice", "PlainText123")

    assert result is True

    mock_uow_for_register.users.add.assert_called_once()
    called_username, called_hash = mock_uow_for_register.users.add.call_args[0]
    assert called_username == "alice"
    assert isinstance(called_hash, str)

    assert called_hash.startswith("$argon2")


def test_register_user_service_returns_false_and_never_adds_for_duplicate(
    mock_uow_for_duplicate,
):
    """
    When username is already taken, RegisterUserService should
    return False and never call users.add()
    """
    service = RegisterUserService()
    result = service("bob", "AnyPassword")

    assert result is False
    mock_uow_for_duplicate.users.add.assert_not_called()
