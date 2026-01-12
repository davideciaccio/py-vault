import sqlite3
from contextlib import contextmanager
from pathlib import Path
from platformdirs import user_data_dir

# Application name used for system-specific data directories
APP_NAME = "pyvault"


class VaultStorage:
    """Handles all database interactions for PyVault with a unified schema."""

    def __init__(self, db_path=None):
        """
        Initialize the storage.
        If no db_path is provided, it uses the standard system data directory.
        """
        if db_path is None:
            # Get the OS-specific data directory for 'pyvault'
            # Windows: %LOCALAPPDATA%/pyvault/
            # Linux: ~/.local/share/pyvault/
            data_dir = Path(user_data_dir(APP_NAME, appauthor=False))

            # Ensure the directory exists before attempting to create the database file
            data_dir.mkdir(parents=True, exist_ok=True)
            self.db_path = data_dir / "vault.db"
        else:
            # Allows passing a custom path (useful for testing)
            self.db_path = Path(db_path)

        self._initialize_db()

        # Keep a persistent connection for backward compatibility with older commands
        self.conn = sqlite3.connect(str(self.db_path))

    @contextmanager
    def _connect(self):
        """Context manager for reliable database connections."""
        # Using str() for compatibility with older sqlite3 versions
        conn = sqlite3.connect(str(self.db_path))
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _initialize_db(self):
        """Creates the necessary tables if they do not exist."""
        with self._connect() as conn:
            # Configuration table for security parameters
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS config (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    master_salt BLOB NOT NULL,
                    master_verifier BLOB NOT NULL
                )
            """
            )

            # Credentials table for storing encrypted secrets
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS credentials (
                    service TEXT PRIMARY KEY,
                    username TEXT NOT NULL,
                    password_blob BLOB NOT NULL
                )
            """
            )

    # --- Master Data Management ---

    def store_master_data(self, salt: bytes, verifier_blob: bytes):
        """Stores the master salt and password verifier."""
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO config (id, master_salt, master_verifier) VALUES (1, ?, ?)",
                (salt, verifier_blob),
            )

    def get_master_salt(self) -> bytes:
        """Retrieves the master salt used for key derivation."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT master_salt FROM config WHERE id = 1")
            result = cursor.fetchone()
            return result[0] if result else None

    def get_verifier(self) -> bytes:
        """Retrieves the verifier blob to check the master password."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT master_verifier FROM config WHERE id = 1")
            result = cursor.fetchone()
            return result[0] if result else None

    # --- Credential Management ---

    def add_credential(self, service: str, username: str, password_blob: bytes):
        """Stores or updates an encrypted credential for a specific service."""
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO credentials (service, username, password_blob) VALUES (?, ?, ?)",
                (service, username, password_blob),
            )

    def get_credential(self, service: str):
        """Fetches the username and encrypted blob for a specific service."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT username, password_blob FROM credentials WHERE service = ?",
                (service,),
            )
            return cursor.fetchone()

    def get_all_credentials(self):
        """Returns a list of all stored services and their usernames."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT service, username FROM credentials ORDER BY service ASC"
            )
            return cursor.fetchall()

    def get_full_inventory(self):
        """Retrieves all stored data for auditing purposes."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT service, username, password_blob FROM credentials")
            return cursor.fetchall()

    def delete_credential(self, service: str):
        """Removes a credential from the vault."""
        with self._connect() as conn:
            conn.execute("DELETE FROM credentials WHERE service = ?", (service,))
