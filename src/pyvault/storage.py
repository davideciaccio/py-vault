import sqlite3
from contextlib import contextmanager


class VaultStorage:
    """Handles all database interactions for PyVault with integrity checks."""

    def __init__(self, db_path="vault.db"):
        self.db_path = db_path
        self._initialize_db()

    @contextmanager
    def _connect(self):
        """Context manager for reliable database connections."""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _initialize_db(self):
        """Creates the necessary tables for configuration and credentials."""
        with self._connect() as conn:
            # Table for system configuration (Salt and Master Verifier)
            # We use a single row (id=1) to ensure global configuration
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS config (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    master_salt BLOB NOT NULL,
                    master_verifier BLOB NOT NULL
                )
            """
            )

            # Credentials table
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS credentials (
                    service TEXT PRIMARY KEY,
                    username TEXT NOT NULL,
                    encrypted_data BLOB NOT NULL
                )
            """
            )

    # --- Master Data Management (Used during init and authentication) ---

    def store_master_data(self, salt: bytes, verifier_blob: bytes):
        """Stores the salt and the encrypted canary (verifier) in one atomic operation."""
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO config (id, master_salt, master_verifier) VALUES (1, ?, ?)",
                (salt, verifier_blob),
            )

    def get_master_salt(self) -> bytes:
        """Retrieves the master salt for key derivation."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT master_salt FROM config WHERE id = 1")
            result = cursor.fetchone()
            return result[0] if result else None

    def get_verifier(self) -> bytes:
        """Retrieves the encrypted verifier (canary) for password validation."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT master_verifier FROM config WHERE id = 1")
            result = cursor.fetchone()
            return result[0] if result else None

    # --- Credential Management ---

    def add_credential(self, service: str, username: str, encrypted_blob: bytes):
        """Stores or updates an encrypted credential."""
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO credentials (service, username, encrypted_data) VALUES (?, ?, ?)",
                (service, username, encrypted_blob),
            )

    def get_credential(self, service: str):
        """Fetches the credential for a specific service."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT username, encrypted_data FROM credentials WHERE service = ?",
                (service,),
            )
            return cursor.fetchone()  # Returns (username, blob) or None

    def list_all_services(self):
        """Returns a list of all stored services (without passwords)."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT service, username FROM credentials ORDER BY service ASC"
            )
            return cursor.fetchall()
