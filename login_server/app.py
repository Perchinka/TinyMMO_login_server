
from .infra.unit_of_work import UnitOfWork
from .crypto.challenge import ChallengeManager
from .crypto.crypto_utils import CryptoUtils
from .services.user_service import UserService

def create_app(settings):
    challenge_mgr = ChallengeManager()
    crypto = CryptoUtils()

    def register(username: str, password: str) -> bool:
        with UnitOfWork(settings.DATABASE_URL) as uow:
            svc = UserService(uow.users, challenge_mgr, crypto)
            return svc.register(username, password)

    def authenticate(username: str, client_resp: str) -> bool:
        with UnitOfWork(settings.DATABASE_URL) as uow:
            svc = UserService(uow.users, challenge_mgr, crypto)
            return svc.authenticate(username, client_resp)

    return {"register": register, "authenticate": authenticate}
