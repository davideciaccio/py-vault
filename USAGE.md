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
