import pytest
from login_server.infra.unit_of_work import UnitOfWork

def test_uow_exposes_users_and_conn():
    with UnitOfWork("dsn") as uow:
        assert hasattr(uow, "users")
        assert hasattr(uow, "conn")

def test_uow_executes_create_table_ddl():
    with UnitOfWork("dsn") as uow:
        cmds = uow.conn.cursor().commands # type: ignore
        assert any("CREATE TABLE IF NOT EXISTS users" in cmd for cmd, _ in cmds)

def test_uow_commits_and_closes_on_success():
    uow = UnitOfWork("dsn")
    with uow:
        pass
    conn = uow.conn
    assert conn.committed is True # type: ignore
    assert conn.closed is True

def test_uow_rolls_back_and_closes_on_error():
    uow = UnitOfWork("dsn")
    with pytest.raises(RuntimeError):
        with uow:
            raise RuntimeError("oops")
    conn = uow.conn
    assert conn.rolled_back is True # type: ignore
    assert conn.closed is True
