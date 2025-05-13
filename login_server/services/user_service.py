import os
from login_server.bootstrap import Bootstrap
from login_server.infra.security import PasswordHasher, ChallengeEncryptor
from login_server.common.exceptions import (
    AuthenticationError,
    ChallengeNotFoundError,
    UserAlreadyExistsError,
)


class RegisterUserService:
    def __init__(self):
        self._hasher = PasswordHasher()

    def __call__(self, username: str, password: str) -> None:
        with Bootstrap.bootstraped.uow() as uow:
            pw_hash = self._hasher.hash(password)
            if not uow.users.is_available(username):
                raise UserAlreadyExistsError
            uow.users.add(username, pw_hash)


class GenerateChallengeService:
    def __init__(self):
        self._hasher = PasswordHasher()
        self._encrypt = ChallengeEncryptor()

    def __call__(self, username: str) -> dict[str, str] | None:
        with Bootstrap.bootstraped.uow() as uow:
            pw_hash = uow.users.get_password_hash(username)
            if pw_hash is None:
                return None

            server_nonce = os.urandom(32).hex()
            salt = os.urandom(16)

            uow.challenges.store(username, server_nonce)
            return {
                "nonce": server_nonce,
                "salt": salt.hex(),
            }


class AuthenticateUserService:
    def __init__(self):
        self._encrypt = ChallengeEncryptor()

    def __call__(
        self,
        username: str,
        client_nonce_hex: str,
        ciphertext_hex: str,
        salt_hex: str,
    ) -> None:
        with Bootstrap.bootstraped.uow() as uow:
            pw_hash = uow.users.get_password_hash(username)
            if pw_hash is None:
                raise AuthenticationError("Invalid username or credentials")

            key = self._encrypt.derive_key(pw_hash, bytes.fromhex(salt_hex))
            client_nonce = bytes.fromhex(client_nonce_hex)
            ciphertext = bytes.fromhex(ciphertext_hex)

            try:
                decrypted = self._encrypt.decrypt(client_nonce, ciphertext, key)
            except Exception:
                raise AuthenticationError("Decryption failed or invalid credentials")

            try:
                original = uow.challenges.retrieve(username)
            except ChallengeNotFoundError:
                raise AuthenticationError("Challenge expired or not found")

            if decrypted != original:
                raise AuthenticationError("Response does not match challenge")

            return True
