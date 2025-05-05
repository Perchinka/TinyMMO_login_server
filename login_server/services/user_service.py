import logging
from typing import Optional
from login_server.crypto import ChallengeManager, CryptoUtils
from login_server.domain.repositories import UserRepository

class UserService:
    """
    Business logic for user registration and authentication.
    """

    def __init__(
        self,
        user_repo: UserRepository,
        challenge_mgr: ChallengeManager,
        crypto: CryptoUtils,
    ):
        self.user_repo = user_repo
        self.challenge_mgr = challenge_mgr
        self.crypto = crypto

    def register(self, username: str, password: str) -> bool:
        if not self.user_repo.is_available(username):
            logging.warning(f"Registration failed: '{username}' taken.")
            return False
        pwd_hash = self.crypto.hash_password(password)
        self.user_repo.add(username, pwd_hash)
        logging.info(f"Registered '{username}'.")
        return True

    def generate_challenge(self, username: str) -> Optional[str]:
        stored = self.user_repo.get_password_hash(username)
        if stored is None:
            logging.error(f"No such user '{username}' for challenge.")
            return None
        return self.challenge_mgr.generate_challenge(username)

    def authenticate(self, username: str, client_response: str) -> bool:
        stored = self.user_repo.get_password_hash(username)
        if stored is None:
            logging.error(f"Auth failed: user '{username}' not found.")
            return False
        srv_chal = self.challenge_mgr.get_challenge(username)
        expected = self.crypto.encrypt_challenge(srv_chal, stored)
        if not self.crypto.compare_encrypted(client_response, expected):
            logging.error(f"Auth failed: bad response for '{username}'.")
            return False
        logging.info(f"Authentication successful for '{username}'.")
        return True
