#!/bin/bash

# Dev Tool - Auto Update Checker
# This script checks for updates when any dev_tool command is run

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
WHITE='\033[1;37m'
BOLD='\033[1m'
DIM='\033[2m'
UNDERLINE='\033[4m'
RESET='\033[0m'

# Tool information
TOOL_NAME="dev_tool"
REPO_URL="https://github.com/KhanhRomVN/dev_tool"
VERSION_URL="https://raw.githubusercontent.com/KhanhRomVN/dev_tool/main/VERSION"
INSTALL_SCRIPT_URL="https://raw.githubusercontent.com/KhanhRomVN/dev_tool/main/install.sh"

# Get current version
get_current_version() {
    if command -v "$TOOL_NAME" >/dev/null 2>&1; then
        "$TOOL_NAME" --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "unknown"
    else
        echo "unknown"
    fi
}

# Get latest version from GitHub
get_latest_version() {
    local latest_version
    if command -v curl >/dev/null 2>&1; then
        latest_version=$(curl -fsSL "$VERSION_URL" 2>/dev/null || echo "")
    elif command -v wget >/dev/null 2>&1; then
        latest_version=$(wget -qO- "$VERSION_URL" 2>/dev/null || echo "")
    fi
    
    if [ -z "$latest_version" ]; then
        echo "error"
    else
        echo "$latest_version"
    fi
}

# Compare version numbers
version_compare() {
    if [ "$1" = "$2" ]; then
        echo "equal"
    elif [ "$(printf '%s\n' "$1" "$2" | sort -V | head -n1)" = "$1" ]; then
        echo "older"
    else
        echo "newer"
    fi
}

# Check for updates
check_for_updates() {
    local current_version=$(get_current_version)
    local latest_version=$(get_latest_version)
    
    if [ "$latest_version" = "error" ]; then
        return 1
    fi
    
    if [ "$current_version" = "unknown" ]; then
        return 1
    fi
    
    local comparison=$(version_compare "$current_version" "$latest_version")
    
    if [ "$comparison" = "older" ]; then
        echo "$latest_version"
    else
        echo ""
    fi
}

# Prompt user for update
prompt_update() {
    local latest_version="$1"
    local current_version=$(get_current_version)
    
    echo -e "${YELLOW}${BOLD}🔄 Update Available!${RESET}"
    echo -e "${WHITE}Current version: ${current_version}${RESET}"
    echo -e "${WHITE}Latest version:  ${latest_version}${RESET}"
    echo ""
    echo -e "${CYAN}Would you like to update now? (y/N): ${RESET}"
    
    read -r response
    case "$response" in
        [yY][eE][sS]|[yY])
            echo -e "${GREEN}Updating to version ${latest_version}...${RESET}"
            
            # Download and run install script
            if command -v curl >/dev/null 2>&1; then
                curl -fsSL "$INSTALL_SCRIPT_URL" | bash -s -- --update
            elif command -v wget >/dev/null 2>&1; then
                wget -qO- "$INSTALL_SCRIPT_URL" | bash -s -- --update
            else
                echo -e "${RED}Error: Neither curl nor wget found. Please update manually.${RESET}"
                return 1
            fi
            ;;
        *)
            echo -e "${BLUE}Skipping update. You can update later by running:${RESET}"
            echo -e "${WHITE}curl -fsSL $INSTALL_SCRIPT_URL | bash${RESET}"
            ;;
    esac
}

# Main function
main() {
    # Only check for updates once per day
    local last_check_file="$HOME/.dev_tool_last_update_check"
    local now=$(date +%s)
    local last_check=0
    
    if [ -f "$last_check_file" ]; then
        last_check=$(cat "$last_check_file")
    fi
    
    # Check if it's been more than 24 hours since last check
    if [ $((now - last_check)) -lt 86400 ]; then
        return 0
    fi
    
    # Write current time to file
    echo "$now" > "$last_check_file"
    
    # Check for updates
    local latest_version=$(check_for_updates)
    
    if [ -n "$latest_version" ]; then
        prompt_update "$latest_version"
    fi
}

# Run only if not in update mode
if [ "$1" != "--silent" ]; then
    main
fi