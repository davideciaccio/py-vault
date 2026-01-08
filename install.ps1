Write-Host "--- Py-vault Installation Started ---" -foregroundColor Cyan

if (!(Get-Command python -ErrorAction SilentlyContinue)) {
	Write-Host "Error: Python is not installed or not in PATH." -ForegroundColor Red
	exit
}

Write-Host "Setting up virtual enviroment..."
python -m venv venv
$VENV_PATH = "$PSScriptRoot\venv\Scripts\Activate.ps1"

Write-Host "installing requirements and package..."
& python -m pip install --upgrade pip
& .\venv\Scripts\pip install -r requirements.txt
& .\venv\Scripts\pip install -e .

Write-Host ""
Write-Host "Installation Finished Successfully" -ForegroundColor Green
Write-Host "------------------------------------------"
Write-Host "To use pyvault from this terminal,run:"
Write-Host ".\venv\Scripts\activate" -ForegroundColor Cyan
Write-Host ""
Write-Host "To make pyvault a global command on Windows:"
Write-Host "1. Open the Start Menu, search Enviroments Variables"
Write-Host "2. Edit your PATH variable"
Write-Host "3. Add this folder: $PSScriptRoot\venv\Scripts" -ForegroundColor Yellow
Write-Host "------------------------------------------"
