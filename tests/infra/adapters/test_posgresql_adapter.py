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


def test_postgresql_adapter_ensure_schema_executes_create_users_table():
    """
    ensure_schema() should open a cursor and execute the DDL
    to create the 'users' table if it does not already exist.
    """
    # Set up a mock connection whose cursor() returns a context manager
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

    adapter = PostgreSQLAdapter(dsn="postgresql://user:pass@host/db")

    adapter.ensure_schema(mock_connection)

    mock_cursor.execute.assert_called_once()
    executed_sql = mock_cursor.execute.call_args[0][0]
    assert "CREATE TABLE IF NOT EXISTS users" in executed_sql
