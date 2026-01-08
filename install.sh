#!/bin/bash

# Py-Vault Global Installer for Linux
# -----------------------------------

# Colors for UI
GREEN='\033[0;32m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}--- Py-Vault Installation Started ---${NC}"

# 1. Check for Python3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python3 is not installed.${NC}"
    exit 1
fi

# 2. Create Virtual Environment
echo -e "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies and the package
echo -e "Installing requirements and package..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

# 4. Create a global symlink (Requires sudo)
echo -e "${CYAN}To use 'pyvault' globally, a symlink will be created in /usr/local/bin.${NC}"
read -p "Do you want to create a global command? (y/n): " confirm

if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
    WRAPPER="/usr/local/bin/pyvault"
    PROJECT_DIR=$(pwd)

    sudo bash -c "cat << 'EOF' > $WRAPPER
#!/bin/bash
source $PROJECT_DIR/venv/bin/activate
python3 $PROJECT_DIR/src/pyvault/main.py \"\$@\"
EOF"

    sudo chmod +x $WRAPPER
    echo -e "${GREEN}✔ Global command 'pyvault' created!${NC}"
else
    echo -e "Skipping global command creation."
fi

echo -e "${GREEN}--- Installation Finished! ---${NC}"
echo -e "You can now run Py-Vault using: ${CYAN}pyvault --help${NC}"
