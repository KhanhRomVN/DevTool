#!/bin/bash

# Dev Tool - AI-powered Git Commit Message Generator
# Cross-platform installer for Windows (WSL/Git Bash), Linux, and macOS

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Tool information
TOOL_NAME="dev_tool"
VERSION="2.0.2"
REPO_URL="https://github.com/KhanhRomVN/dev_tool"
BINARY_NAME="dev_tool"

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo -e "${CYAN}${BOLD}"
    echo "=================================================="
    echo "           🛠️  DEV TOOL 2.0 INSTALLER           "
    echo "        AI-Powered Git Assistant Setup          "
    echo "=================================================="
    echo -e "${NC}"
}

# Enhanced platform detection function
detect_platform() {
    local os=""
    local arch=""
    
    # Detect OS with better Windows detection
    case "$(uname -s)" in
        Linux*)     os="linux";;
        Darwin*)    os="darwin";;
        CYGWIN*|MINGW*|MSYS*)   os="windows";;
        *)          
            # Additional Windows detection
            if [[ -n "$WINDIR" ]] || [[ -n "$SYSTEMROOT" ]]; then
                os="windows"
            else
                print_error "Unsupported operating system: $(uname -s)"
                exit 1
            fi
            ;;
    esac
    
    # Detect architecture
    case "$(uname -m)" in
        x86_64|amd64)   arch="amd64";;
        arm64|aarch64)  arch="arm64";;
        armv6l)         arch="armv6";;
        armv7l)         arch="armv7";;
        i386|i686)      arch="386";;
        *)
            print_error "Unsupported architecture: $(uname -m)"
            exit 1
            ;;
    esac
    
    echo "${os}_${arch}"
}

# Enhanced function to detect if running on Windows
is_windows() {
    [[ "$(uname -s)" == CYGWIN* ]] || [[ "$(uname -s)" == MINGW* ]] || [[ "$(uname -s)" == MSYS* ]] || [[ -n "$WINDIR" ]]
}

# Enhanced function to get proper install directory
get_install_directory() {
    if [[ "$EUID" -eq 0 ]]; then
        # Root user - install system-wide
        echo "/usr/local/bin"
    else
        # Regular user - handle Windows vs Unix differently
        if is_windows; then
            # Windows: Use USERPROFILE if available, otherwise HOME
            local user_bin=""
            if [[ -n "$USERPROFILE" ]]; then
                # Convert Windows path to Unix format for Git Bash
                user_bin="$(cygpath -u "$USERPROFILE" 2>/dev/null || echo "$USERPROFILE")/.local/bin"
            else
                user_bin="$HOME/.local/bin"
            fi
            
            # Ensure directory exists
            mkdir -p "$user_bin"
            echo "$user_bin"
        else
            # Unix-like systems
            if [[ -d "$HOME/.local/bin" ]]; then
                echo "$HOME/.local/bin"
            else
                mkdir -p "$HOME/.local/bin"
                echo "$HOME/.local/bin"
            fi
        fi
    fi
}

# Enhanced function to add directory to PATH
add_to_path() {
    local install_dir="$1"
    local shell_profile=""
    local path_export=""
    
    # Determine shell profile
    if [[ -n "$BASH_VERSION" ]]; then
        if is_windows; then
            # On Windows Git Bash, prefer .bash_profile over .bashrc
            if [[ -f "$HOME/.bash_profile" ]]; then
                shell_profile="$HOME/.bash_profile"
            else
                shell_profile="$HOME/.bashrc"
            fi
        else
            shell_profile="$HOME/.bashrc"
        fi
    elif [[ -n "$ZSH_VERSION" ]]; then
        shell_profile="$HOME/.zshrc"
    else
        shell_profile="$HOME/.profile"
    fi
    
    # Prepare PATH export statement
    if is_windows; then
        # On Windows, normalize the path and ensure proper format
        local normalized_dir="$install_dir"
        # Convert to Unix format if needed
        if [[ "$install_dir" == *":"* ]]; then
            normalized_dir="$(cygpath -u "$install_dir" 2>/dev/null || echo "$install_dir")"
        fi
        path_export="export PATH=\"${normalized_dir}:\$PATH\""
    else
        path_export="export PATH=\"${install_dir}:\$PATH\""
    fi
    
    # Check if already in PATH config
    local path_pattern=""
    if is_windows; then
        path_pattern="\.local/bin"
    else
        path_pattern="\.local/bin"
    fi
    
    if ! grep -q "export PATH.*${path_pattern}" "$shell_profile" 2>/dev/null; then
        echo "" >> "$shell_profile"
        echo "# Local binaries" >> "$shell_profile"
        echo "$path_export" >> "$shell_profile"
        print_success "Added $install_dir to PATH in $shell_profile"
        
        # Also add to current session
        export PATH="$install_dir:$PATH"
        
        # On Windows, also try to add to current session with different formats
        if is_windows; then
            # Try multiple path formats to ensure compatibility
            export PATH="$install_dir:$PATH"
            if [[ -n "$USERPROFILE" ]]; then
                local win_path="$(cygpath -w "$install_dir" 2>/dev/null || echo "$install_dir")"
                export PATH="$install_dir:$PATH"
            fi
        fi
    else
        print_info "PATH already configured in $shell_profile"
        # Still add to current session
        export PATH="$install_dir:$PATH"
    fi
}

# Function to read input safely (works with piped scripts)
read_input() {
    local prompt="$1"
    local default="$2"
    local input=""
    
    # Try to read from /dev/tty if available (better for piped scripts)
    if [ -t 0 ]; then
        # stdin is a terminal
        read -p "$prompt" input
    elif [ -r /dev/tty ]; then
        # stdin is not a terminal but /dev/tty is available
        read -p "$prompt" input < /dev/tty
    else
        # Fallback: assume default
        print_warning "Cannot read input, using default: $default"
        input="$default"
    fi
    
    echo "$input"
}

# Function to compare versions (returns 0 if equal, 1 if v1 > v2, 2 if v1 < v2)
compare_versions() {
    local v1="$1"
    local v2="$2"
    
    # Remove 'v' prefix if exists
    v1=$(echo "$v1" | sed 's/^v//')
    v2=$(echo "$v2" | sed 's/^v//')
    
    if [[ "$v1" == "$v2" ]]; then
        return 0  # Equal
    fi
    
    # Split versions into arrays
    IFS='.' read -ra V1 <<< "$v1"
    IFS='.' read -ra V2 <<< "$v2"
    
    # Pad arrays to same length
    local max_len=$(( ${#V1[@]} > ${#V2[@]} ? ${#V1[@]} : ${#V2[@]} ))
    
    for (( i=0; i<max_len; i++ )); do
        local n1=${V1[i]:-0}
        local n2=${V2[i]:-0}
        
        if (( n1 > n2 )); then
            return 1  # v1 > v2
        elif (( n1 < n2 )); then
            return 2  # v1 < v2
        fi
    done
    
    return 0  # Equal
}

# Get version status string
get_version_status() {
    local current_version="$1"
    local latest_version="$2"
    
    compare_versions "$current_version" "$latest_version"
    local result=$?
    
    case $result in
        0) echo "same version" ;;
        1) echo "newer version" ;;
        2) echo "older version" ;;
    esac
}

# Check if Go is installed
check_go_installation() {
    if command -v go >/dev/null 2>&1; then
        local go_version=$(go version | awk '{print $3}' | sed 's/go//')
        print_success "Go found: version $go_version"
        return 0
    else
        print_warning "Go is not installed on this system"
        return 1
    fi
}

# Install Go (if needed and user agrees)
install_go() {
    print_info "Go is required to build the tool from source."
    print_info "You have three options:"
    echo -e "${CYAN}  1.${NC} Install Go automatically (recommended)"
    echo -e "${CYAN}  2.${NC} Install Go manually and run this script again"
    echo -e "${CYAN}  3.${NC} Download pre-built binary (if available)"
    echo ""
    
    local choice=$(read_input "Choose option (1/2/3) [1]: " "1")
    
    case $choice in
        1|"")
            print_info "Installing Go..."
            install_go_automatically
            ;;
        2)
            print_info "Please install Go from https://golang.org/dl/"
            print_info "Then run this script again."
            exit 0
            ;;
        3)
            print_info "Attempting to download pre-built binary..."
            download_prebuilt_binary
            ;;
        *)
            print_warning "Invalid choice, defaulting to option 1"
            install_go_automatically
            ;;
    esac
}

# Install Go automatically
install_go_automatically() {
    local platform=$(detect_platform)
    local go_version="1.21.5"
    
    case $platform in
        linux_amd64)
            local go_tar="go${go_version}.linux-amd64.tar.gz"
            ;;
        linux_arm64)
            local go_tar="go${go_version}.linux-arm64.tar.gz"
            ;;
        darwin_amd64)
            local go_tar="go${go_version}.darwin-amd64.tar.gz"
            ;;
        darwin_arm64)
            local go_tar="go${go_version}.darwin-arm64.tar.gz"
            ;;
        windows_amd64)
            local go_tar="go${go_version}.windows-amd64.zip"
            ;;
        *)
            print_error "Automatic Go installation not supported for platform: $platform"
            print_info "Please install Go manually from https://golang.org/dl/"
            exit 1
            ;;
    esac
    
    local temp_dir=$(mktemp -d)
    local download_url="https://golang.org/dl/${go_tar}"
    
    print_info "Downloading Go ${go_version}..."
    
    if command -v curl >/dev/null 2>&1; then
        curl -L "$download_url" -o "${temp_dir}/${go_tar}"
    elif command -v wget >/dev/null 2>&1; then
        wget "$download_url" -O "${temp_dir}/${go_tar}"
    else
        print_error "Neither curl nor wget found. Cannot download Go."
        exit 1
    fi
    
    # Install Go - enhanced for Windows
    local install_dir=""
    if [[ "$EUID" -ne 0 ]]; then
        if is_windows && [[ -n "$USERPROFILE" ]]; then
            # Use USERPROFILE on Windows
            install_dir="$(cygpath -u "$USERPROFILE" 2>/dev/null || echo "$USERPROFILE")/.local"
        else
            install_dir="$HOME/.local"
        fi
        mkdir -p "$install_dir"
    else
        install_dir="/usr/local"
    fi
    
    print_info "Installing Go to ${install_dir}..."
    
    # Remove existing Go installation
    if [[ -d "${install_dir}/go" ]]; then
        rm -rf "${install_dir}/go"
    fi
    
    # Extract Go
    if [[ "$go_tar" == *.zip ]]; then
        unzip "${temp_dir}/${go_tar}" -d "$install_dir"
    else
        tar -xzf "${temp_dir}/${go_tar}" -C "$install_dir"
    fi
    
    # Add Go to PATH
    local go_bin="${install_dir}/go/bin"
    export PATH="$go_bin:$PATH"
    
    # Add to shell profile with Windows compatibility
    add_go_to_path "$go_bin"
    
    # Clean up
    rm -rf "$temp_dir"
    
    # Verify installation
    if command -v go >/dev/null 2>&1; then
        print_success "Go installed successfully: $(go version)"
    else
        print_error "Go installation failed"
        exit 1
    fi
}

# Enhanced function to add Go to PATH
add_go_to_path() {
    local go_bin="$1"
    local shell_profile=""
    
    if [[ -n "$BASH_VERSION" ]]; then
        if is_windows; then
            shell_profile="$HOME/.bash_profile"
            [[ ! -f "$shell_profile" ]] && shell_profile="$HOME/.bashrc"
        else
            shell_profile="$HOME/.bashrc"
        fi
    elif [[ -n "$ZSH_VERSION" ]]; then
        shell_profile="$HOME/.zshrc"
    else
        shell_profile="$HOME/.profile"
    fi
    
    if ! grep -q "export PATH.*go/bin" "$shell_profile" 2>/dev/null; then
        echo "" >> "$shell_profile"
        echo "# Go" >> "$shell_profile"
        if is_windows; then
            # Normalize path for Windows
            local normalized_go_bin="$go_bin"
            echo "export PATH=\"${normalized_go_bin}:\$PATH\"" >> "$shell_profile"
        else
            echo "export PATH=\"${go_bin}:\$PATH\"" >> "$shell_profile"
        fi
        print_success "Added Go to PATH in $shell_profile"
    fi
}

# Download pre-built binary (if available)
download_prebuilt_binary() {
    local platform=$(detect_platform)
    local binary_url="${REPO_URL}/releases/download/v${VERSION}/${BINARY_NAME}_${VERSION}_${platform}"
    
    if [[ "$platform" == *"windows"* ]]; then
        binary_url="${binary_url}.exe"
    fi
    
    local temp_dir=$(mktemp -d)
    local binary_path="${temp_dir}/${BINARY_NAME}"
    if [[ "$platform" == *"windows"* ]]; then
        binary_path="${binary_path}.exe"
    fi
    
    print_info "Downloading pre-built binary for $platform..."
    
    # Try to download binary
    if command -v curl >/dev/null 2>&1; then
        if curl -L --fail "$binary_url" -o "$binary_path" 2>/dev/null; then
            install_binary "$binary_path"
            return 0
        fi
    elif command -v wget >/dev/null 2>&1; then
        if wget "$binary_url" -O "$binary_path" 2>/dev/null; then
            install_binary "$binary_path"
            return 0
        fi
    fi
    
    print_warning "Pre-built binary not available for $platform"
    print_info "Falling back to building from source..."
    
    if ! check_go_installation; then
        install_go
    fi
    
    build_from_source
}

# Build from source
build_from_source() {
    print_info "Building $TOOL_NAME from source..."
    
    local temp_dir=$(mktemp -d)
    cd "$temp_dir"
    
    # Clone repository
    if command -v git >/dev/null 2>&1; then
        print_info "Cloning repository..."
        git clone "$REPO_URL" .
    else
        print_error "Git is not installed. Please install Git first."
        exit 1
    fi
    
    # Build the tool
    print_info "Building binary..."
    go mod tidy
    
    # Build with appropriate extension for Windows
    local binary_name="$BINARY_NAME"
    if is_windows; then
        binary_name="${BINARY_NAME}.exe"
    fi
    
    go build -o "$binary_name" .
    
    # Install binary
    install_binary "./${binary_name}"
    
    # Clean up
    cd /
    rm -rf "$temp_dir"
}

# Enhanced install binary function
install_binary() {
    local binary_path="$1"
    local install_dir=$(get_install_directory)
    
    # Make binary executable
    chmod +x "$binary_path"
    
    print_info "Installing to $install_dir..."
    
    # Determine final binary name
    local final_binary_name="$BINARY_NAME"
    if is_windows && [[ "$binary_path" == *.exe ]]; then
        final_binary_name="${BINARY_NAME}.exe"
    fi
    
    # Copy binary
    cp "$binary_path" "${install_dir}/${final_binary_name}"
    
    # Add to PATH
    add_to_path "$install_dir"
    
    # Verify installation with multiple attempts
    local verification_attempts=3
    local verified=false
    
    for ((i=1; i<=verification_attempts; i++)); do
        # Try different command formats
        if command -v "$BINARY_NAME" >/dev/null 2>&1 || \
           command -v "${install_dir}/${BINARY_NAME}" >/dev/null 2>&1 || \
           (is_windows && command -v "${BINARY_NAME}.exe" >/dev/null 2>&1); then
            verified=true
            break
        fi
        
        if [[ $i -lt $verification_attempts ]]; then
            print_info "Verification attempt $i failed, retrying..."
            sleep 1
            # Re-export PATH
            export PATH="$install_dir:$PATH"
        fi
    done
    
    if $verified; then
        print_success "$TOOL_NAME installed successfully!"
        print_info "Installation location: ${install_dir}/${final_binary_name}"
    else
        print_warning "Installation completed but verification failed"
        print_info "Binary installed to: ${install_dir}/${final_binary_name}"
        print_info "You may need to restart your terminal or run 'source ~/.bashrc'"
    fi
}

# Check system requirements
check_requirements() {
    print_info "Checking system requirements..."
    
    # Check for curl or wget
    if ! command -v curl >/dev/null 2>&1 && ! command -v wget >/dev/null 2>&1; then
        print_error "Neither curl nor wget found. Please install one of them."
        exit 1
    fi
    
    # Check for git
    if ! command -v git >/dev/null 2>&1; then
        print_warning "Git is not installed. Some features may not work properly."
        print_info "Please consider installing Git for full functionality."
    fi
    
    # Windows-specific checks
    if is_windows; then
        print_info "Detected Windows environment (Git Bash/MSYS2/Cygwin)"
        
        # Check if we can create directories
        local test_dir="$HOME/.local"
        if ! mkdir -p "$test_dir" 2>/dev/null; then
            print_warning "Cannot create user directories. Installation may fail."
        fi
    fi
    
    print_success "System requirements check passed"
}

# Post-installation setup
post_install_setup() {
    print_info "Running post-installation setup..."
    
    # Try multiple ways to verify installation
    local tool_found=false
    
    if command -v "$BINARY_NAME" >/dev/null 2>&1; then
        tool_found=true
    elif is_windows && command -v "${BINARY_NAME}.exe" >/dev/null 2>&1; then
        tool_found=true
    else
        # Try direct path
        local install_dir=$(get_install_directory)
        if [[ -f "${install_dir}/${BINARY_NAME}" ]]; then
            export PATH="$install_dir:$PATH"
            if command -v "$BINARY_NAME" >/dev/null 2>&1; then
                tool_found=true
            fi
        elif is_windows && [[ -f "${install_dir}/${BINARY_NAME}.exe" ]]; then
            export PATH="$install_dir:$PATH"
            if command -v "${BINARY_NAME}.exe" >/dev/null 2>&1; then
                tool_found=true
            fi
        fi
    fi
    
    if $tool_found; then
        print_success "Tool is ready to use!"
        print_info "Run '$BINARY_NAME settings' to configure your preferences."
        print_info "Run '$BINARY_NAME --help' for usage information."
    else
        print_warning "Tool verification failed. You may need to restart your shell."
        if is_windows; then
            print_info "Try one of these commands:"
            print_info "  - Restart Git Bash"
            print_info "  - Run 'source ~/.bash_profile' or 'source ~/.bashrc'"
            print_info "  - Add to PATH manually: export PATH=\"\$HOME/.local/bin:\$PATH\""
        else
            print_info "Run 'source ~/.bashrc' or restart your terminal."
        fi
    fi
}

# Uninstall function
uninstall() {
    print_info "Uninstalling $TOOL_NAME..."
    
    # Find and remove binary
    local binary_locations=(
        "/usr/local/bin/${BINARY_NAME}"
        "$HOME/.local/bin/${BINARY_NAME}"
        "/usr/bin/${BINARY_NAME}"
    )
    
    # Add Windows-specific locations
    if is_windows; then
        binary_locations+=(
            "$HOME/.local/bin/${BINARY_NAME}.exe"
            "$(get_install_directory)/${BINARY_NAME}"
            "$(get_install_directory)/${BINARY_NAME}.exe"
        )
        
        if [[ -n "$USERPROFILE" ]]; then
            local user_bin="$(cygpath -u "$USERPROFILE" 2>/dev/null || echo "$USERPROFILE")/.local/bin"
            binary_locations+=(
                "${user_bin}/${BINARY_NAME}"
                "${user_bin}/${BINARY_NAME}.exe"
            )
        fi
    fi
    
    local found=false
    for location in "${binary_locations[@]}"; do
        if [[ -f "$location" ]]; then
            rm -f "$location"
            print_success "Removed $location"
            found=true
        fi
    done
    
    if [[ "$found" == false ]]; then
        print_warning "Binary not found in standard locations"
    fi
    
    # Run tool's own uninstall if available
    if command -v "$BINARY_NAME" >/dev/null 2>&1; then
        "$BINARY_NAME" settings # This will trigger the uninstall through the tool's settings
    fi
    
    print_success "Uninstallation completed"
}

# Show installation confirmation with detailed version info
show_install_confirmation() {
    local current_version="$1"
    local latest_version="$2"
    local status="$3"
    
    echo -e "\n${CYAN}${BOLD}📋 Installation Information:${NC}"
    echo -e "${YELLOW}   Current version:${NC} $current_version"
    echo -e "${YELLOW}   Latest version:${NC}  $latest_version"
    echo -e "${YELLOW}   Status:${NC}          $status"
    echo ""
    
    case "$status" in
        "same version")
            print_info "You have the same version installed."
            print_info "Reinstalling will replace your current installation."
            ;;
        "newer version")
            print_warning "You have a newer version than what's being installed!"
            print_warning "This will downgrade your installation from $current_version to $latest_version."
            ;;
        "older version")
            print_success "A newer version is available!"
            print_info "This will upgrade your installation from $current_version to $latest_version."
            ;;
    esac
    
    echo ""
    echo -e "${BOLD}What would you like to do?${NC}"
    echo -e "${GREEN}  y${NC} - Proceed with installation"
    echo -e "${RED}  n${NC} - Cancel installation"
    echo -e "${CYAN}  s${NC} - Show current tool settings"
    echo ""
    
    local max_attempts=3
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        local choice=$(read_input "Your choice (y/n/s) [y]: " "y")
        
        case "$choice" in
            [Yy]|[Yy][Ee][Ss]|"")
                return 0  # Proceed
                ;;
            [Nn]|[Nn][Oo])
                return 1  # Cancel
                ;;
            [Ss])
                show_current_settings
                echo ""
                # Reset attempt counter for settings view
                attempt=1
                ;;
            *)
                print_warning "Invalid choice: '$choice'. Please enter y, n, or s."
                attempt=$((attempt + 1))
                ;;
        esac
    done
    
    # If max attempts reached, default to proceed
    print_warning "Max attempts reached, proceeding with installation..."
    return 0
}

# Show current tool settings
show_current_settings() {
    if command -v "$BINARY_NAME" >/dev/null 2>&1; then
        print_info "Current tool configuration:"
        echo "----------------------------------------"
        
        # Try to get version
        local version_output=$("$BINARY_NAME" --version 2>/dev/null || echo "Version: Unknown")
        echo "🔧 $version_output"
        
        # Try to show help
        local help_output=$("$BINARY_NAME" --help 2>/dev/null | head -5 || echo "Help not available")
        echo "📚 Available commands:"
        echo "$help_output"
        
        echo "----------------------------------------"
        print_info "Run '$BINARY_NAME settings' for detailed configuration."
    elif is_windows && command -v "${BINARY_NAME}.exe" >/dev/null 2>&1; then
        print_info "Tool found as ${BINARY_NAME}.exe"
        "${BINARY_NAME}.exe" --version 2>/dev/null || echo "Version check failed"
    else
        print_warning "Tool is not currently accessible."
    fi
}

# Main installation function
main() {
    print_header
    
    # Check for uninstall flag
    if [[ "$1" == "--uninstall" ]]; then
        uninstall
        exit 0
    fi
    
    # Platform detection and info
    local platform=$(detect_platform)
    if is_windows; then
        print_info "Detected platform: $platform (Windows environment)"
    else
        print_info "Detected platform: $platform"
    fi
    
    # Check system requirements
    check_requirements
    
    # Check if already installed and show detailed info
    local tool_exists=false
    if command -v "$BINARY_NAME" >/dev/null 2>&1; then
        tool_exists=true
    elif is_windows && command -v "${BINARY_NAME}.exe" >/dev/null 2>&1; then
        tool_exists=true
        BINARY_NAME="${BINARY_NAME}.exe"  # Adjust for Windows
    fi
    
    if $tool_exists; then
        # Try to get current version
        local current_version=$("$BINARY_NAME" --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
        
        # If version extraction failed, try alternative method
        if [[ -z "$current_version" ]]; then
            current_version=$("$BINARY_NAME" --version 2>/dev/null || echo "unknown")
            current_version=$(echo "$current_version" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
        fi
        
        # Default to "unknown" if still empty
        if [[ -z "$current_version" ]]; then
            current_version="unknown"
        fi
        
        local status=$(get_version_status "$current_version" "$VERSION")
        
        # Show detailed confirmation dialog
        if ! show_install_confirmation "$current_version" "$VERSION" "$status"; then
            print_info "Installation cancelled by user."
            exit 0
        fi
        
        print_info "Proceeding with installation..."
    else
        print_info "$TOOL_NAME is not currently installed."
        print_info "Installing version $VERSION..."
    fi
    
    # Try to download pre-built binary first, fallback to building from source
    if ! check_go_installation; then
        print_info "Attempting to download pre-built binary..."
        download_prebuilt_binary
    else
        print_info "Go found. Building from source..."
        build_from_source
    fi
    
    # Post-installation setup
    post_install_setup
    
    print_success "🎉 Installation completed successfully!"
    
    # Show final version info
    local final_binary="$BINARY_NAME"
    if is_windows && ! command -v "$BINARY_NAME" >/dev/null 2>&1 && command -v "${BINARY_NAME}.exe" >/dev/null 2>&1; then
        final_binary="${BINARY_NAME}.exe"
    fi
    
    if command -v "$final_binary" >/dev/null 2>&1; then
        local final_version=$("$final_binary" --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "$VERSION")
        print_info "✨ $TOOL_NAME version $final_version is now ready to use!"
    fi
    
    # Platform-specific final instructions
    if is_windows; then
        echo ""
        print_info "📝 Windows-specific instructions:"
        print_info "   - You may need to restart Git Bash or your terminal"
        print_info "   - Or run: source ~/.bash_profile (or ~/.bashrc)"
        print_info "   - If still not found, add manually: export PATH=\"\$HOME/.local/bin:\$PATH\""
        print_info "   - Verify with: $final_binary --help"
    else
        print_info "You may need to restart your terminal or run 'source ~/.bashrc' to use the tool."
    fi
    
    print_info "Get started with: $final_binary --help"
}

# Run main function
main "$@"