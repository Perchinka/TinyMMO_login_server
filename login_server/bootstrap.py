import logging
from typing import Any, Callable
from dataclasses import dataclass
from login_server.config import Config

from .domain.adapters import AbstractSQLAdapter, AbstractRedisAdapter

from .infra.adapters import PostgreSQLAdapter, RedisAdapter
from .infra.repositories import (
    RedisChallengeStorage,
    SQLUserRepository,
    LocalChallengeStorage,
)
from .infra import UnitOfWork


@dataclass
class Bootstraped:
    config: Config

    # Expose Factory, not actual object to get fresh uow each time it's called
    uow: Callable[..., UnitOfWork]


class Bootstrap:
    bootstraped: Bootstraped

    def __call__(self, *args: Any, **kwds: Any) -> Bootstraped:
        config = Config()

        logging.info("ATTEMPTING TO BOOTSTRAP - creating posgres adapter")
        sql_adapter: AbstractSQLAdapter = PostgreSQLAdapter(config.DATABASE_URL)

        logging.info("ATTEMPTING TO BOOTSTRAP - creating redis adapter")
        redis_adapter: AbstractRedisAdapter = RedisAdapter(config.REDIS_URL)

        if config.CHALLENGE_BACKEND.lower() == "redis":
            challenge_store = RedisChallengeStorage
        else:
            challenge_store = LocalChallengeStorage

        logging.info("ATTEMPTING TO BOOTSTRAP - wiring UoW")
        uow_factory = lambda: UnitOfWork(
            sql_adapter=sql_adapter,
            redis_adapter=redis_adapter,
            user_repo=SQLUserRepository,
            challenge_store=challenge_store,
        )

        Bootstrap.bootstraped = Bootstraped(config=config, uow=uow_factory)
        logging.info("Bootstrap is complete")

        return Bootstrap.bootstraped
