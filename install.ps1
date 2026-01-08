# Py-Vault Global Installer for Windows
# --------------------------------------

Write-Host "--- Py-Vault Installation Started ---" -ForegroundColor Cyan

# 1. Check for Python
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Python is not installed or not in PATH." -ForegroundColor Red
    exit
}

# 2. Create Virtual Environment
Write-Host "Setting up virtual environment..."
python -m venv venv
$VENV_PATH = "$PSScriptRoot\venv\Scripts\Activate.ps1"

# 3. Install dependencies and the package
Write-Host "Installing requirements and package..."
& python -m pip install --upgrade pip
& .\venv\Scripts\pip install -r requirements.txt
& .\venv\Scripts\pip install -e .

# 4. Instructions for Global Access
Write-Host ""
Write-Host "✔ Installation Finished Successfully!" -ForegroundColor Green
Write-Host "------------------------------------------------"
Write-Host "To use 'pyvault' from this terminal, run:"
Write-Host ".\venv\Scripts\activate" -ForegroundColor Cyan
Write-Host ""
Write-Host "To make 'pyvault' a global command on Windows:"
Write-Host "1. Open the Start Menu, search for 'Environment Variables'."
Write-Host "2. Edit your PATH variable."
Write-Host "3. Add this folder: $PSScriptRoot\venv\Scripts" -ForegroundColor Yellow
Write-Host "------------------------------------------------"