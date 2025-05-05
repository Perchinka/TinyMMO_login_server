from login_server.config import Config
from login_server.crypto.challenge import ChallengeManager
from login_server.crypto.crypto_utils import CryptoUtils
from login_server.services.user_service import UserService
from login_server.infra.adapters.postgresql_adapter import PostgreSQLAdapter
from login_server.infra.unit_of_work import UnitOfWork


def create_app(config: Config) -> dict[str, callable]:
    """
    Application factory. Wires configuration, infrastructure, crypto, and services.

    Returns a dict with 'register' and 'authenticate' callables.
    """
    adapter = PostgreSQLAdapter(config.DATABASE_URL)
    challenge_mgr = ChallengeManager()
    crypto = CryptoUtils()

    def register(username: str, password: str) -> bool:
        with UnitOfWork(adapter) as uow:
            svc = UserService(uow.users, challenge_mgr, crypto)
            return svc.register(username, password)

    def authenticate(username: str, client_resp: str) -> bool:
        with UnitOfWork(adapter) as uow:
            svc = UserService(uow.users, challenge_mgr, crypto)
            return svc.authenticate(username, client_resp)

    return {"register": register, "authenticate": authenticate}
