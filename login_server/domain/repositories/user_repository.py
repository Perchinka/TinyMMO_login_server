from abc import ABC, abstractmethod
from typing import Optional

class UserRepository(ABC):
    """
    Domain-level interface for user persistence.
    """

    @abstractmethod
    def is_available(self, username: str) -> bool:
        """True if username not yet taken."""
        ...

    @abstractmethod
    def add(self, username: str, password_hash: str) -> None:
        """Persist a new user."""
        ...

    @abstractmethod
    def get_password_hash(self, username: str) -> Optional[str]:
        """Return stored password_hash or None."""
        ...

