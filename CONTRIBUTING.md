# Contributing to Py-Vault 🛡️

First of all, thank you for showing interest in contributing to **Py-Vault**! Projects focused on security and privacy thrive on community audits and improvements.

By participating in this project, you agree to abide by its terms and professional standards.

## 🛠️ Development Workflow

### 1. Fork and Clone
Fork the repository on GitHub and clone it to your local machine:
```bash
git clone https://github.com/davideciaccio/py-vault.git
cd py-vault
```

---

### 2. Environment Setup
Always use a Virtual Environment to keep dependencies isolated:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For testing and linting
```

---

### 3. Branching Policy
Create a descriptive branch name for your changes:

For features: feature/your-feature-name

For bug fixes: fix/issue-description

For documentation: docs/what-changed

---

### 📏 Coding Standards
To maintain a professional codebase, we enforce the following:

Style Guide: Follow PEP 8.

Formatting: We use black for code formatting.

Linting: We use ruff or flake8 to catch potential errors.

Type Hinting: Use Python type hints (e.g., def derive_key(pwd: str) -> bytes:) for better maintainability.

---

### 🧪 Testing
Security software must be reliable.

All new features must include unit tests in the tests/directory.

We use pytest as our testing framework.

Ensure all tests pass before submitting a Pull Request.

---

### 📝 Commit Messages
We follow the Conventional Commits specification:

feat: for new features.

fix: for bug fixes.

docs: for documentation changes.

refactor: for code changes that neither fix a bug or add a feature.

---

### 🚀 Submission Process
Push your changes to your fork.

Submit a Pull Request (PR) to the main branch.

Provide a clear description of the changes and link any related issues.

Wait for the maintainer's review.

---

### ⚖️ License
By contributing, you agree that your contributions will be licensed under the project's MIT License.
