import psycopg2
from contextlib import AbstractContextManager

from login_server.domain.repositories import UserRepository
from .repositories.user_sql_repository import UserSQLRepository

class UnitOfWork(AbstractContextManager["UnitOfWork"]):
    """
    Manages a psycopg2 transaction and exposes a `users` repository bound to it.

    Usage:
        with UnitOfWork(db_url) as uow:
            svc = UserService(uow.users, ...)
    """
    conn: psycopg2.extensions.connection
    users: UserRepository

    def __init__(self, db_url: str):
        self.db_url = db_url

    def __enter__(self) -> "UnitOfWork":
        self.conn = psycopg2.connect(self.db_url)
        self.conn.autocommit = False

        # Ensure table exists
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username VARCHAR PRIMARY KEY,
                    password_hash VARCHAR NOT NULL
                );
            """)

        # Bind repository implementation
        self.users = UserSQLRepository(self.conn)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

        # Returning False propagates exceptions, True silences them
        return False
