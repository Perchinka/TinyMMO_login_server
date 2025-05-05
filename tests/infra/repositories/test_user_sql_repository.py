def test_is_available_returns_true_when_no_user(fake_conn, user_sql_repo):
    fake_conn.cursor_obj._fetch = None
    assert user_sql_repo.is_available("alice") is True

def test_is_available_returns_false_when_user_exists(fake_conn, user_sql_repo):
    fake_conn.cursor_obj._fetch = (1,)
    assert user_sql_repo.is_available("bob") is False

def test_add_inserts_record_with_correct_sql(fake_conn, user_sql_repo):
    user_sql_repo.add("carol", "hashv")
    sql, params = fake_conn.cursor_obj.commands[-1]
    assert "INSERT INTO users" in sql
    assert params == ("carol", "hashv")

def test_get_password_hash_returns_value_when_exists(fake_conn, user_sql_repo):
    fake_conn.cursor_obj._fetch = ("phash",)
    assert user_sql_repo.get_password_hash("dave") == "phash"

def test_get_password_hash_returns_none_when_missing(fake_conn, user_sql_repo):
    fake_conn.cursor_obj._fetch = None
    assert user_sql_repo.get_password_hash("eve") is None
