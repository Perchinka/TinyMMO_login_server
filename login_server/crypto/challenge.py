import secrets
from typing import Dict


class ChallengeManager:
    """
    Handles one-time nonces for login challenges.
    """

    def __init__(self):
        self._challenges: Dict[str, str] = {}

    def generate_challenge(self, username: str) -> str:
        """
        Generate a new random challenge for `username` and store it.
        Returns the challenge string.
        """
        nonce = secrets.token_hex(32)
        self._challenges[username] = nonce
        return nonce

    def get_challenge(self, username: str) -> str:
        """
        Retrieve the stored challenge for `username`, or empty string if none.
        """
        return self._challenges.get(username, "")
