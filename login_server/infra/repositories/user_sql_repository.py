from typing import Optional

from psycopg2 import IntegrityError
from psycopg2.extensions import connection as _Connection

from login_server.common.exceptions import UserAlreadyExistsError
from login_server.domain.repositories import AbstractUserRepository


class SQLUserRepository(AbstractUserRepository):
    """
    psycopg2 implementation of UserRepository.
    """

    def __init__(self, conn: _Connection):
        self.conn = conn

    def is_available(self, username: str) -> bool:
        with self.conn.cursor() as cur:
            cur.execute("SELECT 1 FROM users WHERE username = %s;", (username,))
            return cur.fetchone() is None

    def add(self, username: str, password_hash: str) -> None:
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    "INSERT INTO users (username, password_hash) VALUES (%s, %s);",
                    (username, password_hash),
                )
            except IntegrityError as e:
                raise UserAlreadyExistsError(
                    f"Username '{username}' is already taken"
                ) from e

    def get_password_hash(self, username: str) -> Optional[str]:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT password_hash FROM users WHERE username = %s;", (username,)
            )
            row = cur.fetchone()
            return row[0] if row else None
