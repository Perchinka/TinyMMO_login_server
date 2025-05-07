import secrets
import logging
from login_server.bootstrap import Bootstrap
import hmac
import hashlib


class CryptoUtils:
    # Temporary solution
    """
    Provides static methods for password hashing and challenge encryption.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash `password` using SHA-256 and return the hex digest.
        """
        pw_bytes = password.encode("utf-8")
        digest = hashlib.sha256(pw_bytes).hexdigest()
        return digest

    @staticmethod
    def encrypt_challenge(challenge: str, key: str) -> str:
        """
        HMAC-SHA256 'encrypt' the `challenge` string using `key` (hex password hash).
        Returns the hex digest of the HMAC.
        """
        # key is hex string; convert to bytes
        key_bytes = bytes.fromhex(key)
        msg = challenge.encode("utf-8")
        mac = hmac.new(key_bytes, msg, digestmod=hashlib.sha256)
        return mac.hexdigest()

    @staticmethod
    def compare_encrypted(a: str, b: str) -> bool:
        """
        Constant-time comparison of two hex digests.
        """
        # compare_digest works on bytes or str
        return hmac.compare_digest(a, b)


class RegisterUserService:
    def __call__(self, username: str, password: str) -> bool:
        with Bootstrap.bootstraped.uow() as uow:
            if not uow.users.is_available(username):
                logging.warning(f"Registration failed: '{username}' taken.")
                return False
            passwd_hash = CryptoUtils.hash_password(password)
            uow.users.add(username, passwd_hash)
            logging.info(f"Registered '{username}'.")
            return True


class GenerateChallengeService:
    def __call__(self, username: str) -> str | None:
        with Bootstrap.bootstraped.uow() as uow:
            stored = uow.users.get_password_hash(username)
            if stored is None:
                logging.error(f"No such user '{username}' for challenge.")
                return None
            challenge = secrets.token_hex(32)
            uow.challenges.store(username, challenge)
            return challenge


class AuthenticateUserService:
    def __call__(self, username: str, client_response: str) -> bool:
        with Bootstrap.bootstraped.uow() as uow:
            stored = uow.users.get_password_hash(username)
            if stored is None:
                logging.error(f"Auth failed: user '{username}' not found.")
                return False
            original = uow.challenges.retrieve(username)
            expected = CryptoUtils.encrypt_challenge(original, stored)
            if not CryptoUtils.compare_encrypted(client_response, expected):
                logging.error(f"Auth failed: bad response for '{username}'.")
                return False
            logging.info(f"Authentication successful for '{username}'.")
            return True
