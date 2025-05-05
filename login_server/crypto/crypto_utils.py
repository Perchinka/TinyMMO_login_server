import hashlib
import hmac
from typing import Union


class CryptoUtils:
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
