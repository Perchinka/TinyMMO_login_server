import time
import pytest
from unittest.mock import MagicMock
from login_server.infra.repositories.challenge_storage import (
    LocalChallengeStorage,
    RedisChallengeStorage,
)
from login_server.common.exceptions import ChallengeNotFoundError


def test_local_challenge_available_within_ttl(monkeypatch):
    """
    LocalChallengeStorage.retrieve should return the stored challenge
    if called before the TTL expires.
    """
    # Freeze time at 100
    monkeypatch.setattr(time, "time", lambda: 100)
    storage = LocalChallengeStorage(ttl_seconds=10)
    storage.store("userA", "challengeA")

    # Advance to 105 (within TTL)
    monkeypatch.setattr(time, "time", lambda: 105)
    result = storage.retrieve("userA")
    assert result == "challengeA"


def test_local_challenge_raises_after_ttl(monkeypatch):
    """
    LocalChallengeStorage.retrieve should raise ChallengeNotFoundError
    if called after the TTL has expired.
    """
    # Freeze time at 200
    monkeypatch.setattr(time, "time", lambda: 200)
    storage = LocalChallengeStorage(ttl_seconds=5)
    storage.store("userA", "challengeA")

    # Advance to 206 (past TTL)
    monkeypatch.setattr(time, "time", lambda: 206)
    with pytest.raises(ChallengeNotFoundError) as exc:
        storage.retrieve("userA")
    assert "has expired" in str(exc.value)


def test_local_challenge_raises_when_no_entry():
    """
    LocalChallengeStorage.retrieve should raise ChallengeNotFoundError
    if no challenge was ever stored.
    """
    storage = LocalChallengeStorage(ttl_seconds=5)
    with pytest.raises(ChallengeNotFoundError) as exc:
        storage.retrieve("no_such_user")
    assert "No challenge found" in str(exc.value)


def test_redis_challenge_store_and_retrieve_bytes():
    """
    RedisChallengeStorage.store should call setex correctly,
    and retrieve should return the raw bytes when present.
    """
    mock_client = MagicMock()
    storage = RedisChallengeStorage(mock_client, ttl_seconds=20)

    storage.store("userB", "valueB")
    mock_client.setex.assert_called_once_with("challenge:userB", 20, "valueB")

    mock_client.get.return_value = b"bytes_value"
    result = storage.retrieve("userB")
    assert result == b"bytes_value"


def test_redis_challenge_retrieve_raises_when_none():
    """
    RedisChallengeStorage.retrieve should raise ChallengeNotFoundError
    when Redis.get() returns None.
    """
    mock_client = MagicMock()
    mock_client.get.return_value = None
    storage = RedisChallengeStorage(mock_client, ttl_seconds=5)

    with pytest.raises(ChallengeNotFoundError) as exc:
        storage.retrieve("userC")
    assert "No challenge found" in str(exc.value)
