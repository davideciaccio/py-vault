# PyVault Usage Guide

This guide covers the basic commands to get started with **PyVault**, your secure CLI credential manager.

---

type ```pyvault ``` or ```pyvault --help ``` to see the main tool functions.

### 1. Initialize the Vault (init)

Before storing any credentials, you must initialize your vault. This process sets up the local database and your **Master Password**.

> **Warning**: Do not lose your Master Password. It is the only key to decrypt your data; there is no "recovery" or "reset" option.

```bash
pyvault init
```

What happens:
- Creates the vault.db file in your project directory.
- Prompts you to set a Master Password.
- Generates a unique salt and a cryptographic verifier to secure the vault.

---

### 2. Adding Credentials (add)
The add command is used to store new service credentials. You will always be prompted for your Master Password to authorize the operation.

- Case A: Manual Password Entry

 Use this if you already have a password for a service and want to store it securely.

 ```bash
 pyvault add spotify --username mario.rossi
 ```

 Flow:
 Enter your Master Password.
 Enter the Spotify password when prompted.
 The credentials are encrypted and saved.

- Case B: Auto-Generate a Secure Password

 Use the --gen flag to let PyVault create a strong, random password for you.

 ```bash
 pyvault add github --username dev_user --gen
 ```

 Flow:Enter your Master Password.
 PyVault generates a 20-character random password (default).
 The password is displayed once and saved securely.

- Case C: Custom Length Generated Password

 If a service requires a specific password length, use the --length option.

 ```bash
 pyvault add bank_account --username user123 --gen --length 32
 ```

 Result: Generates and saves a 32-character high-entropy password.

---

### 3. Retrieving Credentials (get)
 The get command retrieves and decrypts your stored secrets. For security, the decryption happens only in memory.

- Case A: View in Terminal

 This displays your username and password directly in the console.

 ```bash
 pyvault get google
 ```

- Case B: Copy to Clipboard

 Use the --copy flag to send the password to your clipboard without displaying it on screen.

 ```bash
 pyvault get google --copy
 ```

 Security Note: When using --copy, PyVault starts a background process that automatically clears your clipboard after 30 seconds to prevent accidental exposure.

---

### 4. Listing Stored Services (list)

 The list command provides an organized overview of all services currently stored in your vault. This is useful for auditing your accounts without exposing sensitive passwords.

 ```bash
  pyvault list
  ```
 - Details:

   - Authentication: Requires your Master Password to access the database metadata.

   - Security: For your protection, this command never displays passwords. It only shows service names and usernames.

 - UI: Displays a professionally formatted table using the rich library, including a security banner.

 Example Output: After successful authentication, you will see a table like this:


(![pyvault list -> table](images/pyvault_list_commad.png))

---

### 5. Removing Credentials (rm)
 The rm command allows you to permanently delete a service and its credentials from the vault. This action is irreversible.

 ```bash
 pyvault rm SERVICE
 ```
 - Workflow:

    - Authorization: You must enter your Master Password.

    - Verification: The system checks if the service exists.

    - Confirmation: You will be asked "Are you sure?". You must explicitly confirm (Y/n) to proceed.

 - Example:

 ```bash
 pyvault rm old_bank_account
 ```
---

## 6. Security Audit (audit)
The audit command is a professional-grade tool designed to analyze your password hygiene without ever compromising your secrets. It identifies potential vulnerabilities in your vault using a "Zero-Knowledge" approach.

```bash
pyvault audit
```

### Key Analysis Features:
* **Password Reuse Detection**: Identifies if the same password is used for multiple services, preventing "credential stuffing" attacks.
* **Strength Analysis**: Flags any password shorter than **12 characters** as high risk.
* **Visual Reporting**: Generates a color-coded security report:
    * High-risk vulnerabilities that need immediate action.
    * Reuse warnings for better organization.
    * Confirmation of excellent password hygiene.

---

## 7. Emergency Vault Wipe (wipe)
The **wipe** command acts as a "panic button" for your security. It is designed to instantaneously and permanently destroy the local database file (`vault.db`).

```bash
pyvault wipe
```

### ⚠ Irreversible Action
This operation is **final**. Once the vault is wiped, all stored credentials, salts, and metadata are physically deleted from the disk and cannot be recovered by any means.

### Protection Layers:
To prevent accidental data loss, the command requires passing through three distinct security layers:
1.  **Explicit Confirmation**: A preliminary "Are you sure?" prompt.
2.  **Identity Verification**: You must enter your Master Password to authorize the destruction.
3.  **Human Verification**: A 6-character dynamic alphanumeric challenge (e.g., `XJ92L1`) must be solved to confirm the action.

---

## 8. Migration and Backup (Import/Export)
These commands allow you to move your data safely between different platforms or create local backups.

### 8.1 Formatting External Data (`formatter`)
If you are migrating from **Chrome**, **Edge**, or **Bitwarden**, you must first format your raw CSV file into a PyVault-compatible structure.

**Command:**
`pyvault formatter FILE_PATH DEST_PATH NEW_FILE_NAME`

> **Note:** You can use shortcuts like `~/Downloads` for the paths.
> **Warning:** If your file names or paths contain **spaces**, you must wrap the path in quotes (e.g., `"~/Downloads/My Passwords.csv"`) or rename the file without spaces to avoid recognition issues.

### 8.2 Importing Data (`import`)
Once you have a PyVault-formatted CSV, you can load it into your vault. Duplicate services will be skipped automatically.

**Command:**
`pyvault import FILE_PATH`

### 8.3 Exporting Your Vault (`export`)
Extracts your credentials, decrypts them, and saves them to a file.

**Command:**
`pyvault export DEST_PATH NEW_FILE_NAME [OPTIONS]`

**Options:**
* `--format [csv|json]`: Choose output format (Default: CSV).

> [!CAUTION]
> **SECURITY WARNING:** Exported files are stored in **PLAIN TEXT**. Ensure the destination path (e.g., `~/Documents/Backups`) is secure and delete the file immediately after use.
