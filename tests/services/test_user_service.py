from login_server.crypto.crypto_utils import CryptoUtils

def test_register_new_user_returns_true(user_service):
    assert user_service.register("alice", "password") is True

def test_register_stores_hashed_password(user_sql_repo, user_service):
    user_service.register("gwen", "topsecret")
    assert user_sql_repo.get_password_hash("gwen") != "topsecret"
    assert len(user_sql_repo.get_password_hash("gwen")) == 64

def test_register_duplicate_user_returns_false(user_service):
    user_service.register("bob", "password")
    assert user_service.register("bob", "password") is False

def test_generate_challenge_for_existing_user(user_service):
    user_service.register("carol", "pw")
    challenge = user_service.generate_challenge("carol")
    assert isinstance(challenge, str)

def test_generate_challenge_for_unknown_user_returns_none(user_service):
    assert user_service.generate_challenge("unknown") is None

def test_authenticate_valid_response_returns_true(user_service):
    user_service.register("dave", "secret")
    challenge = user_service.generate_challenge("dave")
    key = CryptoUtils.hash_password("secret")
    response = CryptoUtils.encrypt_challenge(challenge, key)
    assert user_service.authenticate("dave", response) is True

def test_authenticate_unknown_user_returns_false(user_service):
    assert user_service.authenticate("eve", "any") is False

def test_authenticate_wrong_response_returns_false(user_service):
    user_service.register("frank", "pwX")
    challenge = user_service.generate_challenge("frank") 
    assert user_service.authenticate("frank", "invalid") is False
