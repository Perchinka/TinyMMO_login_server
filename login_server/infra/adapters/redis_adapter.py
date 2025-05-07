import redis
from typing import Any
from login_server.domain.adapters.redis_adapter import AbstractRedisAdapter


class RedisAdapter(AbstractRedisAdapter):
    def __init__(self, url):
        self.url = url

    def connect(self) -> Any:
        return redis.Redis.from_url(self.url, decode_responses=True)
