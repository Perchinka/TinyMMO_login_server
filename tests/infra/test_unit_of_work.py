import pytest
from login_server.infra.unit_of_work import UnitOfWork


def test_unit_of_work_initializes_connection_and_repositories(adapter_mock):
    """
    When entering the UnitOfWork context .conn, .users, and .challenges attributes are exposed on the context.
    """
    stub_user_repo = lambda conn: "USER_REPOSITORY"
    stub_challenge_store = lambda client: "CHALLENGE_STORE"

    uow = UnitOfWork(
        sql_adapter=adapter_mock,
        redis_adapter=adapter_mock,
        user_repo=stub_user_repo,  # type: ignore
        challenge_store=stub_challenge_store,  # type: ignore
    )

    with uow as context:
        assert adapter_mock.connect.call_count == 2, "Expected two calls to connect()"
        adapter_mock.ensure_schema.assert_called_once_with(context.conn)

        assert context.conn is adapter_mock.connect.return_value
        assert context.users == "USER_REPOSITORY"
        assert context.challenges == "CHALLENGE_STORE"


def test_unit_of_work_commits_and_closes_on_success(adapter_mock):
    """
    Exiting the UnitOfWork context without errors should commit the SQL transaction
    and then close the connection.
    """
    uow = UnitOfWork(
        sql_adapter=adapter_mock,
        redis_adapter=adapter_mock,
        user_repo=lambda conn: None,  # type: ignore
        challenge_store=lambda client: None,  # type: ignore
    )

    with uow:
        pass

    conn = uow.conn
    conn.commit.assert_called_once()
    conn.close.assert_called_once()


def test_unit_of_work_rolls_back_and_closes_on_exception(adapter_mock):
    """
    If an exception is raised inside the UnitOfWork context,
    it should rollback the SQL transaction and then close the connection.
    """
    uow = UnitOfWork(
        sql_adapter=adapter_mock,
        redis_adapter=adapter_mock,
        user_repo=lambda conn: None,  # type: ignore
        challenge_store=lambda client: None,  # type: ignore
    )

    with pytest.raises(RuntimeError):
        with uow:
            raise RuntimeError("force rollback")

    conn = uow.conn
    conn.rollback.assert_called_once()
    conn.close.assert_called_once()
