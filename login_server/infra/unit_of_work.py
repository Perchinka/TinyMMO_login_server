from contextlib import AbstractContextManager
from typing import Any

from login_server.domain.repositories import UserRepository
from .repositories.user_sql_repository import UserSQLRepository

from login_server.domain.adapters import SQLAdapter

class UnitOfWork(AbstractContextManager["UnitOfWork"]):
    """
    Manages a SQLAdapter‐provided connection in a transaction,
    exposes `.users` as a UserRepository.
    """

    conn: Any
    users: UserRepository

    def __init__(self, adapter: SQLAdapter):
        self.adapter = adapter

    def __enter__(self) -> "UnitOfWork":
        self.conn = self.adapter.connect()
        self.adapter.ensure_schema(self.conn)

        self.users = UserSQLRepository(self.conn)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        # commit or rollback, then close
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

        # returning False re-raises any exception
        return False
