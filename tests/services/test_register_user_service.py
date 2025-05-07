import pytest
from unittest.mock import MagicMock
from login_server.services.user_service import RegisterUserService
from login_server.bootstrap import Bootstrap


@pytest.mark.usefixtures("dummy_bootstrap")
def test_register_user_calls_add(monkeypatch):
    # Capture the single DummyUOW instance
    instances = []

    def uow_factory():
        uow = (
            pytest.lazy_fixture("dummy_bootstrap") or MagicMock()
        )  # ignore fixture return
        return uow

    # Instead, override bootstraped.uow to track created UoW
    created = []

    def track_uow():
        u = Bootstrap.bootstraped.uow_orig()
        created.append(u)
        return u

    # unwrap original and wrap
    Bootstrap.bootstraped.uow_orig = Bootstrap.bootstraped.uow
    monkeypatch.setattr(Bootstrap.bootstraped, "uow", track_uow)

    svc = RegisterUserService()
    assert svc("alice", "pw") is True

    # ensure add was called exactly once with correct args
    u = created[0]
    u.users.add.assert_called_once()
    args = u.users.add.call_args[0]
    assert args[0] == "alice"
    assert isinstance(args[1], str) and args[1].startswith("$argon2")


@pytest.mark.usefixtures("dummy_bootstrap")
def test_register_duplicate(monkeypatch):
    # make is_available return False
    class BadUOW:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            pass

        users = MagicMock(is_available=lambda u: False)
        challenges = MagicMock()

    monkeypatch.setattr(Bootstrap.bootstraped, "uow", lambda: BadUOW())
    svc = RegisterUserService()
    assert svc("bob", "pw") is False
