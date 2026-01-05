# Py-Vault 🛡️

**Py-Vault** is a professional-grade, zero-knowledge CLI password manager built with Python. It is designed for users who prioritize extreme privacy and require defense against modern attack vectors, including HID injection (Rubber Ducky) and automated keylogging.



---

## 🚀 Key Features

* **Zero-Knowledge Architecture**: Your master password and salt never leave your local machine.
* **Military-Grade Encryption**: Powered by **AES-256-GCM** for authenticated encryption and **Argon2id** for robust key derivation.
* **Active Defense**:
    * **Anti-HID Injection**: Real-time typing speed analysis to block automated hardware attacks.
    * **Random Challenges**: Interactive verification steps to disrupt pre-programmed scripts.
* **Cross-Platform**: Seamlessly runs on Linux, macOS, and Windows.
* **Developer-Friendly**: Built with `click` and `rich` for a beautiful, intuitive CLI experience.

---

## 🛠️ Security Architecture

Py-Vault doesn't just hide your data; it makes it mathematically inaccessible.

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **KDF** | Argon2id | Protects against brute-force and GPU-accelerated attacks. |
| **Encryption** | AES-256-GCM | Ensures data confidentiality and integrity (tamper-proof). |
| **Storage** | Encrypted SQLite | Provides ACID-compliant, high-performance local storage. |
| **Input** | Hidden Echo | Prevents "shoulder surfing" by masking all sensitive inputs. |

---

## 📦 Installation

### 🐧 Linux & 🍎 macOS
1. **Clone the repository**:
   ```bash
   git clone [https://github.com/davideciaccio/py-vault.git](https://github.com/davideciaccio/py-vault.git)
   cd py-vault
Run the installer:

Bash

chmod +x install.sh
./install.sh
Restart your terminal and type vault.

🪟 Windows
Clone the repository:

PowerShell

git clone [https://github.com/davideciaccio/py-vault.git](https://github.com/davideciaccio/py-vault.git)
cd py-vault
Run the installer (Run PowerShell as Admin):

PowerShell

Set-ExecutionPolicy Bypass -Scope Process -Force
.\install.ps1
💻 Usage
Py-Vault uses an intuitive command structure. Below are the primary actions:

Initialize the Vault
Create your secure database and set your Master Password.

Bash

pyvault init
Store Credentials
Add a new service. You can provide your own password or generate a secure one.

Bash

# Manual entry
pyvault add github

# Auto-generate a 32-character secure password
pyvault add google --gen --length 32
Retrieve Passwords
To protect against screen-scrapers, passwords are sent to the clipboard and cleared automatically.

Bash

# Copy to clipboard for 30 seconds
pyvault get github --copy
Security Audit
Analyze your vault for vulnerabilities like weak or reused passwords.

Bash

pyvault audit
🛡️ Anti-Automation Protection
Unlike standard password managers, Py-Vault monitors the entropy of input timing.

Human Verification: If a sequence of characters is entered with a delay of less than 50ms per keystroke (standard for Rubber Ducky devices), access is immediately revoked.

Interactive Confirmation: Critical operations require the user to type a randomized character displayed on the screen, breaking automated HID scripts.

📄 License
Distributed under the MIT License. See LICENSE for more information.

⚠️ Disclaimer
This tool is provided "as is" for educational and personal use. While it implements industry-standard cryptographic practices, always ensure your Master Password is long, unique, and securely stored.

Created with passion by davideciaccio
