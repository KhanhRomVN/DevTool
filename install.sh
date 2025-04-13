#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}DTL (Developer Tool) Installation${NC}"
echo "--------------------------------"

# Check for python3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    exit 1
fi

# Install pipx if not present
if ! command -v pipx &> /dev/null; then
    echo "Installing pipx..."
    sudo apt-get update
    sudo apt-get install -y pipx
    pipx ensurepath
fi

# Clean up all possible existing installations
echo "Cleaning up any existing installations..."

# Remove from /usr/local/bin (requires sudo)
if [ -f "/usr/local/bin/dtl" ]; then
    echo "Removing from /usr/local/bin..."
    sudo rm "/usr/local/bin/dtl"
fi

# Remove from ~/.local/bin
if [ -L "$HOME/.local/bin/dtl" ]; then
    echo "Removing from ~/.local/bin..."
    rm "$HOME/.local/bin/dtl"
fi

# Remove any existing pipx installation
if pipx list | grep -q "dtl"; then
    echo "Removing existing pipx installation..."
    pipx uninstall dtl
fi

# Always remove old configuration to force fresh setup
CONFIG_DIR="$HOME/.config/dtl"
if [ -d "$CONFIG_DIR" ]; then
    echo "Removing old configuration..."
    rm -rf "$CONFIG_DIR"
fi

# Install the package using pipx
echo "Installing dtl..."
pipx install .

echo -e "\n${GREEN}Installation completed successfully!${NC}"
echo -e "You can now use the 'dtl' command to manage your development tasks."
echo -e "\nAvailable commands:"
echo "  dtl help              # Show help message"
echo "  dtl config           # Configure settings"
echo "  dtl auto-commit      # Generate commit message and handle git operations"
echo -e "\nAuto-commit options:"
echo "  --no-push           # Skip automatic push"
echo "  --no-review         # Skip code review"
echo -e "\nNote: The first time you run the command, you'll be prompted for your Gemini API key."

# Ensure PATH is updated
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo -e "\n${BLUE}Adding ~/.local/bin to PATH...${NC}"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    export PATH="$HOME/.local/bin:$PATH"
fi

# Final verification
echo -e "\n${BLUE}Verifying installation...${NC}"
if command -v dtl &> /dev/null; then
    echo -e "${GREEN}dtl is successfully installed and available in your PATH${NC}"
    which dtl
    
    # Verify configuration directory is clean
    if [ -d "$CONFIG_DIR" ]; then
        echo -e "${RED}Warning: Old configuration found. It will be cleared on first run.${NC}"
    else
        echo -e "${GREEN}Clean installation - you will be prompted for configuration on first run.${NC}"
    fi
else
    echo -e "${RED}Warning: dtl command not found in PATH. Please run:${NC}"
    echo "source ~/.bashrc"
    echo "or open a new terminal"
fi