import pytest
from click.testing import CliRunner
from unittest.mock import patch
from pyvault.main import get


@pytest.fixture
def runner():
    """Provides a CliRunner instance for testing Click commands."""
    return CliRunner()


@pytest.fixture
def mock_get_deps():
    """Mock dependencies for the get command in pyvault.main."""
    # We patch the classes directly in the main module to inject our mocks
    with patch("pyvault.main.VaultStorage") as mock_storage, patch(
        "pyvault.main.CryptoManager"
    ) as mock_crypto, patch("pyvault.main.os.path.exists") as mock_exists, patch(
        "pyvault.main.SecurityProtections.check_input_speed"
    ) as mock_speed, patch(
        "pyvault.main.pyperclip"
    ) as mock_pyperclip, patch(
        "pyvault.main.threading.Thread"
    ) as mock_thread:
        mock_exists.return_value = True
        mock_speed.return_value = True

        yield {
            "storage": mock_storage.return_value,
            "crypto": mock_crypto.return_value,
            "pyperclip": mock_pyperclip,
            "thread": mock_thread,
        }


# 1. Test Success: Display credentials in terminal (Tuple format)
@patch("questionary.password")
def test_get_success_display(mock_password, runner, mock_get_deps):
    mock_password.return_value.ask.return_value = "master_correct"

    # Mocking the database record as a TUPLE (username, password_blob)
    mock_get_deps["storage"].get_credential.return_value = (
        "mario_user",
        b"encrypted_data",
    )

    # Mock decryption: first call for verifier (None/Success), second for the secret
    mock_get_deps["crypto"].decrypt.side_effect = [None, "decrypted_password"]

    result = runner.invoke(get, ["google"])

    assert result.exit_code == 0
    assert "Username: mario_user" in result.output
    assert "Password: decrypted_password" in result.output
    mock_get_deps["pyperclip"].copy.assert_not_called()


# 2. Test Success: Copy password to clipboard and start thread
@patch("questionary.password")
def test_get_success_copy(mock_password, runner, mock_get_deps):
    mock_password.return_value.ask.return_value = "master_correct"

    # Return a tuple to match the main logic fix
    mock_get_deps["storage"].get_credential.return_value = (
        "mario_user",
        b"encrypted_data",
    )
    mock_get_deps["crypto"].decrypt.side_effect = [None, "decrypted_password"]

    result = runner.invoke(get, ["google", "--copy"])

    assert result.exit_code == 0
    assert "copied to clipboard" in result.output
    # Check if pyperclip was used to store the secret
    mock_get_deps["pyperclip"].copy.assert_called_with("decrypted_password")
    # Check if the background thread for clearing was initialized
    mock_get_deps["thread"].assert_called_once()


# 3. Test Failure: Service not found
@patch("questionary.password")
def test_get_service_not_found(mock_password, runner, mock_get_deps):
    mock_password.return_value.ask.return_value = "master_correct"

    # DB returns None if service is missing
    mock_get_deps["storage"].get_credential.return_value = None
    mock_get_deps["crypto"].decrypt.return_value = None

    result = runner.invoke(get, ["unknown_service"])

    assert "No credentials found" in result.output


# 4. Test Failure: Invalid Master Password
@patch("questionary.password")
def test_get_wrong_master_password(mock_password, runner, mock_get_deps):
    mock_password.return_value.ask.return_value = "wrong_pwd"

    # Simulate verifier decryption failure (wrong key)
    mock_get_deps["crypto"].decrypt.side_effect = Exception("Auth failed")

    result = runner.invoke(get, ["google"])

    assert "ACCESS DENIED" in result.output
    # Ensure no DB lookup happens if auth fails
    mock_get_deps["storage"].get_credential.assert_not_called()
