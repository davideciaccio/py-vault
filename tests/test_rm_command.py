import pytest
from click.testing import CliRunner
from unittest.mock import patch
from pyvault.main import rm


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_rm_deps():
    with patch("pyvault.main.VaultStorage") as mock_storage, patch(
        "pyvault.main.CryptoManager"
    ) as mock_crypto, patch("pyvault.main.os.path.exists") as mock_exists, patch(
        "pyvault.main.SecurityProtections.check_input_speed"
    ) as mock_speed:
        mock_exists.return_value = True
        mock_speed.return_value = True

        yield {"storage": mock_storage.return_value, "crypto": mock_crypto.return_value}


@patch("questionary.password")
@patch("questionary.confirm")
def test_rm_success(mock_confirm, mock_password, runner, mock_rm_deps):
    mock_password.return_value.ask.return_value = "correct_pwd"
    mock_confirm.return_value.ask.return_value = True

    # Mock finding the service and verifying password
    mock_rm_deps["storage"].get_credential.return_value = ("user", b"blob")
    mock_rm_deps["crypto"].decrypt.return_value = None  # Verifier success

    result = runner.invoke(rm, ["github"])

    assert "has been removed" in result.output
    mock_rm_deps["storage"].delete_credential.assert_called_once_with("github")


@patch("questionary.password")
@patch("questionary.confirm")
def test_rm_cancelled(mock_confirm, mock_password, runner, mock_rm_deps):
    mock_password.return_value.ask.return_value = "correct_pwd"
    mock_confirm.return_value.ask.return_value = False  # User says NO

    mock_rm_deps["storage"].get_credential.return_value = ("user", b"blob")
    mock_rm_deps["crypto"].decrypt.return_value = None

    result = runner.invoke(rm, ["github"])

    assert "Deletion cancelled" in result.output
    mock_rm_deps["storage"].delete_credential.assert_not_called()
