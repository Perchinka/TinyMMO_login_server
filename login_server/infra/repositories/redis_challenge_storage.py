from login_server.domain.repositories import AbstractChallengeStorage
from redis import Redis


class RedisChallengeStorage(AbstractChallengeStorage):
    def __init__(self, client: Redis, ttl_seconds: int = 300):
        self.client = client
        self.ttl = ttl_seconds

    def store(self, username: str, challenge: str) -> None:
        self.client.setex(f"challenge:{username}", self.ttl, challenge)

    def retrieve(self, username: str) -> str:
        return str(self.client.get(f"challenge:{username}")) or ""
