import pytest
from login_server.infra.unit_of_work import UnitOfWork


def test_uow_exposes_users_and_challenges(adapter_mock):
    # adapter_mock is used for both SQL and Redis here
    uow = UnitOfWork(
        sql_adapter=adapter_mock,
        redis_adapter=adapter_mock,
        user_repo=lambda conn: "USERS",
        challenge_store=lambda client: "CHALLENGES",
    )

    with uow as w:
        # .connect() should have been called twice: once for SQL, once for Redis
        assert adapter_mock.connect.call_count == 2
        adapter_mock.ensure_schema.assert_called_once_with(w.conn)

        assert w.conn is adapter_mock.connect.return_value
        assert w.users == "USERS"
        assert w.challenges == "CHALLENGES"


def test_uow_commit_and_close(adapter_mock):
    uow = UnitOfWork(
        sql_adapter=adapter_mock,
        redis_adapter=adapter_mock,
        user_repo=lambda c: None,
        challenge_store=lambda c: None,
    )
    with uow:
        pass
    conn = uow.conn
    conn.commit.assert_called_once()
    conn.close.assert_called_once()


def test_uow_rollback_on_error(adapter_mock):
    uow = UnitOfWork(
        sql_adapter=adapter_mock,
        redis_adapter=adapter_mock,
        user_repo=lambda c: None,
        challenge_store=lambda c: None,
    )
    with pytest.raises(RuntimeError):
        with uow:
            raise RuntimeError("boom")
    conn = uow.conn
    conn.rollback.assert_called_once()
    conn.close.assert_called_once()
