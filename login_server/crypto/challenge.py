"""
auth/challenge.py

Manages generation and retrieval of authentication challenges.
"""

class ChallengeManager:
    """
    Handles nonces.
    """
    def generate_challenge(self, username: str) -> str:
        """
        Generate a new random challenge for `username` and temporaraly store it.
        """
        return ""

    def get_challenge(self, username: str) -> str:
        """
        Retrieve the stored challenge for `username`, or empty string.
        """
        return ""
