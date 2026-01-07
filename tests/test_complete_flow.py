import pytest
import os
import re
from click.testing import CliRunner
from unittest.mock import patch
from pyvault.main import cli


# Helper per pulire l'output dai codici colore di Rich
def strip_ansi(text):
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture(autouse=True)
def cleanup():
    """Assicura che il database non esista prima e dopo il test."""
    if os.path.exists("vault.db"):
        os.remove("vault.db")
    yield
    if os.path.exists("vault.db"):
        os.remove("vault.db")


@patch("questionary.password")
@patch("questionary.confirm")
@patch("pyvault.protections.SecurityProtections.check_input_speed")
@patch("pyvault.protections.SecurityProtections.random_confirmation_challenge")
def test_full_application_flow(
    mock_challenge, mock_speed, mock_confirm, mock_password, runner
):
    # Setup Mocks
    mock_speed.return_value = True
    mock_challenge.return_value = True

    # IMPORTANTE: Ogni chiamata a questionary.password(...).ask() consuma un elemento.
    mock_password.return_value.ask.side_effect = [
        "Master123!",  # 1. init (Master Pwd)
        "Master123!",  # 2. add google (Master Pwd)
        "password_segreta",  # 3. add google (Service Pwd - Manuale)
        "Master123!",  # 4. add github (Master Pwd)
        "Master123!",  # 5. list (Master Pwd)
        "Master123!",  # 6. get google (Master Pwd)
        "Master123!",  # 7. audit (Master Pwd)
        "Master123!",  # 8. rm google (Master Pwd)
        "Master123!",  # 9. list finale (Master Pwd)
    ]
    mock_confirm.return_value.ask.return_value = True

    # 1. TEST INIT
    result = runner.invoke(cli, ["init"])
    assert result.exit_code == 0
    assert "Success" in strip_ansi(result.output)

    # 2. TEST ADD (Manuale)
    # Rimosso input="password_segreta\n" perché usiamo il mock di questionary
    result = runner.invoke(cli, ["add", "google", "--username", "mario@gmail.com"])
    assert result.exit_code == 0
    assert "saved successfully" in strip_ansi(result.output)

    # 3. TEST ADD (Generato)
    result = runner.invoke(
        cli, ["add", "github", "--username", "mario_dev", "--gen", "--length", "24"]
    )
    assert result.exit_code == 0
    assert "Generated password" in strip_ansi(result.output)

    # 4. TEST LIST
    result = runner.invoke(cli, ["list"])
    clean_out = strip_ansi(result.output)
    assert result.exit_code == 0
    assert "google" in clean_out
    assert "github" in clean_out

    # 5. TEST GET
    result = runner.invoke(cli, ["get", "google"])
    clean_out = strip_ansi(result.output)
    assert result.exit_code == 0
    assert "mario@gmail.com" in clean_out
    assert "password_segreta" in clean_out

    # 6. TEST AUDIT
    result = runner.invoke(cli, ["audit"])
    clean_out = strip_ansi(result.output)
    assert result.exit_code == 0
    assert "Security Audit Report" in clean_out

    # 7. TEST RM
    result = runner.invoke(cli, ["rm", "google"])
    assert result.exit_code == 0
    assert "has been removed" in strip_ansi(result.output)

    # 8. VERIFICA FINALE
    result = runner.invoke(cli, ["list"])
    assert "google" not in strip_ansi(result.output)
