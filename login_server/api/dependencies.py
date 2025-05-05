from fastapi import Depends
from login_server.config import Config
from login_server.crypto.challenge import ChallengeManager
from login_server.crypto.crypto_utils import CryptoUtils
from login_server.infra.adapters.postgresql_adapter import PostgreSQLAdapter

def get_config() -> Config:
    return Config()

def get_adapter(cfg: Config = Depends(get_config)) -> PostgreSQLAdapter:
    return PostgreSQLAdapter(cfg.DATABASE_URL)

def get_challenge_mgr() -> ChallengeManager:
    return ChallengeManager()

def get_crypto_utils() -> CryptoUtils:
    return CryptoUtils()

