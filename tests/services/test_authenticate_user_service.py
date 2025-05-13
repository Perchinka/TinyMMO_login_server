import os
import pytest
from unittest.mock import MagicMock
from login_server.services.user_service import AuthenticateUserService
from login_server.bootstrap import Bootstrap
from login_server.common.exceptions import AuthenticationError
from login_server.infra.security.challenge_encryptor import ChallengeEncryptor


@pytest.mark.usefixtures("dummy_bootstrap")
def test_authenticate_succeeds_for_matching_challenge(monkeypatch):
    """
    When the decrypted text matches the stored challenge,
    AuthenticateUserService should not raise.
    """
    stored_challenge = "expected_nonce"
    stored_hash = "argon2_hash_string"
    salt = os.urandom(16)
    key = ChallengeEncryptor().derive_key(stored_hash, salt)
    nonce, ciphertext = ChallengeEncryptor().encrypt(stored_challenge, key)

    mock_uow = MagicMock()
    mock_uow.__enter__.return_value = mock_uow
    mock_uow.__exit__.return_value = None
    mock_uow.users.get_password_hash.return_value = stored_hash
    mock_uow.challenges.retrieve.return_value = stored_challenge

    monkeypatch.setattr(Bootstrap.bootstraped, "uow", lambda: mock_uow)

    service = AuthenticateUserService()
    service(
        username="alice",
        client_nonce_hex=nonce.hex(),
        ciphertext_hex=ciphertext.hex(),
        salt_hex=salt.hex(),
    )


@pytest.mark.usefixtures("dummy_bootstrap")
def test_authenticate_raises_for_non_matching_or_invalid_cipher(monkeypatch):
    """
    If decryption fails or the decrypted text does not match,
    AuthenticateUserService should raise AuthenticationError.
    """
    stored_hash = "argon2_hash_string"
    salt = os.urandom(16)

    mock_uow = MagicMock()
    mock_uow.__enter__.return_value = mock_uow
    mock_uow.__exit__.return_value = None
    mock_uow.users.get_password_hash.return_value = stored_hash
    mock_uow.challenges.retrieve.return_value = "original_nonce"

    monkeypatch.setattr(Bootstrap.bootstraped, "uow", lambda: mock_uow)

    service = AuthenticateUserService()
    with pytest.raises(AuthenticationError):
        service(
            username="bob",
            client_nonce_hex="00" * 12,
            ciphertext_hex="ff" * 16,
            salt_hex=salt.hex(),
        )
