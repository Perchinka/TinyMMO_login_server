import pytest


def test_is_available_returns_true_when_no_user_found(connection_mock, user_sql_repo):
    """
    is_available() should return True when the database query yields no rows.
    """
    mock_cursor = connection_mock.cursor.return_value.__enter__.return_value
    mock_cursor.fetchone.return_value = None

    assert user_sql_repo.is_available("alice") is True
    mock_cursor.execute.assert_called_once_with(
        "SELECT 1 FROM users WHERE username = %s;", ("alice",)
    )


def test_is_available_returns_false_when_user_exists(connection_mock, user_sql_repo):
    """
    is_available() should return False when the database query finds a matching row.
    """
    mock_cursor = connection_mock.cursor.return_value.__enter__.return_value
    mock_cursor.fetchone.return_value = (1,)

    assert user_sql_repo.is_available("bob") is False


def test_add_inserts_new_user_record(connection_mock, user_sql_repo):
    """
    add() should execute an INSERT statement with the provided username and password_hash.
    """
    user_sql_repo.add("carol", "hash_value")

    mock_cursor = connection_mock.cursor.return_value.__enter__.return_value
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO users (username, password_hash) VALUES (%s, %s);",
        ("carol", "hash_value"),
    )


def test_get_password_hash_returns_value_or_none(connection_mock, user_sql_repo):
    """
    get_password_hash() should return the stored hash when present, otherwise None.
    """
    mock_cursor = connection_mock.cursor.return_value.__enter__.return_value

    mock_cursor.fetchone.return_value = ("stored_hash",)
    result = user_sql_repo.get_password_hash("dave")
    assert result == "stored_hash"
    mock_cursor.execute.assert_called_with(
        "SELECT password_hash FROM users WHERE username = %s;", ("dave",)
    )

    mock_cursor.fetchone.return_value = None
    result = user_sql_repo.get_password_hash("eve")
    assert result is None
