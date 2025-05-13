class UserAlreadyExistsError(Exception):
    """
    Raised when attempting to register a username that's already taken.
    """

    pass


class UserNotFoundError(Exception):
    """
    Raised when an operation references a user that does not exist.
    """

    pass


class AuthenticationError(Exception):
    """
    Raised when user authentication fails (bad credentials or expired challenge).
    """

    pass


class ChallengeNotFoundError(Exception):
    """
    Raised when a one‐time login challenge is not found or has expired.
    """

    pass
