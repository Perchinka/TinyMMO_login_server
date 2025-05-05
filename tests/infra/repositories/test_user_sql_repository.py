def test_is_available_returns_true_when_no_user(connection_mock, user_sql_repo):
    cursor = connection_mock.cursor.return_value
    cursor.__enter__.return_value.fetchone.return_value = None

    assert user_sql_repo.is_available("alice") is True
    cursor.__enter__.return_value.execute.assert_called_once_with(
        "SELECT 1 FROM users WHERE username = %s;",
        ("alice",)
    )

def test_is_available_returns_false_when_user_exists(connection_mock, user_sql_repo):
    cursor = connection_mock.cursor.return_value
    cursor.__enter__.return_value.fetchone.return_value = (1,)

    assert user_sql_repo.is_available("bob") is False

def test_add_executes_insert_sql(connection_mock, user_sql_repo):
    cursor = connection_mock.cursor.return_value

    user_sql_repo.add("carol", "hashv")
    cursor.__enter__.return_value.execute.assert_called_once_with(
        "INSERT INTO users (username, password_hash) VALUES (%s, %s);",
        ("carol", "hashv")
    )

def test_get_password_hash_returns_value_when_exists(connection_mock, user_sql_repo):
    cursor = connection_mock.cursor.return_value
    cursor.__enter__.return_value.fetchone.return_value = ("phash",)

    assert user_sql_repo.get_password_hash("dave") == "phash"
    cursor.__enter__.return_value.execute.assert_called_once_with(
        "SELECT password_hash FROM users WHERE username = %s;",
        ("dave",)
    )

def test_get_password_hash_returns_none_when_missing(connection_mock, user_sql_repo):
    cursor = connection_mock.cursor.return_value
    cursor.__enter__.return_value.fetchone.return_value = None

    assert user_sql_repo.get_password_hash("eve") is None
    cursor.__enter__.return_value.execute.assert_called_once_with(
        "SELECT password_hash FROM users WHERE username = %s;",
        ("eve",)
    )
