# 🛡️ Py-Vault

**Py-Vault** is a professional-grade, zero-knowledge CLI password manager built with Python. It is designed for users who prioritize extreme privacy and require defense against modern attack vectors, including HID injection (Rubber Ducky) and automated keylogging.

---

## 🚀 Key Features

* **Zero-Knowledge Architecture**: Your master password and salt never leave your local machine.
* **Military-Grade Encryption**: Powered by **AES-256-GCM** for authenticated encryption and **Argon2id** for robust key derivation.
* **Active Defense**:
    * **Anti-HID Injection**: Real-time typing speed analysis to block automated hardware attacks.
    * **Random Challenges**: Interactive verification steps to disrupt pre-programmed scripts.
* **Professional CLI**: Built with `click` and `rich` for a beautiful, intuitive, and colored terminal experience.
* **Cross-Platform**: Seamlessly runs on Linux, macOS, and Windows.

---

## 🛠️ Security Architecture

Py-Vault doesn't just hide your data; it makes it mathematically inaccessible.

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **KDF** | Argon2id | Protects against brute-force and GPU-accelerated attacks. |
| **Encryption** | AES-256-GCM | Ensures data confidentiality and tamper-proof integrity. |
| **Storage** | Encrypted SQLite | ACID-compliant, high-performance local storage. |
| **Layout** | **Src-Layout** | Ensures clean dependency management and secure module isolation. |



---

## 📦 Installation Guide

To avoid path conflicts and ensure all security modules are correctly resolved, Py-Vault must be installed in **editable mode** within a virtual environment.

### 🐧 Linux & 🍎 macOS

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/davideciaccio/py-vault.git
    cd py-vault
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the package**:
    The `-e` (editable) flag is **mandatory** to register the `pyvault` command and resolve internal module paths correctly:
    ```bash
    pip install -e .
    ```

4.  **Verify the installation**:
    ```bash
    pyvault --version
    ```

### 🪟 Windows - powershell

1.  **Clone the repository**:
    ```powershell
    git clone https://github.com/davideciaccio/py-vault.git
    cd py-vault
    ```

2.  **Setup Environment**:
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install**:
    ```powershell
    pip install -e .
    ```

---

📄 License
Distributed under the MIT License. See LICENSE for more information.

---

⚠️ Disclaimer
This tool is provided "as is" for educational and personal use. While it implements industry-standard cryptographic practices, the security of your data ultimately depends on the strength and secrecy of your Master Password.

---

Created with passion by davideciaccio
