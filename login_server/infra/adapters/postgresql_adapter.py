import psycopg2
from typing import Any
from login_server.domain.adapters import AbstractSQLAdapter


class PostgreSQLAdapter(AbstractSQLAdapter):
    """
    SQLAdapter for PostgreSQL.
    """

    def __init__(self, dsn: str):
        self.dsn = dsn

    def connect(self) -> Any:
        conn = psycopg2.connect(self.dsn)
        conn.autocommit = False
        return conn
