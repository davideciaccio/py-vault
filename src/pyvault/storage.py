import sqlite3
from contextlib import contextmanager


class VaultStorage:
    """Handles all database interactions for PyVault with a unified schema."""

    def __init__(self, db_path="vault.db"):
        self.db_path = db_path
        self._initialize_db()
        # Manteniamo self.conn per compatibilità con i vecchi comandi che non usano ancora _connect
        self.conn = sqlite3.connect(self.db_path)

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
        """Creates the necessary tables with the unified schema."""
        with self._connect() as conn:
            # Tabella di configurazione
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS config (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    master_salt BLOB NOT NULL,
                    master_verifier BLOB NOT NULL
                )
            """
            )

            # Tabella credenziali - Standard: password_blob
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS credentials (
                    service TEXT PRIMARY KEY,
                    username TEXT NOT NULL,
                    password_blob BLOB NOT NULL
                )
            """
            )

    # --- Master Data Management (Richiesti da 'init' e 'audit') ---

    def store_master_data(self, salt: bytes, verifier_blob: bytes):
        """Stores the salt and verifier."""
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO config (id, master_salt, master_verifier) VALUES (1, ?, ?)",
                (salt, verifier_blob),
            )

    def get_master_salt(self) -> bytes:
        """Retrieves the master salt."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT master_salt FROM config WHERE id = 1")
            result = cursor.fetchone()
            return result[0] if result else None

    def get_verifier(self) -> bytes:
        """Retrieves the verifier blob."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT master_verifier FROM config WHERE id = 1")
            result = cursor.fetchone()
            return result[0] if result else None

    # --- Credential Management ---

    def add_credential(self, service: str, username: str, password_blob: bytes):
        """Stores or updates an encrypted credential."""
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO credentials (service, username, password_blob) VALUES (?, ?, ?)",
                (service, username, password_blob),
            )

    def get_credential(self, service: str):
        """Fetches a specific credential."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT username, password_blob FROM credentials WHERE service = ?",
                (service,),
            )
            return cursor.fetchone()

    def get_all_credentials(self):
        """Used by the 'list' command."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT service, username FROM credentials ORDER BY service ASC"
            )
            return cursor.fetchall()

    def get_full_inventory(self):
        """Used by the 'audit' command."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT service, username, password_blob FROM credentials")
            return cursor.fetchall()

    def delete_credential(self, service: str):
        """Used by the 'rm' command."""
        with self._connect() as conn:
            conn.execute("DELETE FROM credentials WHERE service = ?", (service,))
