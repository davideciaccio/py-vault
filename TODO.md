#Py-Vault: Project Roadmap

This document tracks the development progress of the Py-Vault password manager. Each phase is designed to ensure maximum security and a professional developer experience.

## Phase 1: Security Foundation (Core)
- [x] **KDF Implementation**: Configure Argon2id for robust Master Password key derivation.
- [x] **Encryption Engine**: Implement AES-256-GCM for authenticated encryption at rest.
- [x] **Anti-Automation**: Implement typing speed monitoring logic (Anti-Rubber Ducky).
- [x] **Random Challenge**: Interactive human-verification system using random characters.
- [x] **Secure Storage**: Implement the encrypted SQLite database logic (`src/storage.py`).

## Phase 2: CLI & UX Development
- [x] **CLI Structure**: Build command hierarchy with `click` (init, add, get, list, audit).
- [x] **Banner & UI**: Integrate `rich` for ASCII banners, panels, and styled tables.
- [X] **Password Gen**: Cryptographically secure password generator with customizable parameters.
- [X] **Clipboard Management**: Secure copy system with an auto-clear timer (e.g., 30s).

## Phase 3: Advanced Features & Audit
- [x] **Security Audit**: Logic to scan the vault for weak or reused passwords.
- [x] **Import/Export**: Encrypted backup functionality and secure CSV import (with warnings).
- [x] **Vault Wipe**: Emergency command for instantaneous and secure local data destruction.

## Phase 4: Distribution & Documentation
- [x] **Project Structure**: Created `src/`, `tests/` folders and initialized Git repository.
- [x] **License**: MIT License selected and added to the project.
- [x] **README.md**: Professional introduction, OS-specific guides, and detailed **Usage** section.
- [X] **CONTRIBUTING.md**: Guidelines for Pull Requests and security vulnerability protocols.
- [x] **Install Scripts**: Finalize `install.sh` (Linux/macOS) and `install.ps1` (Windows).

## Phase 5: Maintenance & Repository Security
- [x] **Dependency Management**: Create `requirements.txt` and `requirements-dev.txt`.
- [x] **Modern Packaging**: Configure `pyproject.toml` (PEP 517 compliance).
- [x] **Pre-commit Hooks**: Setup hooks to prevent accidental commits of `.db` or `.env` files.
- [x] **Automated Updates**: Configure GitHub Dependabot for automated security patching.
- [x] **CI Pipeline**: Setup GitHub Actions for automated testing on every PR.
