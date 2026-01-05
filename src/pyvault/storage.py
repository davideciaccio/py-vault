import sqlite3


class VaultStorage:
    """Handles all database interactions for PyVault."""

    def __init__(self, db_path="vault.db"):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def initialize_db(self):
        """Creates the necessary tables if they do not exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Credentials table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS credentials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    service TEXT UNIQUE NOT NULL,
                    username TEXT NOT NULL,
                    encrypted_data BLOB NOT NULL
                )
            """
            )
            # Table for system secrets (like the Salt)
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS system_secrets (
                    key TEXT PRIMARY KEY,
                    value BLOB NOT NULL
                )
            """
            )
            conn.commit()

    def save_master_salt(self, salt: bytes):
        """Saves the unique salt for this installation."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO system_secrets (key, value) VALUES ('master_salt', ?)",
                (salt,),
            )
            conn.commit()

    def get_master_salt(self) -> bytes:
        """Retrieves the salt from the database."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM system_secrets WHERE key = 'master_salt'")
            result = cursor.fetchone()
            return result[0] if result else None

    def add_credential(self, service: str, username: str, encrypted_blob: bytes):
        """Stores a new encrypted credential."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO credentials (service, username, encrypted_data) VALUES (?, ?, ?)",
                (service, username, encrypted_blob),
            )
            conn.commit()

    def get_credential(self, service: str):
        """Fetches the credential for a specific service."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT username, encrypted_data FROM credentials WHERE service = ?",
                (service,),
            )
            return cursor.fetchone()  # Returns (username, blob) or None
