import os

from login_server.common.logging import setup_logger


class Config:
    # TODO put in __init__ so it wouldn't load on import
    """
    Application configuration, loaded from environment variables.

    Attributes:
        DB_HOST (str): PostgreSQL host.
        DB_PORT (int): PostgreSQL port.
        DB_USER (str): PostgreSQL username.
        DB_PASSWORD (str): PostgreSQL password.
        DB_NAME (str): PostgreSQL database name.

    Properties:
        DATABASE_URL (str): SQLAlchemy-style database URL.
    """

    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")
    DB_NAME: str = os.getenv("DB_NAME", "postgres")

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")

    def __init__(self) -> None:
        setup_logger(self.LOGGING_LEVEL)
