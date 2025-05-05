from pydantic_settings import BaseSettings


class Config(BaseSettings):
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

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"
        env_prefix = ""

