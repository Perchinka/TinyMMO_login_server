from contextlib import AbstractContextManager

from login_server.domain.adapters import (
    AbstractSQLAdapter,
    AbstractRedisAdapter,
)

from login_server.domain.repositories import UserRepository, ChallengeStorage
from .repositories import SQLUserRepository, RedisChallengeStorage


class UnitOfWork(AbstractContextManager["UnitOfWork"]):
    """
    A unit of work that manages:
      - an SQL transaction for users
      - a Redis-backed challenge store

    Exposes:
      - .users          -> UserRepository
      - .challenge_store -> ChallengeStorage
    """

    def __init__(
        self, sql_adapter: AbstractSQLAdapter, redis_adapter: AbstractRedisAdapter
    ):
        self.sql_adapter = sql_adapter
        self.redis_adapter = redis_adapter

    def __enter__(self) -> "UnitOfWork":
        self.conn = self.sql_adapter.connect()
        self.sql_adapter.ensure_schema(self.conn)
        self.users = SQLUserRepository(self.conn)

        self.redis_client = self.redis_adapter.connect()
        self.challenge_store = RedisChallengeStorage(self.redis_client)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()
