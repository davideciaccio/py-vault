# Py-Vault
**The Security Password Manager from the Command Line.**

Py-Vault is a professional-grade CLI password manager built for users who value privacy, speed, and technical transparency. It utilizes standard encryption protocols and anti-automation protections to keep your data secure.

![alt text](images/pyvault_v1.0.0.png)

---

## Table of Contents
1. [Key Features](#key-features)
2. [Security Architecture](#security-architecture)
3. [Getting Started](#getting-started)
   - [Clone the Repository](#clone-the-repository)
   - [Installation (Linux/macOS)](#installation-linux--macos)
   - [Installation (Windows)](#installation-windows)
4. [Quick Start Guide](#quick-start-guide)
5. [Advanced Tools](#advanced-tools)
   - [Data Migration](#data-migration)
   - [Security Audit](#security-audit)
   - [Emergency Wipe](#emergency-wipe)
6. [Contributing](#contributing)
7. [Disclaimer](#disclaimer)
8. [License](#license)

---

## Key Features
* **Zero-Knowledge Architecture:** Your Master Password is never stored; it is only used to derive encryption keys.
* **Strong Encryption:** AES-256-GCM authenticated encryption for all vault data.
* **Migration Toolkit:** Built-in formatter for Chrome, Edge, and Bitwarden exports.
* **Security Audit:** Automated checks for weak, short, or reused passwords.
* **Anti-Automation:** Typing speed analysis (Anti-Ducky) and interactive human verification.
* **Emergency Wipe:** Instant, secure destruction of the local vault in case of compromise.

---

## Security Architecture
Py-Vault implements a multi-layered defense strategy:

* **Key Derivation:** Uses **Argon2id**, the winner of the Password Hashing Competition, to derive a 256-bit key from your Master Password using a unique salt.
* **Data Encryption:** Employs **AES-256 in GCM mode**. This provides both confidentiality and **integrity**, ensuring that if the database is tampered with, the vault will refuse to decrypt.
* **Physical Security:** Includes a human-verification challenge to prevent automated "Brute Force" or "Rubber Ducky" script attacks.

---

## Getting Started

### Clone the Repository
First, clone the project to your local machine using Git:

```bash
git clone https://github.com/davideciaccio/py-vault.git
cd py-vault
```

### Installation (Linux & macOS)
The Linux installer sets up a virtual environment and creates a global wrapper in `/usr/local/bin`.

1.  **Grant execution permissions:**
```bash
chmod +x install.sh
```

2.  **Run the installer:**
```bash
./install.sh
```

3.  **Usage:** Open a new terminal and run `pyvault`.

### Installation (Windows)
First, clone the project to your local machine using Git:

```powershell
git clone https://github.com/davideciaccio/py-vault.git
cd py-vault
```
The Windows installer configures the environment and prepares the executable.

1.  **Open PowerShell as Administrator** in the project folder.
2.  **Run the installer:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\install.ps1
```

3.  **Global Access:** Add your `C:\path\to\py-vault\venv\Scripts` folder to your System Environment Variables (PATH).

---

## Quick Start Guide

**1. Initialize your Vault**
```bash
pyvault init
```

**2. Add a new credential**
```bash
pyvault add github --username dev_user
```

**3. Retrieve a password (auto-copies to clipboard for 30s)**
```bash
pyvault get github
```

**4. List all services**
```bash
pyvault list
```

---

## Advanced Tools

### Data Migration
Convert external exports into PyVault format and import them:

```bash
# 1. Format external CSV
pyvault formatter "~/Downloads/chrome_passwords.csv" ~/Desktop ready.csv

# 2. Import formatted file
pyvault import ~/Desktop/ready.csv
```

### Security Audit
Analyze your vault to identify security risks:

```bash
pyvault audit
```

### Emergency Wipe
Instantly destroy all local data and the database:

```bash
pyvault wipe
```

---

## Contributing
Contributions are welcome! Please read the `CONTRIBUTING.md` for guidelines on how to submit security-related patches.

---

## Disclaimer
This tool is provided "as is" for educational and personal use. While it implements standard cryptographic practices, the security of your data ultimately depends on the strength and secrecy of your Master Password.

---

## License
This project is licensed under the **MIT License**.

---

Created by davideciaccio
