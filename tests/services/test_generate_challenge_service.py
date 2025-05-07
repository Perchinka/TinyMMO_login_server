import pytest
from unittest.mock import MagicMock
from login_server.services.user_service import GenerateChallengeService
from login_server.bootstrap import Bootstrap


@pytest.mark.usefixtures("dummy_bootstrap")
def test_generate_challenge_returns_none_for_unknown_user():
    """
    When the username has no associated password hash,
    GenerateChallengeService should return None.
    """
    generate_service = GenerateChallengeService()

    result = generate_service("nonexistent_user")

    assert result is None


@pytest.mark.usefixtures("dummy_bootstrap")
def test_generate_challenge_returns_nonce_and_salt_and_persists_it(monkeypatch):
    """
    For a user with a stored password hash, GenerateChallengeService
    should return a dict containing 'nonce' and 'salt', and store the nonce
    in the challenge storage under the correct username.
    """
    mock_uow = MagicMock()
    mock_uow.__enter__.return_value = mock_uow
    mock_uow.__exit__.return_value = None
    mock_uow.users.get_password_hash.return_value = "dummy_password_hash"
    mock_uow.challenges = MagicMock()

    monkeypatch.setattr(Bootstrap.bootstraped, "uow", lambda: mock_uow)

    generate_service = GenerateChallengeService()

    response = generate_service("existing_user")

    assert isinstance(response, dict), "Expected a dict with 'nonce' and 'salt'"
    assert "nonce" in response and isinstance(response["nonce"], str)
    assert "salt" in response and isinstance(response["salt"], str)

    mock_uow.challenges.store.assert_called_once_with(
        "existing_user", response["nonce"]
    )
