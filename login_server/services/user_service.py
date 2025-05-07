import os
from login_server.bootstrap import Bootstrap
from login_server.infra.security import PasswordHasher
from login_server.infra.security import ChallengeEncryptor


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
        self._encryptor = ChallengeEncryptor()

    def __call__(self, username: str) -> dict | None:
        with Bootstrap.bootstraped.uow() as uow:
            pw_hash = uow.users.get_password_hash(username)
            if pw_hash is None:
                return None

            # generate server nonce and salt
            server_nonce = os.urandom(32).hex()
            salt = os.urandom(16)
            key = self._encryptor.derive_key(pw_hash, salt)

            # store plaintext nonce (so we can verify client later)
            uow.challenges.store(username, server_nonce)

            return {
                "nonce": server_nonce,
                "salt": salt.hex(),
            }


class AuthenticateUserService:
    def __init__(self):
        self._encryptor = ChallengeEncryptor()

    def __call__(
        self,
        username: str,
        client_nonce_hex: str,
        client_cipher_hex: str,
        salt_hex: str,
    ) -> bool:
        with Bootstrap.bootstraped.uow() as uow:
            pw_hash = uow.users.get_password_hash(username)
            if pw_hash is None:
                return False

            # reconstruct key
            salt = bytes.fromhex(salt_hex)
            key = self._encryptor.derive_key(pw_hash, salt)

            # decrypt client’s response to see if they saw our server_nonce
            client_nonce = bytes.fromhex(client_nonce_hex)
            client_cipher = bytes.fromhex(client_cipher_hex)
            try:
                server_nonce = self._encryptor.decrypt(client_nonce, client_cipher, key)
            except Exception:
                return False

            stored = uow.challenges.retrieve(username)
            if server_nonce != stored:
                return False

            # (Optionally: now encrypt the client's own challenge back)
            return True
