import pytest
from login_server.crypto.crypto_utils import CryptoUtils

def test_hash_password_returns_string():
    result = CryptoUtils.hash_password("password")
    assert isinstance(result, str)
    assert len(result) > 0

def test_encrypt_challenge_is_deterministic():
    key = CryptoUtils.hash_password("password")
    e1 = CryptoUtils.encrypt_challenge("challenge", key)
    e2 = CryptoUtils.encrypt_challenge("challenge", key)
    assert e1 == e2

def test_compare_encrypted_returns_true_for_same_input():
    key = CryptoUtils.hash_password("password")
    encrypted = CryptoUtils.encrypt_challenge("challenge", key)
    assert CryptoUtils.compare_encrypted(encrypted, encrypted)

def test_compare_encrypted_returns_false_for_different_input():
    key1 = CryptoUtils.hash_password("pass1")
    key2 = CryptoUtils.hash_password("pass2")
    e1 = CryptoUtils.encrypt_challenge("challenge", key1)
    e2 = CryptoUtils.encrypt_challenge("challenge", key2)
    assert not CryptoUtils.compare_encrypted(e1, e2)

