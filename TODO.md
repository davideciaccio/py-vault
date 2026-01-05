#Py-Vault: Project Roadmap

This document tracks the development progress of the Py-Vault password manager. Each phase is designed to ensure maximum security and a professional developer experience.

## Phase 1: Security Foundation (Core)
- [ ] **KDF Implementation**: Configure Argon2id for robust Master Password key derivation.
- [ ] **Encryption Engine**: Implement AES-256-GCM for authenticated encryption at rest.
- [ ] **Anti-Automation**: Implement typing speed monitoring logic (Anti-Rubber Ducky).
- [ ] **Random Challenge**: Interactive human-verification system using random characters.
- [ ] **Secure Storage**: Implement the encrypted SQLite database logic (`src/storage.py`).

## Phase 2: CLI & UX Development
- [ ] **CLI Structure**: Build command hierarchy with `click` (init, add, get, list, audit).
- [ ] **Banner & UI**: Integrate `rich` for ASCII banners, panels, and styled tables.
- [ ] **Password Gen**: Cryptographically secure password generator with customizable parameters.
- [ ] **Clipboard Management**: Secure copy system with an auto-clear timer (e.g., 30s).

## Phase 3: Advanced Features & Audit
- [ ] **Security Audit**: Logic to scan the vault for weak or reused passwords.
- [ ] **Import/Export**: Encrypted backup functionality and secure CSV import (with warnings).
- [ ] **Vault Wipe**: Emergency command for instantaneous and secure local data destruction.

## Phase 4: Distribution & Documentation
- [x] **Project Structure**: Created `src/`, `tests/` folders and initialized Git repository.
- [x] **License**: MIT License selected and added to the project.
- [ ] **README.md**: Professional introduction, OS-specific guides, and detailed **Usage** section.
- [ ] **CONTRIBUTING.md**: Guidelines for Pull Requests and security vulnerability protocols.
- [ ] **Install Scripts**: Finalize `install.sh` (Linux/macOS) and `install.ps1` (Windows).

## Phase 5: Maintenance & Repository Security
- [x] **Dependency Management**: Create `requirements.txt` and `requirements-dev.txt`.
- [x] **Modern Packaging**: Configure `pyproject.toml` (PEP 517 compliance).
- [x] **Pre-commit Hooks**: Setup hooks to prevent accidental commits of `.db` or `.env` files.
- [ ] **Automated Updates**: Configure GitHub Dependabot for automated security patching.
- [ ] **CI Pipeline**: Setup GitHub Actions for automated testing on every PR.
