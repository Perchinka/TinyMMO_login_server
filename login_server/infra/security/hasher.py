from argon2 import PasswordHasher as _Argon2Hasher
from argon2.exceptions import VerifyMismatchError


class PasswordHasher:
    """
    Wraps argon2-cffi’s PasswordHasher with sensible defaults.
    """

    def __init__(self) -> None:
        self._hasher = _Argon2Hasher(
            time_cost=3,
            memory_cost=64 * 1024,
            parallelism=4,
        )

    def hash(self, password: str) -> str:
        """
        Hash a plaintext password, returning the full Argon2 hash string
        (which encodes salt & parameters).
        """
        return self._hasher.hash(password)

    def verify(self, password: str, stored_hash: str) -> bool:
        """
        Verify `password` against the stored Argon2 hash.
        """
        try:
            return self._hasher.verify(stored_hash, password)
        except VerifyMismatchError:
            return False
