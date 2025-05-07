import os
from login_server.bootstrap import Bootstrap
from login_server.infra.security import PasswordHasher, ChallengeEncryptor
from login_server.common.exceptions import ChallengeNotFoundError


class RegisterUserService:
    def __init__(self):
        self._hasher = PasswordHasher()

    def __call__(self, username: str, password: str) -> bool:
        with Bootstrap.bootstraped.uow() as uow:
            if not uow.users.is_available(username):
                return False
            pw_hash = self._hasher.hash(password)
            uow.users.add(username, pw_hash)
            return True


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
            key = self._encrypt.derive_key(pw_hash, salt)

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
    ) -> bool:
        with Bootstrap.bootstraped.uow() as uow:
            pw_hash = uow.users.get_password_hash(username)
            if pw_hash is None:
                return False

            key = self._encrypt.derive_key(pw_hash, bytes.fromhex(salt_hex))
            client_nonce = bytes.fromhex(client_nonce_hex)
            ciphertext = bytes.fromhex(ciphertext_hex)

            try:
                decrypted = self._encrypt.decrypt(client_nonce, ciphertext, key)
            except Exception:
                return False

            try:
                original = uow.challenges.retrieve(username)
            except ChallengeNotFoundError:
                return False

            return decrypted == original
