import pytest
from unittest.mock import MagicMock
from login_server.services.user_service import GenerateChallengeService
from login_server.bootstrap import Bootstrap


@pytest.mark.usefixtures("dummy_bootstrap")
def test_generate_challenge_unknown_user():
    gen = GenerateChallengeService()
    assert gen("noone") is None


@pytest.mark.usefixtures("dummy_bootstrap")
def test_generate_challenge_for_existing_user(monkeypatch):
    # Prepare a fake UoW instance
    fake_uow = MagicMock()
    fake_uow.__enter__.return_value = fake_uow
    fake_uow.__exit__.return_value = None

    # Return a dummy password hash so GenerateChallengeService proceeds
    fake_uow.users.get_password_hash.return_value = "fakepw"
    fake_uow.challenges = MagicMock()

    # Patch bootstrap to use our fake_uow
    monkeypatch.setattr(Bootstrap.bootstraped, "uow", lambda: fake_uow)

    gen = GenerateChallengeService()
    out = gen("alice")

    assert isinstance(out, dict)
    assert "nonce" in out and "salt" in out
    fake_uow.challenges.store.assert_called_once_with("alice", out["nonce"])
