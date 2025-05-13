import os

from login_server.common.logging import setup_logger


class Config:
    # TODO put in __init__ so it wouldn't load on import
    """
    Application configuration, loaded from environment variables.

    Attributes:
        POSTGRES_HOST (str): PostgreSQL host.
        POSTGRES_PORT (int): PostgreSQL port.
        POSTGRES_USER (str): PostgreSQL username.
        POSTGRES_PASSWORD (str): PostgreSQL password.
        POSTGRES_DB (str): PostgreSQL database name.

    Properties:
        DATABASE_URL (str): SQLAlchemy-style database URL.
    """

    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "postgres")

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")

    def __init__(self) -> None:
        setup_logger(self.LOGGING_LEVEL)
