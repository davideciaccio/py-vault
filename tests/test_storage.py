import os
import pytest
from src.storage import VaultStorage


@pytest.fixture
def temp_db(tmp_path):
    """Creates a temporary database file for testing."""
    db_file = tmp_path / "test_vault.db"
    storage = VaultStorage(db_path=str(db_file))
    storage.initialize_db()
    return storage


def test_db_initialization(temp_db):
    """Checks if the tables are created successfully."""
    # If initialize_db failed, operations would raise sqlite3.OperationalError
    assert os.path.exists(temp_db.db_path)


def test_salt_storage_and_retrieval(temp_db):
    """Verifies that the Master Salt is stored and retrieved correctly."""
    original_salt = os.urandom(16)
    temp_db.save_master_salt(original_salt)

    retrieved_salt = temp_db.get_master_salt()
    assert retrieved_salt == original_salt
    assert isinstance(retrieved_salt, bytes)


def test_credential_storage_and_retrieval(temp_db):
    """Tests saving and fetching encrypted credentials."""
    service = "github"
    username = "parrot_user"
    encrypted_blob = os.urandom(48)  # Simulating a nonce + ciphertext bundle

    temp_db.add_credential(service, username, encrypted_blob)

    result = temp_db.get_credential(service)
    assert result is not None
    assert result[0] == username  # Check username
    assert result[1] == encrypted_blob  # Check blob integrity


def test_credential_overwrite(temp_db):
    """Ensures that adding the same service updates the existing record."""
    service = "github"
    temp_db.add_credential(service, "user1", b"blob1")
    temp_db.add_credential(service, "user2", b"blob2")

    result = temp_db.get_credential(service)
    assert result[0] == "user2"
    assert result[1] == b"blob2"
