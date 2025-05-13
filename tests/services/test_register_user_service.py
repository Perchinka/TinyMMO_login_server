import pytest
from unittest.mock import MagicMock
from login_server.services.user_service import RegisterUserService
from login_server.bootstrap import Bootstrap
from login_server.common.exceptions import UserAlreadyExistsError


@pytest.fixture
def mock_uow_for_register(monkeypatch):
    mock_uow = MagicMock()
    mock_uow.__enter__.return_value = mock_uow
    mock_uow.__exit__.return_value = None

    mock_uow.users.is_available.return_value = True
    mock_uow.users.add = MagicMock()

    monkeypatch.setattr(Bootstrap, "bootstraped", MagicMock(uow=lambda: mock_uow))
    return mock_uow


@pytest.fixture
def mock_uow_for_duplicate(monkeypatch):
    mock_uow = MagicMock()
    mock_uow.__enter__.return_value = mock_uow
    mock_uow.__exit__.return_value = None

    mock_uow.users.is_available.return_value = False
    mock_uow.users.add = MagicMock()

    monkeypatch.setattr(Bootstrap, "bootstraped", MagicMock(uow=lambda: mock_uow))
    return mock_uow


def test_register_user_service_adds_user_and_does_not_raise(mock_uow_for_register):
    """
    When username is available, RegisterUserService should call add() and not raise.
    """
    service = RegisterUserService()
    # Should not raise
    service("alice", "PlainText123")

    mock_uow_for_register.users.add.assert_called_once_with(
        "alice", mock_uow_for_register.users.add.call_args[0][1]
    )


def test_register_user_service_raises_for_duplicate_and_never_adds(
    mock_uow_for_duplicate,
):
    """
    When username is already taken, RegisterUserService should raise
    UserAlreadyExistsError and never call add().
    """
    service = RegisterUserService()
    with pytest.raises(UserAlreadyExistsError):
        service("bob", "AnyPassword")

    mock_uow_for_duplicate.users.add.assert_not_called()
