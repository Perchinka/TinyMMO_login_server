from abc import ABC, abstractmethod
from typing import Any


class AbstractSQLAdapter(ABC):
    """
    Abstract interface for a SQL engine adapter.
    Provides methods to open a connection and ensure schema.
    """

    @abstractmethod
    def connect(self) -> Any:
        """
        Open and return a new database connection.
        The connection must start in manual‐commit mode.
        """
        ...

    @abstractmethod
    def ensure_schema(self, connection: Any) -> None:
        """
        Execute any DDL required to initialize the schema.
        """
        ...
