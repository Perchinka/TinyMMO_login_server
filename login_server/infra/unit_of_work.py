from contextlib import AbstractContextManager
from typing import Type

from login_server.domain.adapters import (
    AbstractSQLAdapter,
    AbstractRedisAdapter,
)

from login_server.domain.repositories import (
    AbstractUserRepository,
    AbstractChallengeStorage,
)
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
        self,
        sql_adapter: AbstractSQLAdapter,
        redis_adapter: AbstractRedisAdapter,
        user_repo: Type[AbstractUserRepository],
        challenge_store: Type[AbstractChallengeStorage],
    ):
        self.sql_adapter = sql_adapter
        self.redis_adapter = redis_adapter
        self.user_repo = user_repo
        self.challenge_store = challenge_store

    def __enter__(self) -> "UnitOfWork":
        # SQL
        self.conn = self.sql_adapter.connect()
        self.sql_adapter.ensure_schema(self.conn)
        self.users = self.user_repo(self.conn)

        # Redis
        self.redis_client = self.redis_adapter.connect()
        self.challenge_store = self.challenge_store(self.redis_client)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()
