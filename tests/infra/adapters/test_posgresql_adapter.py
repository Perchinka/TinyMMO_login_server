import pytest
from unittest.mock import MagicMock
import login_server.infra.adapters.postgresql_adapter as pg_mod
from login_server.infra.adapters.postgresql_adapter import PostgreSQLAdapter


def test_postgresql_adapter_connect_disables_autocommit(monkeypatch):
    """
    Given psycopg2.connect returns a connection with autocommit=True,
    PostgreSQLAdapter.connect() should return that connection with autocommit set to False.
    """
    # Stub psycopg2.connect to return our fake connection
    fake_connection = MagicMock()
    fake_connection.autocommit = True
    monkeypatch.setattr(pg_mod.psycopg2, "connect", lambda dsn: fake_connection)

    adapter = PostgreSQLAdapter(dsn="postgresql://user:pass@host/db")

    connection = adapter.connect()

    assert connection is fake_connection
    assert connection.autocommit is False
