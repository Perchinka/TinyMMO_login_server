import pytest
from login_server.infra.unit_of_work import UnitOfWork
from login_server.infra.repositories.user_sql_repository import UserSQLRepository

def test_uow_exposes_users_and_conn(adapter_mock):
    with UnitOfWork(adapter_mock) as uow:
        # .conn comes from adapter.connect()
        assert uow.conn is adapter_mock.connect.return_value
        # .users is bound to that same connection
        assert isinstance(uow.users, UserSQLRepository)
        # adapter.connect() and ensure_schema() were called
        adapter_mock.connect.assert_called_once()
        adapter_mock.ensure_schema.assert_called_once_with(uow.conn)

def test_uow_commits_and_closes_on_success(adapter_mock):
    uow = UnitOfWork(adapter_mock)
    with uow:
        pass
    # After a successful block, commit then close
    conn = uow.conn
    conn.commit.assert_called_once()
    conn.close.assert_called_once()

def test_uow_rolls_back_and_closes_on_error(adapter_mock):
    uow = UnitOfWork(adapter_mock)
    with pytest.raises(RuntimeError):
        with uow:
            raise RuntimeError("boom")
    # On exception, rollback then close
    conn = uow.conn
    conn.rollback.assert_called_once()
    conn.close.assert_called_once()

def test_ensure_schema_called_before_repo_binding(adapter_mock):
    # Even if repo not used, ensure_schema should still be invoked
    with UnitOfWork(adapter_mock):
        pass
    adapter_mock.ensure_schema.assert_called_once_with(adapter_mock.connect.return_value)
