import pytest
import os
from click.testing import CliRunner
from unittest.mock import patch
from pyvault.main import cli


@pytest.fixture
def runner():
    return CliRunner()


@patch("questionary.confirm")
@patch("questionary.password")
@patch("pyvault.protections.SecurityProtections.random_confirmation_challenge")
@patch("pyvault.protections.SecurityProtections.check_input_speed")
def test_vault_wipe_flow(
    mock_speed, mock_challenge, mock_password, mock_confirm, runner
):
    # Setup: crea un file dummy vault.db
    with open("vault.db", "w") as f:
        f.write("dummy data")

    mock_confirm.return_value.ask.return_value = True
    mock_password.return_value.ask.return_value = "master"
    mock_challenge.return_value = True
    mock_speed.return_value = True

    with patch("pyvault.main.VaultStorage"), patch(
        "pyvault.main.CryptoManager"
    ) as mock_crypto:
        # Simula verifica password corretta
        mock_crypto.return_value.decrypt.return_value = True

        result = runner.invoke(cli, ["wipe"])

        assert result.exit_code == 0
        assert "Vault successfully destroyed" in result.output
        assert not os.path.exists("vault.db")
