from abc import ABC, abstractmethod
from typing import Any


class AbstractRedisAdapter(ABC):
    @abstractmethod
    def connect(self) -> Any:
        """Open and return a Redis client/connection."""
        ...
