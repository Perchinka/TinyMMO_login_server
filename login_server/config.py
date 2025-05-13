from enum import Enum
from pydantic_settings import SettingsConfigDict, BaseSettings


class ChallengeBackend(str, Enum):
    LOCAL = "local"
    REDIS = "redis"


class Config(BaseSettings):
    """
    Application settings, loaded from environment and .env,
    with strict validation.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid",
    )

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "postgres"

    REDIS_URL: str = "redis://localhost:6379/0"

    CHALLENGE_BACKEND: ChallengeBackend = ChallengeBackend.LOCAL

    LOGGING_LEVEL: str = "INFO"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
