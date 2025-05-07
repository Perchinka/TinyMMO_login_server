import os
from typing import Tuple

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes


class ChallengeEncryptor:
    """
    Derive per-session keys from the Argon2 password hash via HKDF‐SHA256,
    then encrypt/decrypt challenges with ChaCha20-Poly1305.
    """

    def derive_key(self, password_hash: str, salt: bytes) -> bytes:
        """
        HKDF-SHA256 to 32-byte key.  `salt` can be stored alongside the user record
        or regenerated per‐challenge.
        """
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            info=b"tiny-mmo-login-challenge",
        )
        return hkdf.derive(password_hash.encode("utf-8"))

    def encrypt(self, plaintext: str, key: bytes) -> Tuple[bytes, bytes]:
        """
        Returns (nonce, ciphertext).
        """
        aead = ChaCha20Poly1305(key)
        nonce = os.urandom(12)
        ct = aead.encrypt(nonce, plaintext.encode("utf-8"), associated_data=None)
        return nonce, ct

    def decrypt(self, nonce: bytes, ciphertext: bytes, key: bytes) -> str:
        """
        Returns the decrypted plaintext.
        """
        aead = ChaCha20Poly1305(key)
        pt = aead.decrypt(nonce, ciphertext, associated_data=None)
        return pt.decode("utf-8")
