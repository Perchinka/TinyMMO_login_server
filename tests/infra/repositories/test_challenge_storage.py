import time
import pytest
from unittest.mock import MagicMock
from login_server.infra.repositories.challenge_storage import (
    LocalChallengeStorage,
    RedisChallengeStorage,
)


def test_local_challenge_available_before_ttl_and_expires_after(monkeypatch):
    """
    LocalChallengeStorage should return the stored challenge until TTL has passed,
    then return an empty string and remove the expired entry.
    """
    # Freeze initial time to 100
    monkeypatch.setattr(time, "time", lambda: 100)
    storage = LocalChallengeStorage(ttl_seconds=10)
    storage.store("userA", "challengeA")

    # Advance to time 105 (within TTL)
    monkeypatch.setattr(time, "time", lambda: 105)
    assert storage.retrieve("userA") == "challengeA"

    # Advance to time 111 (past TTL)
    monkeypatch.setattr(time, "time", lambda: 111)
    assert storage.retrieve("userA") == ""  # expired

    assert storage.retrieve("userA") == ""


def test_local_challenge_retrieve_without_store_always_empty():
    """
    Retrieving a challenge that was never stored should return an empty string.
    """
    storage = LocalChallengeStorage(ttl_seconds=5)
    assert storage.retrieve("no_such_user") == ""


def test_redis_challenge_store_calls_setex_with_correct_namespace_and_ttl():
    """
    RedisChallengeStorage.store() should call Redis.setex() using key 'challenge:<username>'.
    """
    mock_client = MagicMock()
    storage = RedisChallengeStorage(mock_client, ttl_seconds=20)

    storage.store("userB", "valueB")

    mock_client.setex.assert_called_once_with("challenge:userB", 20, "valueB")


def test_redis_challenge_retrieve_returns_bytes_as_string():
    """
    RedisChallengeStorage.retrieve() should wrap the raw bytes result in str() if present.
    """
    mock_client = MagicMock()
    mock_client.get.return_value = b"bytes_value"
    storage = RedisChallengeStorage(mock_client, ttl_seconds=5)

    result = storage.retrieve("userB")

    assert result == "b'bytes_value'"


def test_redis_challenge_retrieve_none_returns_none_string():
    """
    If Redis.get() returns None, retrieve() should return the string 'None'.
    """
    mock_client = MagicMock()
    mock_client.get.return_value = None
    storage = RedisChallengeStorage(mock_client, ttl_seconds=5)

    result = storage.retrieve("userC")

    assert result == "None"


def test_redis_challenge_retrieve_empty_string_returns_empty():
    """
    If Redis.get() returns an empty string, retrieve() should return an empty string.
    """
    mock_client = MagicMock()
    mock_client.get.return_value = ""
    storage = RedisChallengeStorage(mock_client, ttl_seconds=5)

    result = storage.retrieve("userD")

    assert result == ""
