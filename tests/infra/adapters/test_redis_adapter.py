from login_server.infra.adapters.redis_adapter import RedisAdapter
from redis import Redis


def test_redis_adapter_connect_returns_client():
    adapter = RedisAdapter("redis://localhost:6379/0")
    client = adapter.connect()
    assert isinstance(client, Redis)
