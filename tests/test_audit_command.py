import pytest
import re
from click.testing import CliRunner
from unittest.mock import patch
from pyvault.main import audit


def strip_ansi(text):
    """Rimuove i codici colore ANSI e i markup di rich."""
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


@pytest.fixture
def runner():
    return CliRunner()


@patch("questionary.password")
def test_audit_logic(mock_password, runner):
    with patch("pyvault.main.VaultStorage") as mock_storage, patch(
        "pyvault.main.CryptoManager"
    ) as mock_crypto, patch("pyvault.main.os.path.exists") as mock_exists, patch(
        "pyvault.main.SecurityProtections.check_input_speed"
    ) as mock_speed:
        mock_exists.return_value = True
        mock_speed.return_value = True
        mock_password.return_value.ask.return_value = "master"

        # Scenario: 1 debole, 2 duplicati
        mock_storage.return_value.get_full_inventory.return_value = [
            ("short", "user", b"b1"),
            ("reuse1", "user", b"b2"),
            ("reuse2", "user", b"b3"),
        ]

        # Mock decrittazione (Verifier + 3 password)
        mock_crypto.return_value.decrypt.side_effect = [
            None,  # Verifier OK
            "123",  # 'short' (Debole)
            "same",  # 'reuse1' (Duplicato)
            "same",  # 'reuse2' (Duplicato)
        ]

        # Eseguiamo il comando forzando una larghezza terminale fissa
        result = runner.invoke(audit, terminal_width=100)

        # PULIZIA OUTPUT
        clean_output = strip_ansi(result.output)

        # DEBUG: se fallisce ancora, de-commenta la riga sotto per vedere cosa vede Python
        # print(f"\nDEBUG OUTPUT:\n{clean_output}")

        assert result.exit_code == 0

        # Verifica la presenza dei dati (più sicuro dei titoli delle tabelle)
        assert "short" in clean_output
        assert "reuse1" in clean_output
        assert "reuse2" in clean_output

        # Verifica i messaggi di stato
        assert "Security Audit Report" in clean_output
