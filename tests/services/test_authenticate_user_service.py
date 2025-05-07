import os
import pytest
from unittest.mock import MagicMock
from login_server.services.user_service import AuthenticateUserService
from login_server.bootstrap import Bootstrap
from login_server.infra.security.challenge_encryptor import ChallengeEncryptor


@pytest.mark.usefixtures("dummy_bootstrap")
def test_authenticate_user_success(monkeypatch):
    # Set up a “realistic” challenge/response
    original = "srv_nonce"
    fake_hash = "dummyhash"
    salt = os.urandom(16)
    key = ChallengeEncryptor().derive_key(fake_hash, salt)
    nonce, ct = ChallengeEncryptor().encrypt(original, key)

    fake_uow = MagicMock()
    fake_uow.__enter__.return_value = fake_uow
    fake_uow.__exit__.return_value = None

    fake_uow.users.get_password_hash.return_value = fake_hash
    fake_uow.challenges.retrieve.return_value = original

    monkeypatch.setattr(Bootstrap.bootstraped, "uow", lambda: fake_uow)

    svc = AuthenticateUserService()
    ok = svc("alice", nonce.hex(), ct.hex(), salt.hex())
    assert ok is True


@pytest.mark.usefixtures("dummy_bootstrap")
def test_authenticate_user_failure_wrong_cipher(monkeypatch):
    fake_hash = "dummyhash"
    salt = os.urandom(16)

    fake_uow = MagicMock()
    fake_uow.__enter__.return_value = fake_uow
    fake_uow.__exit__.return_value = None

    fake_uow.users.get_password_hash.return_value = fake_hash
    fake_uow.challenges.retrieve.return_value = "orig"

    monkeypatch.setattr(Bootstrap.bootstraped, "uow", lambda: fake_uow)

    svc = AuthenticateUserService()
    # Pass nonsense so decryption fails or mismatch
    result = svc("alice", "00" * 12, "ff" * 16, salt.hex())
    assert result is False
