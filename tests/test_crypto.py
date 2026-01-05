import pytest
import os
from src.crypto import CryptoManager


def test_encryption_decryption_cycle():
    """Test that data encrypted can be correctly decrypted with the same key."""
    crypto = CryptoManager()
    password = "MasterPassword123!"
    salt = os.urandom(16)
    secret_data = "MySuperSecretBankPassword"

    # 1. Derive Key
    key = crypto.derive_key(password, salt)

    # 2. Encrypt
    encrypted_bundle = crypto.encrypt(secret_data, key)

    # 3. Decrypt
    decrypted_data = crypto.decrypt(encrypted_bundle, key)

    assert decrypted_data == secret_data
    assert decrypted_data != encrypted_bundle  # Check it's actually encrypted


def test_wrong_password_fails():
    """Test that a wrong password cannot decrypt the data (Auth Tag check)."""
    crypto = CryptoManager()
    salt = os.urandom(16)

    key_correct = crypto.derive_key("correct_password", salt)
    key_wrong = crypto.derive_key("wrong_password", salt)

    encrypted = crypto.encrypt("Sensitive Info", key_correct)

    # AES-GCM must raise an InvalidTag exception when the key is wrong
    from cryptography.exceptions import InvalidTag

    with pytest.raises(InvalidTag):
        crypto.decrypt(encrypted, key_wrong)
