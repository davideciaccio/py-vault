import os
from argon2 import low_level
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class CryptoManager:
    """
    Handles cryptographic operations including key derivation and
    authenticated encryption/decryption.
    """

    def __init__(self):
        # AES-256-GCM standard sizes
        self.key_size = 32  # 256 bits
        self.salt_size = 16  # 128 bits
        self.nonce_size = 12  # Recommended for GCM

        # Argon2id parameters
        self.time_cost = 3
        self.memory_cost = 65536  # 64MB
        self.parallelism = 4

    def derive_key(self, master_password: str, salt: bytes) -> bytes:
        """
        Derives a high-entropy 32-byte key from a password using Argon2id.
        """
        return low_level.hash_secret_raw(
            secret=master_password.encode(),
            salt=salt,
            time_cost=self.time_cost,
            memory_cost=self.memory_cost,
            parallelism=self.parallelism,
            hash_len=self.key_size,
            type=low_level.Type.ID,
        )

    def encrypt(self, data: str, key: bytes) -> bytes:
        """
        Encrypts data using AES-256-GCM.
        Returns: nonce + ciphertext (tag is included by cryptography lib).
        """
        aesgcm = AESGCM(key)
        nonce = os.urandom(self.nonce_size)
        ciphertext = aesgcm.encrypt(nonce, data.encode(), None)
        return nonce + ciphertext

    def decrypt(self, encrypted_bundle: bytes, key: bytes) -> str:
        """
        Decrypts an AES-256-GCM encrypted bundle.
        """
        nonce = encrypted_bundle[: self.nonce_size]
        ciphertext = encrypted_bundle[self.nonce_size :]

        aesgcm = AESGCM(key)
        decrypted_data = aesgcm.decrypt(nonce, ciphertext, None)
        return decrypted_data.decode()
