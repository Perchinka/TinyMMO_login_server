import time
from redis import Redis
from login_server.domain.repositories import AbstractChallengeStorage
from login_server.common.exceptions import ChallengeNotFoundError


class RedisChallengeStorage(AbstractChallengeStorage):
    """
    Redis‐backed one‐time challenge store with TTL.
    """

    def __init__(self, client: Redis, ttl_seconds: int = 300):
        self.client = client
        self.ttl = ttl_seconds

    def store(self, username: str, challenge: str) -> None:
        """
        Store a challenge under the key 'challenge:<username>' with TTL.
        """
        self.client.setex(f"challenge:{username}", self.ttl, challenge)

    def retrieve(self, username: str) -> str:
        """
        Retrieve and return the challenge string.
        Raises ChallengeNotFoundError if no challenge is present.
        """
        val = self.client.get(f"challenge:{username}")
        if val is None:
            raise ChallengeNotFoundError(f"No challenge found for user '{username}'")
        return val


class LocalChallengeStorage(AbstractChallengeStorage):
    """
    In‐memory challenge store for testing or single‐instance use.
    Raises ChallengeNotFoundError on missing or expired entries.
    """

    def __init__(self, client=None, ttl_seconds: int = 300):
        # client is ignored; this is purely in‐memory
        self.storage: dict[str, tuple[str, float]] = {}
        self.ttl = ttl_seconds

    def store(self, username: str, challenge: str) -> None:
        """
        Store (challenge, timestamp).
        """
        self.storage[username] = (challenge, time.time())

    def retrieve(self, username: str) -> str:
        """
        Return the stored challenge if within TTL.
        Otherwise delete and raise ChallengeNotFoundError.
        """
        record = self.storage.get(username)
        if record is None:
            raise ChallengeNotFoundError(f"No challenge found for user '{username}'")

        challenge, created_at = record
        if time.time() - created_at > self.ttl:
            # expired: remove and signal not found
            del self.storage[username]
            raise ChallengeNotFoundError(f"Challenge for user '{username}' has expired")

        return challenge
