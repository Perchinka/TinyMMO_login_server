from login_server.domain.repositories import AbstractChallengeStorage
from redis import Redis
import time


class RedisChallengeStorage(AbstractChallengeStorage):
    def __init__(self, client: Redis, ttl_seconds: int = 300):
        self.client = client
        self.ttl = ttl_seconds

    def store(self, username: str, challenge: str) -> None:
        self.client.setex(f"challenge:{username}", self.ttl, challenge)

    def retrieve(self, username: str) -> str:
        return str(self.client.get(f"challenge:{username}")) or ""


class LocalChallengeStorage(AbstractChallengeStorage):
    """
    In-memory implementation of ChallengeStorage.
    Stores challenges in a simple dict.

    Note:
        TTL logic is minimal and checked on retrieval only.
    """

    def __init__(self, client=None, ttl_seconds: int = 300):
        self.storage = {}  # key: username, value: (challenge, timestamp)
        self.ttl = ttl_seconds

    def store(self, username: str, challenge: str) -> None:
        self.storage[username] = (challenge, time.time())

    def retrieve(self, username: str) -> str:
        record = self.storage.get(username)
        if not record:
            return ""

        challenge, created_at = record
        if time.time() - created_at > self.ttl:
            del self.storage[username]
            return ""
        return challenge
