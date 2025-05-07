import pytest


def test_is_available_true(connection_mock, user_sql_repo):
    cur = connection_mock.cursor.return_value.__enter__.return_value
    cur.fetchone.return_value = None
    assert user_sql_repo.is_available("alice") is True
    cur.execute.assert_called_once_with(
        "SELECT 1 FROM users WHERE username = %s;", ("alice",)
    )


def test_is_available_false(connection_mock, user_sql_repo):
    cur = connection_mock.cursor.return_value.__enter__.return_value
    cur.fetchone.return_value = (1,)
    assert user_sql_repo.is_available("bob") is False


def test_add_executes_insert(connection_mock, user_sql_repo):
    repo = user_sql_repo
    repo.add("carol", "h")
    cur = connection_mock.cursor.return_value.__enter__.return_value
    cur.execute.assert_called_once_with(
        "INSERT INTO users (username, password_hash) VALUES (%s, %s);", ("carol", "h")
    )


def test_get_password_hash(connection_mock, user_sql_repo):
    cur = connection_mock.cursor.return_value.__enter__.return_value
    # when present
    cur.fetchone.return_value = ("ph",)
    assert user_sql_repo.get_password_hash("dave") == "ph"
    cur.execute.assert_called_with(
        "SELECT password_hash FROM users WHERE username = %s;", ("dave",)
    )
    # when missing
    cur.fetchone.return_value = None
    assert user_sql_repo.get_password_hash("eve") is None
