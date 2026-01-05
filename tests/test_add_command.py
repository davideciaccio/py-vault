import pytest
from click.testing import CliRunner
from unittest.mock import patch

# Importiamo il comando dal tuo pacchetto
from pyvault.main import add


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_vault_deps():
    """Mock delle dipendenze puntando al percorso corretto: pyvault.main"""
    with patch("pyvault.main.VaultStorage") as mock_storage, patch(
        "pyvault.main.CryptoManager"
    ) as mock_crypto, patch("pyvault.main.os.path.exists") as mock_exists, patch(
        "pyvault.main.SecurityProtections.check_input_speed"
    ) as mock_speed:
        mock_exists.return_value = True
        mock_speed.return_value = True

        yield {
            "storage": mock_storage.return_value,
            "crypto": mock_crypto.return_value,
            "exists": mock_exists,
        }


# 1. Test Successo: Aggiunta manuale
@patch("questionary.password")
def test_add_manual_success(mock_password, runner, mock_vault_deps):
    mock_password.return_value.ask.side_effect = ["master_correct", "service_secret"]
    mock_vault_deps["storage"].get_master_salt.return_value = b"salt"
    mock_vault_deps["storage"].get_verifier.return_value = b"verifier"
    mock_vault_deps["crypto"].derive_key.return_value = b"key"

    result = runner.invoke(add, ["google", "--username", "mario"])

    assert result.exit_code == 0
    assert "Credentials for google saved successfully!" in result.output


# 2. Test Successo: Generazione automatica (--gen)
@patch("questionary.password")
def test_add_generated_success(mock_password, runner, mock_vault_deps):
    mock_password.return_value.ask.return_value = "master_correct"
    mock_vault_deps["crypto"].decrypt.return_value = None

    result = runner.invoke(
        add, ["github", "--username", "mario", "--gen", "--length", "15"]
    )

    assert result.exit_code == 0
    assert "Generated password:" in result.output


# 3. TEST MANCANTE - Fallimento: Password Master Errata
@patch("questionary.password")
def test_add_wrong_master_password(mock_password, runner, mock_vault_deps):
    mock_password.return_value.ask.return_value = "wrong_password"

    # Simuliamo il fallimento della decifratura (eccezione)
    mock_vault_deps["crypto"].decrypt.side_effect = Exception("Decryption failed")

    result = runner.invoke(add, ["test_service", "--username", "user"])

    # Deve stampare ACCESS DENIED e NON deve salvare nulla
    assert "ACCESS DENIED" in result.output
    mock_vault_deps["storage"].add_credential.assert_not_called()
