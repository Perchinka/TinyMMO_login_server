"""
auth/crypto_utils.py

Hashing and challenge‐encryption utilities.
"""

class CryptoUtils:
    """
    Provides static methods for password hashing and challenge encryption.
    """
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash `password` using SHA-256 and return hex digest.
        """
        return ""

    @staticmethod
    def encrypt_challenge(challenge: str, key: str) -> str:
        """
        HMAC-SHA256 encrypt `challenge` with `key`.
        """
        return ""

    @staticmethod
    def compare_encrypted(a: str, b: str) -> bool:
        """
        Comparison of two hashes.
        """
        return a==b 

