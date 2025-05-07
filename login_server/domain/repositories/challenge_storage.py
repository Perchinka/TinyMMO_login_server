from abc import ABC, abstractmethod
from typing import Any


class AbstractChallengeStorage(ABC):
    """High-level interface for storing/retrieving one-time challenges."""

    @abstractmethod
    def __init__(self, conn: Any) -> None:
        super().__init__()

    @abstractmethod
    def store(self, username: str, challenge: str) -> None: ...

    @abstractmethod
    def retrieve(self, username: str) -> str: ...
