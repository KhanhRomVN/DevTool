#!/bin/bash

# Dev Tool - AI-powered Git Commit Message Generator
# Enhanced Cross-platform installer with bilingual support and update functionality
# Developer: KhanhRomVN
# Repository: https://github.com/KhanhRomVN/dev_tool
# Contact: khanhromvn@gmail.com

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
VERSION="2.1.5"
REPO_URL="https://github.com/KhanhRomVN/DevTool"
BINARY_NAME="dev_tool"
DEVELOPER="KhanhRomVN"
CONTACT="khanhromvn@gmail.com"

# Installation modes
UPDATE_MODE=false

# Language support
LANG_EN="en"
LANG_VI="vi"
CURRENT_LANG="$LANG_EN"

# Process command line arguments
process_arguments() {
    for arg in "$@"
    do
        case $arg in
            --update)
                UPDATE_MODE=true
                shift
                ;;
            --uninstall)
                uninstall
                exit 0
                ;;
            --help|--guide)
                show_help
                exit 0
                ;;
            *)
                # Unknown option
                ;;
        esac
    done
}

# Show help function
show_help() {
    echo -e "${CYAN}${BOLD}Dev Tool Installer${RESET}"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo -e "  ${GREEN}--update${RESET}      Update existing installation to version $VERSION"
    echo -e "  ${GREEN}--uninstall${RESET}   Remove dev_tool from system"
    echo -e "  ${GREEN}--help${RESET}        Show this help message"
    echo -e "  ${GREEN}--guide${RESET}       Show detailed command guide"
    echo ""
    echo "Examples:"
    echo -e "  ${DIM}./install.sh${RESET}           # Fresh installation"
    echo -e "  ${DIM}./install.sh --update${RESET}   # Update existing installation"
    echo -e "  ${DIM}./install.sh --help${RESET}     # Show this help"
    echo ""
    echo "Environment variables:"
    echo -e "  ${YELLOW}DEV_TOOL_LANG${RESET}       Set language (en|vi)"
    echo ""
    echo "For more information, visit: $REPO_URL"
}

# Language detection
detect_language() {
    # Check system locale
    if [[ "$LANG" == *"vi"* ]] || [[ "$LANGUAGE" == *"vi"* ]] || [[ "$LC_ALL" == *"vi"* ]]; then
        CURRENT_LANG="$LANG_VI"
    else
        CURRENT_LANG="$LANG_EN"
    fi
    
    # Allow override with environment variable
    if [[ -n "$DEV_TOOL_LANG" ]]; then
        CURRENT_LANG="$DEV_TOOL_LANG"
    fi
}

# Multilingual text function
text() {
    local key="$1"
    case "$key" in
        # Headers and titles
        "header_title")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "CÀI ĐẶT DEV TOOL 2.0"
            else
                echo "DEV TOOL 2.0 INSTALLER"
            fi
            ;;
        "header_subtitle")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Trợ lý Git thông minh với AI"
            else
                echo "AI-Powered Git Assistant Setup"
            fi
            ;;
        "header_developer")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Phát triển bởi: $DEVELOPER"
            else
                echo "Developed by: $DEVELOPER"
            fi
            ;;
        "update_mode_title")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "CẬP NHẬT DEV TOOL"
            else
                echo "UPDATE DEV TOOL"
            fi
            ;;
        "update_checking")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Kiểm tra phiên bản hiện tại"
            else
                echo "Checking current version"
            fi
            ;;
        "update_from_to")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Cập nhật từ phiên bản $1 lên $2"
            else
                echo "Updating from version $1 to $2"
            fi
            ;;
        "update_same_version")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Đã có phiên bản mới nhất ($1)"
            else
                echo "Already running latest version ($1)"
            fi
            ;;
        "update_success")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Cập nhật thành công!"
            else
                echo "Update completed successfully!"
            fi
            ;;
        
        # Status messages
        "detecting_platform")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Đang phát hiện hệ điều hành"
            else
                echo "Detecting platform"
            fi
            ;;
        "checking_requirements")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Kiểm tra yêu cầu hệ thống"
            else
                echo "Checking system requirements"
            fi
            ;;
        "requirements_passed")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Hệ thống đáp ứng yêu cầu"
            else
                echo "System requirements check passed"
            fi
            ;;
        "not_installed")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "$TOOL_NAME chưa được cài đặt"
            else
                echo "$TOOL_NAME is not currently installed"
            fi
            ;;
        "installing_version")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Đang cài đặt phiên bản $VERSION"
            else
                echo "Installing version $VERSION"
            fi
            ;;
        "go_found")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Đã tìm thấy Go"
            else
                echo "Go found"
            fi
            ;;
        "building_source")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Đã tìm thấy Go. Đang build từ mã nguồn"
            else
                echo "Go found. Building from source"
            fi
            ;;
        "cloning_repo")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Đang tải repository"
            else
                echo "Cloning repository"
            fi
            ;;
        "building_binary")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Đang build binary"
            else
                echo "Building binary"
            fi
            ;;
        "installing_to")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Đang cài đặt vào"
            else
                echo "Installing to"
            fi
            ;;
        "path_configured")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "PATH đã được cấu hình trong"
            else
                echo "PATH already configured in"
            fi
            ;;
        "install_success")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "$TOOL_NAME đã được cài đặt thành công!"
            else
                echo "$TOOL_NAME installed successfully!"
            fi
            ;;
        "install_location")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Vị trí cài đặt"
            else
                echo "Installation location"
            fi
            ;;
        "post_install")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Đang thiết lập sau cài đặt"
            else
                echo "Running post-installation setup"
            fi
            ;;
        "tool_ready")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Công cụ đã sẵn sàng sử dụng!"
            else
                echo "Tool is ready to use!"
            fi
            ;;
        "run_settings")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Chạy '$BINARY_NAME settings' để cấu hình tùy chọn"
            else
                echo "Run '$BINARY_NAME settings' to configure your preferences"
            fi
            ;;
        "run_help")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Chạy '$BINARY_NAME --help' để xem hướng dẫn sử dụng"
            else
                echo "Run '$BINARY_NAME --help' for usage information"
            fi
            ;;
        "install_complete")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "🎉 Cài đặt hoàn tất thành công!"
            else
                echo "🎉 Installation completed successfully!"
            fi
            ;;
        "version_ready")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "✨ $TOOL_NAME phiên bản $1 đã sẵn sàng sử dụng!"
            else
                echo "✨ $TOOL_NAME version $1 is now ready to use!"
            fi
            ;;
        "restart_terminal")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Bạn có thể cần khởi động lại terminal hoặc chạy 'source ~/.bashrc' để sử dụng công cụ"
            else
                echo "You may need to restart your terminal or run 'source ~/.bashrc' to use the tool"
            fi
            ;;
        "get_started")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Bắt đầu với: $BINARY_NAME --help"
            else
                echo "Get started with: $BINARY_NAME --help"
            fi
            ;;
        "installing_go")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Đang cài đặt Go mới nhất"
            else
                echo "Installing latest Go"
            fi
            ;;
        "go_install_success")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Go đã được cài đặt thành công"
            else
                echo "Go installed successfully"
            fi
            ;;
        "downloading_go")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo "Đang tải Go"
            else
                echo "Downloading Go"
            fi
            ;;
        *)
            echo "$key"
            ;;
    esac
}

# Enhanced print functions with better styling
print_info() {
    echo -e "${BLUE}${BOLD}ℹ️  ${RESET}${BLUE}$1${RESET}"
}

print_success() {
    echo -e "${GREEN}${BOLD}✅ ${RESET}${GREEN}$1${RESET}"
}

print_warning() {
    echo -e "${YELLOW}${BOLD}⚠️  ${RESET}${YELLOW}$1${RESET}"
}

print_error() {
    echo -e "${RED}${BOLD}❌ ${RESET}${RED}$1${RESET}"
}

print_step() {
    echo -e "${CYAN}${BOLD}🔧 ${RESET}${CYAN}$1${RESET}"
}

print_highlight() {
    echo -e "${MAGENTA}${BOLD}✨ ${RESET}${MAGENTA}$1${RESET}"
}

# Enhanced header with developer info and multilingual support
print_header() {
    clear
    echo -e "${CYAN}${BOLD}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                              ║"
    if [[ "$UPDATE_MODE" == true ]]; then
        echo "║                          🔄  $(text "update_mode_title")                          ║"
        echo "║                        $(text "header_subtitle")                        ║"
    else
        echo "║                          🛠️  $(text "header_title")                           ║"
        echo "║                        $(text "header_subtitle")                        ║"
    fi
    echo "║                                                                              ║"
    echo "║  $(text "header_developer")                                                    ║"
    echo "║  📧 Email: $CONTACT                                           ║"
    echo "║  🌐 Repository: $REPO_URL              ║"
    echo "║  📦 Version: $VERSION                                                        ║"
    echo "║                                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${RESET}"
    echo ""
}

# Language selection menu
show_language_menu() {
    echo -e "${WHITE}${BOLD}$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "🌐 Chọn ngôn ngữ / Select Language"; else echo "🌐 Select Language / Chọn ngôn ngữ"; fi)${RESET}"
    echo -e "${CYAN}  1.${RESET} English"
    echo -e "${CYAN}  2.${RESET} Tiếng Việt"
    echo ""
    
    local choice=$(read_input "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Lựa chọn (1/2)"; else echo "Choice (1/2)"; fi) [1]: " "1")
    
    case $choice in
        2)
            CURRENT_LANG="$LANG_VI"
            ;;
        *)
            CURRENT_LANG="$LANG_EN"
            ;;
    esac
}

# Enhanced platform detection function
detect_platform() {
    local os=""
    local arch=""
    
    case "$(uname -s)" in
        Linux*)     os="linux";;
        Darwin*)    os="darwin";;
        CYGWIN*|MINGW*|MSYS*)   os="windows";;
        *)          
            if [[ -n "$WINDIR" ]] || [[ -n "$SYSTEMROOT" ]]; then
                os="windows"
            else
                print_error "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Hệ điều hành không được hỗ trợ"; else echo "Unsupported operating system"; fi): $(uname -s)"
                exit 1
            fi
            ;;
    esac
    
    case "$(uname -m)" in
        x86_64|amd64)   arch="amd64";;
        arm64|aarch64)  arch="arm64";;
        armv6l)         arch="armv6";;
        armv7l)         arch="armv7";;
        i386|i686)      arch="386";;
        *)
            print_error "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Kiến trúc không được hỗ trợ"; else echo "Unsupported architecture"; fi): $(uname -m)"
            exit 1
            ;;
    esac
    
    echo "${os}_${arch}"
}

is_windows() {
    [[ "$(uname -s)" == CYGWIN* ]] || [[ "$(uname -s)" == MINGW* ]] || [[ "$(uname -s)" == MSYS* ]] || [[ -n "$WINDIR" ]]
}

get_install_directory() {
    if [[ "$EUID" -eq 0 ]]; then
        echo "/usr/local/bin"
    else
        if is_windows; then
            local user_bin=""
            if [[ -n "$USERPROFILE" ]]; then
                user_bin="$(cygpath -u "$USERPROFILE" 2>/dev/null || echo "$USERPROFILE")/.local/bin"
            else
                user_bin="$HOME/.local/bin"
            fi
            mkdir -p "$user_bin"
            echo "$user_bin"
        else
            if [[ -d "$HOME/.local/bin" ]]; then
                echo "$HOME/.local/bin"
            else
                mkdir -p "$HOME/.local/bin"
                echo "$HOME/.local/bin"
            fi
        fi
    fi
}

add_to_path() {
    local install_dir="$1"
    local shell_profile=""
    local path_export=""
    
    if [[ -n "$BASH_VERSION" ]]; then
        if is_windows; then
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
    
    if is_windows; then
        local normalized_dir="$install_dir"
        if [[ "$install_dir" == *":"* ]]; then
            normalized_dir="$(cygpath -u "$install_dir" 2>/dev/null || echo "$install_dir")"
        fi
        path_export="export PATH=\"${normalized_dir}:\$PATH\""
    else
        path_export="export PATH=\"${install_dir}:\$PATH\""
    fi
    
    local path_pattern="\.local/bin"
    
    if ! grep -q "export PATH.*${path_pattern}" "$shell_profile" 2>/dev/null; then
        echo "" >> "$shell_profile"
        echo "# Local binaries" >> "$shell_profile"
        echo "$path_export" >> "$shell_profile"
        print_success "$(text "path_configured") $shell_profile"
        export PATH="$install_dir:$PATH"
        
        if is_windows; then
            export PATH="$install_dir:$PATH"
            if [[ -n "$USERPROFILE" ]]; then
                local win_path="$(cygpath -w "$install_dir" 2>/dev/null || echo "$install_dir")"
                export PATH="$install_dir:$PATH"
            fi
        fi
    else
        print_info "$(text "path_configured") $shell_profile"
        export PATH="$install_dir:$PATH"
    fi
}

read_input() {
    local prompt="$1"
    local default="$2"
    local validation_pattern="${3:-}"
    local input=""
    local attempts=0
    local max_attempts=3
    
    while [[ $attempts -lt $max_attempts ]]; do
        if [ -t 0 ]; then
            read -p "$prompt" input
        elif [ -r /dev/tty ]; then
            read -p "$prompt" input < /dev/tty
        else
            print_warning "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Không thể đọc input, sử dụng mặc định"; else echo "Cannot read input, using default"; fi): $default"
            input="$default"
            break
        fi
        
        # Use default if empty
        if [[ -z "$input" ]]; then
            input="$default"
        fi
        
        # Validate input if pattern provided
        if [[ -n "$validation_pattern" ]]; then
            if [[ "$input" =~ ^${validation_pattern}$ ]]; then
                break
            else
                ((attempts++))
                if [[ $attempts -lt $max_attempts ]]; then
                    print_warning "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Input không hợp lệ. Thử lại"; else echo "Invalid input. Please try again"; fi)"
                fi
            fi
        else
            break
        fi
    done
    
    echo "$input"
}

check_go_installation() {
    # Check multiple possible locations for Go
    local go_locations=(
        "$(command -v go 2>/dev/null)"
        "$HOME/go/bin/go"
        "/usr/local/go/bin/go"
        "/usr/bin/go"
        "/usr/lib/go/bin/go"  # Arch Linux specific
        "/opt/go/bin/go"      # Alternative location
    )
    
    for go_bin in "${go_locations[@]}"; do
        if [[ -x "$go_bin" ]] && "$go_bin" version >/dev/null 2>&1; then
            local go_version=$("$go_bin" version | awk '{print $3}' | sed 's/go//')
            print_success "$(text "go_found"): version $go_version"
            
            # Get GOROOT more reliably
            local go_root=$("$go_bin" env GOROOT 2>/dev/null)
            
            # Fallback GOROOT detection for different systems
            if [[ -z "$go_root" ]] || [[ ! -d "$go_root" ]]; then
                # Try common locations based on binary path
                local bin_dir=$(dirname "$go_bin")
                local possible_roots=(
                    "$(dirname "$bin_dir")"
                    "/usr/lib/go"      # Arch Linux package location
                    "/usr/local/go"    # Standard location
                    "/opt/go"          # Alternative location
                )
                
                for root in "${possible_roots[@]}"; do
                    if [[ -d "$root" ]] && [[ -f "$root/bin/go" ]]; then
                        go_root="$root"
                        break
                    fi
                done
            fi
            
            if [[ -n "$go_root" ]] && [[ -d "$go_root" ]]; then
                export GOROOT="$go_root"
                export PATH="$GOROOT/bin:$PATH"
                print_info "GOROOT set to: $GOROOT"
                return 0
            else
                print_warning "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Tìm thấy Go nhưng không thể xác định GOROOT"; else echo "Found Go but cannot determine GOROOT"; fi)"
                # Continue with Go found but no GOROOT
                export PATH="$(dirname "$go_bin"):$PATH"
                return 0
            fi
        fi
    done
    
    print_warning "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Go chưa được cài đặt trên hệ thống này"; else echo "Go is not installed on this system"; fi)"
    return 1
}

install_go() {
    print_step "$(text "installing_go")..."
    
    local platform=$(detect_platform)
    local os=$(echo "$platform" | cut -d'_' -f1)
    local arch=$(echo "$platform" | cut -d'_' -f2)
    
    # Map architecture names to Go's naming convention
    case "$arch" in
        "amd64") arch="amd64" ;;
        "arm64") arch="arm64" ;;
        "386") arch="386" ;;
        "armv6") arch="armv6l" ;;
        "armv7") arch="armv6l" ;;
        *) arch="amd64" ;;
    esac
    
    # Use fixed version for Windows to avoid download issues
    local go_version="go1.21.0"
    
    # For non-Windows systems, try to get latest version
    if [[ "$os" != "windows" ]]; then
        go_version=$(curl -s https://golang.org/VERSION?m=text | head -n 1)
        if [[ -z "$go_version" ]]; then
            go_version="go1.21.0"
        fi
    fi
    
    local go_url=""
    local temp_dir=$(mktemp -d)
    local go_install_dir="/usr/local/go"
    
    # Use user directory if not root
    if [[ "$EUID" -ne 0 ]]; then
        go_install_dir="$HOME/go-lang"
    fi
    
    # Kiểm tra kết nối mạng trước khi tải
    if ! check_network_connectivity; then
        print_error "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Không có kết nối mạng. Không thể tải Go"; else echo "No network connectivity. Cannot download Go"; fi)"
        show_manual_go_installation
        return 1
    fi

    print_info "$(text "downloading_go")..."
    
    # Sử dụng fallback download
    if ! download_go_with_fallback "$go_version" "$os" "$arch" "$temp_dir"; then
        print_error "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Không thể tải Go từ tất cả mirrors"; else echo "Failed to download Go from all mirrors"; fi)"
        show_manual_go_installation
        return 1
    fi

    # Extract downloaded file
    if [[ "$os" == "windows" ]]; then
        if ! unzip -q "$temp_dir/go.zip" -d "$temp_dir"; then
            print_error "Failed to extract Go archive"
            return 1
        fi
        rm -f "$temp_dir/go.zip"
    else
        if ! tar -xzf "$temp_dir/go.tar.gz" -C "$temp_dir"; then
            print_error "Failed to extract Go archive"
            return 1
        fi
        rm -f "$temp_dir/go.tar.gz"
    fi

    rm -rf "$go_install_dir"
    mv "$temp_dir/go" "$go_install_dir"
    
     # Set correct environment variables
    export GOROOT="$go_install_dir"
    export GOPATH="$HOME/go"
    export GOMODCACHE="$GOPATH/pkg/mod"
    export PATH="$GOROOT/bin:$PATH"
    
    # Create GOPATH directory if it doesn't exist
    mkdir -p "$GOPATH" "$GOMODCACHE"
    
    # Verify GOROOT is accessible
    if [[ ! -d "$GOROOT" ]] || [[ ! -f "$GOROOT/bin/go" ]]; then
        print_error "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "GOROOT không hợp lệ sau khi cài đặt"; else echo "Invalid GOROOT after installation"; fi): $GOROOT"
        return 1
    fi
    
    # Add to shell profile
    local shell_profiles=("$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile")
    
    if is_windows; then
        shell_profiles+=("$HOME/.bash_profile")
    fi
    
    for profile in "${shell_profiles[@]}"; do
        if [[ -f "$profile" ]]; then
            # Remove old Go paths to prevent conflicts
            sed -i '/export GOROOT=/d' "$profile" 2>/dev/null || true
            sed -i '/export GOPATH=/d' "$profile" 2>/dev/null || true
            sed -i '/export GOMODCACHE=/d' "$profile" 2>/dev/null || true
            
            # Add new Go configuration
            echo "" >> "$profile"
            echo "# Go language configuration" >> "$profile"
            echo "export GOROOT=\"$go_install_dir\"" >> "$profile"
            echo "export GOPATH=\"\$HOME/go\"" >> "$profile"
            echo "export GOMODCACHE=\"\$GOPATH/pkg/mod\"" >> "$profile"
            echo "export PATH=\"\$GOROOT/bin:\$PATH\"" >> "$profile"
            break
        fi
    done
    
    rm -rf "$temp_dir"
    print_success "$(text "go_install_success")"
    
    # Verify installation với multiple attempts
    local verification_attempts=3
    local verified=false

    for ((i=1; i<=verification_attempts; i++)); do
        if [[ -f "$GOROOT/bin/go" ]] && "$GOROOT/bin/go" version >/dev/null 2>&1; then
            local installed_version=$("$GOROOT/bin/go" version | awk '{print $3}')
            print_success "$(text "go_install_success"): $installed_version"
            verified=true
            break
        fi
        
        if [[ $i -lt $verification_attempts ]]; then
            print_info "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Thử xác minh lần $i thất bại, đang thử lại"; else echo "Verification attempt $i failed, retrying"; fi)..."
            sleep 2
        fi
    done

    if [[ "$verified" == false ]]; then
        print_error "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Xác minh cài đặt Go thất bại"; else echo "Go installation verification failed"; fi)"
        show_manual_go_installation
        return 1
    fi
}

# Download Go với fallback mirrors
download_go_with_fallback() {
    local go_version="$1"
    local os="$2" 
    local arch="$3"
    local temp_dir="$4"
    local file_extension=""
    
    if [[ "$os" == "windows" ]]; then
        file_extension="zip"
    else
        file_extension="tar.gz"
    fi
    
    local filename="$go_version.$os-$arch.$file_extension"
    local mirrors=(
        "https://dl.google.com/go/$filename"
        "https://golang.org/dl/$filename"
        "https://go.dev/dl/$filename"
    )
    
    for mirror in "${mirrors[@]}"; do
        print_info "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Thử tải từ"; else echo "Trying to download from"; fi): $mirror"
        
        if command -v curl >/dev/null 2>&1; then
            if curl -L --connect-timeout 30 --max-time 300 -o "$temp_dir/go.$file_extension" "$mirror"; then
                return 0
            fi
        else
            if wget --timeout=300 -O "$temp_dir/go.$file_extension" "$mirror"; then
                return 0
            fi
        fi
        
        print_warning "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Tải thất bại từ mirror này"; else echo "Failed to download from this mirror"; fi)"
    done
    
    return 1
}

# Manual Go installation guide
show_manual_go_installation() {
    echo ""
    echo -e "${YELLOW}${BOLD}╔══════════════════════════════════════════════════════════════════════════════╗${RESET}"
    if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
        echo -e "${YELLOW}${BOLD}║                        ⚠️  CÀI ĐẶT GO THẤT BẠI                               ║${RESET}"
        echo -e "${YELLOW}${BOLD}║                     HƯỚNG DẪN CÀI ĐẶT GO THỦ CÔNG                           ║${RESET}"
    else
        echo -e "${YELLOW}${BOLD}║                          ⚠️  GO INSTALLATION FAILED                        ║${RESET}"
        echo -e "${YELLOW}${BOLD}║                      MANUAL GO INSTALLATION GUIDE                           ║${RESET}"
    fi
    echo -e "${YELLOW}${BOLD}╚══════════════════════════════════════════════════════════════════════════════╝${RESET}"
    echo ""
    
    local platform=$(detect_platform)
    local os=$(echo "$platform" | cut -d'_' -f1)
    local arch=$(echo "$platform" | cut -d'_' -f2)
    
    # Map architecture for display
    case "$arch" in
        "amd64") arch_display="64-bit" ;;
        "arm64") arch_display="ARM64" ;;
        "386") arch_display="32-bit" ;;
        *) arch_display="$arch" ;;
    esac
    
    if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
        print_info "Hệ thống phát hiện: $os ($arch_display)"
        echo ""
        echo -e "${WHITE}${BOLD}📋 CÁCH CÀI ĐẶT GO CHO HỆ THỐNG CỦA BẠN:${RESET}"
    else
        print_info "Detected system: $os ($arch_display)"
        echo ""
        echo -e "${WHITE}${BOLD}📋 HOW TO INSTALL GO FOR YOUR SYSTEM:${RESET}"
    fi
    
    case "$os" in
        "windows")
            show_windows_go_installation
            ;;
        "linux")
            show_linux_go_installation
            ;;
        "darwin")
            show_macos_go_installation
            ;;
        *)
            show_generic_go_installation
            ;;
    esac
    
    echo ""
    if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
        echo -e "${CYAN}${BOLD}🔄 SAU KHI CÀI ĐẶT GO:${RESET}"
        echo -e "${GREEN}  1.${RESET} Khởi động lại terminal"
        echo -e "${GREEN}  2.${RESET} Chạy lại script này: ${GREEN}./install.sh${RESET}"
        echo -e "${GREEN}  3.${RESET} Hoặc chạy: ${GREEN}go version${RESET} để kiểm tra"
        echo ""
        echo -e "${MAGENTA}${BOLD}💡 LƯU Ý:${RESET} ${MAGENTA}Đảm bảo biến môi trường PATH đã được cập nhật${RESET}"
    else
        echo -e "${CYAN}${BOLD}🔄 AFTER INSTALLING GO:${RESET}"
        echo -e "${GREEN}  1.${RESET} Restart your terminal"
        echo -e "${GREEN}  2.${RESET} Re-run this script: ${GREEN}./install.sh${RESET}"
        echo -e "${GREEN}  3.${RESET} Or run: ${GREEN}go version${RESET} to verify"
        echo ""
        echo -e "${MAGENTA}${BOLD}💡 NOTE:${RESET} ${MAGENTA}Make sure PATH environment variable is updated${RESET}"
    fi
}

# Windows Go installation guide
show_windows_go_installation() {
    if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
        echo -e "${BLUE}${BOLD}🪟 WINDOWS:${RESET}"
        echo ""
        echo -e "${YELLOW}${BOLD}Phương pháp 1: Tải từ trang chính thức (Khuyên dùng)${RESET}"
        echo -e "${GREEN}  1.${RESET} Truy cập: ${CYAN}https://golang.org/dl/${RESET}"
        echo -e "${GREEN}  2.${RESET} Tải file: ${GREEN}go1.21.x.windows-amd64.msi${RESET}"
        echo -e "${GREEN}  3.${RESET} Chạy file .msi và làm theo hướng dẫn"
        echo -e "${GREEN}  4.${RESET} Khởi động lại Command Prompt/PowerShell"
        echo ""
        echo -e "${YELLOW}${BOLD}Phương pháp 2: Sử dụng Chocolatey${RESET}"
        echo -e "${GREEN}  1.${RESET} Mở PowerShell với quyền Admin"
        echo -e "${GREEN}  2.${RESET} Chạy: ${GREEN}choco install golang${RESET}"
        echo ""
        echo -e "${YELLOW}${BOLD}Phương pháp 3: Sử dụng Scoop${RESET}"
        echo -e "${GREEN}  1.${RESET} Mở PowerShell"
        echo -e "${GREEN}  2.${RESET} Chạy: ${GREEN}scoop install go${RESET}"
        echo ""
        echo -e "${YELLOW}${BOLD}Phương pháp 4: Sử dụng winget${RESET}"
        echo -e "${GREEN}  1.${RESET} Mở Command Prompt hoặc PowerShell"
        echo -e "${GREEN}  2.${RESET} Chạy: ${GREEN}winget install GoLang.Go${RESET}"
    else
        echo -e "${BLUE}${BOLD}🪟 WINDOWS:${RESET}"
        echo ""
        echo -e "${YELLOW}${BOLD}Method 1: Download from official site (Recommended)${RESET}"
        echo -e "${GREEN}  1.${RESET} Visit: ${CYAN}https://golang.org/dl/${RESET}"
        echo -e "${GREEN}  2.${RESET} Download: ${GREEN}go1.21.x.windows-amd64.msi${RESET}"
        echo -e "${GREEN}  3.${RESET} Run the .msi file and follow instructions"
        echo -e "${GREEN}  4.${RESET} Restart Command Prompt/PowerShell"
        echo ""
        echo -e "${YELLOW}${BOLD}Method 2: Using Chocolatey${RESET}"
        echo -e "${GREEN}  1.${RESET} Open PowerShell as Administrator"
        echo -e "${GREEN}  2.${RESET} Run: ${GREEN}choco install golang${RESET}"
        echo ""
        echo -e "${YELLOW}${BOLD}Method 3: Using Scoop${RESET}"
        echo -e "${GREEN}  1.${RESET} Open PowerShell"
        echo -e "${GREEN}  2.${RESET} Run: ${GREEN}scoop install go${RESET}"
        echo ""
        echo -e "${YELLOW}${BOLD}Method 4: Using winget${RESET}"
        echo -e "${GREEN}  1.${RESET} Open Command Prompt or PowerShell"
        echo -e "${GREEN}  2.${RESET} Run: ${GREEN}winget install GoLang.Go${RESET}"
    fi
}

# Linux Go installation guide
show_linux_go_installation() {
    local distro=$(detect_linux_distro)
    
    if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
        echo -e "${BLUE}${BOLD}🐧 LINUX ($distro):${RESET}"
        echo ""
        echo -e "${YELLOW}${BOLD}Lệnh cụ thể cho hệ thống của bạn:${RESET}"
    else
        echo -e "${BLUE}${BOLD}🐧 LINUX ($distro):${RESET}"
        echo ""
        echo -e "${YELLOW}${BOLD}Specific commands for your system:${RESET}"
    fi
    
    case "$distro" in
        "ubuntu"|"debian"|"pop"|"mint"|"elementary")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo -e "${CYAN}${BOLD}Phát hiện: Ubuntu/Debian based${RESET}"
                echo -e "${GREEN}  sudo apt update && sudo apt install golang-go${RESET}"
            else
                echo -e "${CYAN}${BOLD}Detected: Ubuntu/Debian based${RESET}"
                echo -e "${GREEN}  sudo apt update && sudo apt install golang-go${RESET}"
            fi
            ;;
        "centos"|"rhel")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo -e "${CYAN}${BOLD}Phát hiện: CentOS/RHEL${RESET}"
                echo -e "${GREEN}  sudo dnf install golang  ${RESET}${DIM}# (CentOS 8+)${RESET}"
                echo -e "${GREEN}  sudo yum install golang  ${RESET}${DIM}# (CentOS 7)${RESET}"
            else
                echo -e "${CYAN}${BOLD}Detected: CentOS/RHEL${RESET}"
                echo -e "${GREEN}  sudo dnf install golang  ${RESET}${DIM}# (CentOS 8+)${RESET}"
                echo -e "${GREEN}  sudo yum install golang  ${RESET}${DIM}# (CentOS 7)${RESET}"
            fi
            ;;
        "fedora")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo -e "${CYAN}${BOLD}Phát hiện: Fedora${RESET}"
                echo -e "${GREEN}  sudo dnf install golang${RESET}"
            else
                echo -e "${CYAN}${BOLD}Detected: Fedora${RESET}"
                echo -e "${GREEN}  sudo dnf install golang${RESET}"
            fi
            ;;
        "arch"|"manjaro")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo -e "${CYAN}${BOLD}Phát hiện: Arch Linux${RESET}"
                echo -e "${GREEN}  sudo pacman -S go${RESET}"
            else
                echo -e "${CYAN}${BOLD}Detected: Arch Linux${RESET}"
                echo -e "${GREEN}  sudo pacman -S go${RESET}"
            fi
            ;;
        "opensuse"|"suse")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo -e "${CYAN}${BOLD}Phát hiện: openSUSE${RESET}"
                echo -e "${GREEN}  sudo zypper install go${RESET}"
            else
                echo -e "${CYAN}${BOLD}Detected: openSUSE${RESET}"
                echo -e "${GREEN}  sudo zypper install go${RESET}"
            fi
            ;;
        "alpine")
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo -e "${CYAN}${BOLD}Phát hiện: Alpine Linux${RESET}"
                echo -e "${GREEN}  sudo apk add go${RESET}"
            else
                echo -e "${CYAN}${BOLD}Detected: Alpine Linux${RESET}"
                echo -e "${GREEN}  sudo apk add go${RESET}"
            fi
            ;;
        *)
            # Hiển thị tất cả các lựa chọn cho distribution không xác định
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                echo -e "${YELLOW}${BOLD}Không xác định được distribution cụ thể. Thử các lệnh sau:${RESET}"
                echo ""
                echo -e "${CYAN}${BOLD}Ubuntu/Debian:${RESET} ${GREEN}sudo apt update && sudo apt install golang-go${RESET}"
                echo -e "${CYAN}${BOLD}CentOS/RHEL:${RESET} ${GREEN}sudo dnf install golang${RESET}"
                echo -e "${CYAN}${BOLD}Fedora:${RESET} ${GREEN}sudo dnf install golang${RESET}"
                echo -e "${CYAN}${BOLD}Arch Linux:${RESET} ${GREEN}sudo pacman -S go${RESET}"
                echo -e "${CYAN}${BOLD}openSUSE:${RESET} ${GREEN}sudo zypper install go${RESET}"
                echo -e "${CYAN}${BOLD}Alpine Linux:${RESET} ${GREEN}sudo apk add go${RESET}"
            else
                echo -e "${YELLOW}${BOLD}Cannot detect specific distribution. Try these commands:${RESET}"
                echo ""
                echo -e "${CYAN}${BOLD}Ubuntu/Debian:${RESET} ${GREEN}sudo apt update && sudo apt install golang-go${RESET}"
                echo -e "${CYAN}${BOLD}CentOS/RHEL:${RESET} ${GREEN}sudo dnf install golang${RESET}"
                echo -e "${CYAN}${BOLD}Fedora:${RESET} ${GREEN}sudo dnf install golang${RESET}"
                echo -e "${CYAN}${BOLD}Arch Linux:${RESET} ${GREEN}sudo pacman -S go${RESET}"
                echo -e "${CYAN}${BOLD}openSUSE:${RESET} ${GREEN}sudo zypper install go${RESET}"
                echo -e "${CYAN}${BOLD}Alpine Linux:${RESET} ${GREEN}sudo apk add go${RESET}"
            fi
            ;;
    esac
    
    # Thêm phần hướng dẫn cài đặt thủ công
    echo ""
    if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
        echo -e "${YELLOW}${BOLD}Hoặc cài đặt thủ công (phiên bản mới nhất):${RESET}"
        echo -e "${GREEN}  wget https://golang.org/dl/go1.21.6.linux-amd64.tar.gz${RESET}"
        echo -e "${GREEN}  sudo tar -C /usr/local -xzf go1.21.6.linux-amd64.tar.gz${RESET}"
        echo -e "${GREEN}  echo 'export PATH=\$PATH:/usr/local/go/bin' >> ~/.bashrc${RESET}"
        echo -e "${GREEN}  source ~/.bashrc${RESET}"
    else
        echo -e "${YELLOW}${BOLD}Or install manually (latest version):${RESET}"
        echo -e "${GREEN}  wget https://golang.org/dl/go1.21.6.linux-amd64.tar.gz${RESET}"
        echo -e "${GREEN}  sudo tar -C /usr/local -xzf go1.21.6.linux-amd64.tar.gz${RESET}"
        echo -e "${GREEN}  echo 'export PATH=\$PATH:/usr/local/go/bin' >> ~/.bashrc${RESET}"
        echo -e "${GREEN}  source ~/.bashrc${RESET}"
    fi
}

# Phát hiện Linux distribution cụ thể
detect_linux_distro() {
    local distro=""
    
    # Kiểm tra các file nhận diện distribution
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        distro="$ID"
    elif [[ -f /etc/lsb-release ]]; then
        . /etc/lsb-release
        distro=$(echo "$DISTRIB_ID" | tr '[:upper:]' '[:lower:]')
    elif command -v lsb_release >/dev/null 2>&1; then
        distro=$(lsb_release -si | tr '[:upper:]' '[:lower:]')
    elif [[ -f /etc/redhat-release ]]; then
        if grep -q "CentOS" /etc/redhat-release; then
            distro="centos"
        elif grep -q "Red Hat" /etc/redhat-release; then
            distro="rhel"
        elif grep -q "Fedora" /etc/redhat-release; then
            distro="fedora"
        fi
    elif [[ -f /etc/arch-release ]]; then
        distro="arch"
    elif [[ -f /etc/alpine-release ]]; then
        distro="alpine"
    elif [[ -f /etc/SUSE-brand ]] || [[ -f /etc/SuSE-release ]]; then
        distro="opensuse"
    else
        distro="unknown"
    fi
    
    echo "$distro"
}

# Kiểm tra kết nối mạng
check_network_connectivity() {
    local test_urls=(
        "https://golang.org"
        "https://dl.google.com"
        "https://github.com"
    )
    
    for url in "${test_urls[@]}"; do
        if command -v curl >/dev/null 2>&1; then
            if curl -s --connect-timeout 5 --max-time 10 "$url" >/dev/null 2>&1; then
                return 0
            fi
        elif command -v wget >/dev/null 2>&1; then
            if wget --timeout=10 --tries=1 -q --spider "$url" 2>/dev/null; then
                return 0
            fi
        fi
    done
    
    return 1
}

# macOS Go installation guide
show_macos_go_installation() {
    if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
        echo -e "${BLUE}${BOLD}🍎 MACOS:${RESET}"
        echo ""
        echo -e "${YELLOW}${BOLD}Phương pháp 1: Tải từ trang chính thức${RESET}"
        echo -e "${GREEN}  1.${RESET} Truy cập: ${CYAN}https://golang.org/dl/${RESET}"
        echo -e "${GREEN}  2.${RESET} Tải file: ${GREEN}go1.21.x.darwin-amd64.pkg${RESET}"
        echo -e "${GREEN}  3.${RESET} Chạy file .pkg và làm theo hướng dẫn"
        echo ""
        echo -e "${YELLOW}${BOLD}Phương pháp 2: Sử dụng Homebrew${RESET}"
        echo -e "${GREEN}  brew install go${RESET}"
        echo ""
        echo -e "${YELLOW}${BOLD}Phương pháp 3: Sử dụng MacPorts${RESET}"
        echo -e "${GREEN}  sudo port install go${RESET}"
    else
        echo -e "${BLUE}${BOLD}🍎 MACOS:${RESET}"
        echo ""
        echo -e "${YELLOW}${BOLD}Method 1: Download from official site${RESET}"
        echo -e "${GREEN}  1.${RESET} Visit: ${CYAN}https://golang.org/dl/${RESET}"
        echo -e "${GREEN}  2.${RESET} Download: ${GREEN}go1.21.x.darwin-amd64.pkg${RESET}"
        echo -e "${GREEN}  3.${RESET} Run the .pkg file and follow instructions"
        echo ""
        echo -e "${YELLOW}${BOLD}Method 2: Using Homebrew${RESET}"
        echo -e "${GREEN}  brew install go${RESET}"
        echo ""
        echo -e "${YELLOW}${BOLD}Method 3: Using MacPorts${RESET}"
        echo -e "${GREEN}  sudo port install go${RESET}"
    fi
}

# Generic Go installation guide
show_generic_go_installation() {
    if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
        echo -e "${YELLOW}${BOLD}Hướng dẫn chung:${RESET}"
        echo -e "${GREEN}  1.${RESET} Truy cập: ${CYAN}https://golang.org/dl/${RESET}"
        echo -e "${GREEN}  2.${RESET} Chọn file phù hợp với hệ điều hành"
        echo -e "${GREEN}  3.${RESET} Làm theo hướng dẫn cài đặt"
        echo -e "${GREEN}  4.${RESET} Cập nhật biến môi trường PATH"
    else
        echo -e "${YELLOW}${BOLD}Generic instructions:${RESET}"
        echo -e "${GREEN}  1.${RESET} Visit: ${CYAN}https://golang.org/dl/${RESET}"
        echo -e "${GREEN}  2.${RESET} Choose appropriate file for your OS"
        echo -e "${GREEN}  3.${RESET} Follow installation instructions"
        echo -e "${GREEN}  4.${RESET} Update PATH environment variable"
    fi
}

build_from_source() {
    print_step "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Đang build $TOOL_NAME từ mã nguồn"; else echo "Building $TOOL_NAME from source"; fi)..."
    
    # Verify Go environment is set
    local go_binary=""
    if command -v go >/dev/null 2>&1; then
        go_binary="go"
    elif [[ -n "$GOROOT" ]] && [[ -x "$GOROOT/bin/go" ]]; then
        go_binary="$GOROOT/bin/go"
    fi
    
    if [[ -z "$go_binary" ]]; then
        print_error "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Không tìm thấy Go binary để build"; else echo "Cannot find Go binary for building"; fi)"
        return 1
    fi
    
    # Set up Go environment if not already set
    if [[ -z "$GOPATH" ]]; then
        export GOPATH="$HOME/go"
        export GOMODCACHE="$GOPATH/pkg/mod"
        mkdir -p "$GOPATH" "$GOMODCACHE"
    fi
    
    print_info "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Sử dụng Go"; else echo "Using Go"; fi): $($go_binary version)"
    print_info "GOPATH: ${GOPATH:-not set}"
    print_info "GOROOT: ${GOROOT:-system default}"
    
    local temp_dir=$(mktemp -d)
    cd "$temp_dir"
    
    if command -v git >/dev/null 2>&1; then
        print_info "$(text "cloning_repo")..."
        git clone "$REPO_URL" .
    else
        print_error "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Git chưa được cài đặt. Vui lòng cài đặt Git trước"; else echo "Git is not installed. Please install Git first"; fi)."
        exit 1
    fi
    
    print_info "$(text "building_binary")..."
    
    # Use full path to go binary if needed
    local go_cmd="go"
    if [[ -n "$GOROOT" ]] && [[ -x "$GOROOT/bin/go" ]]; then
        go_cmd="$GOROOT/bin/go"
    fi
    
    # Initialize and tidy modules
    $go_cmd mod tidy || {
        print_warning "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "go mod tidy thất bại, tiếp tục build"; else echo "go mod tidy failed, continuing with build"; fi)"
    }
    
    local binary_name="$BINARY_NAME"
    if is_windows; then
        binary_name="${BINARY_NAME}.exe"
    fi
    
    # Build with verbose output for debugging
    print_info "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Đang build binary"; else echo "Building binary"; fi): $binary_name"
    
    if ! $go_cmd build -v -o "$binary_name" .; then
        print_error "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Build thất bại"; else echo "Build failed"; fi)"
        return 1
    fi
    
    print_success "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Build thành công"; else echo "Build successful"; fi): $binary_name"
    
    install_binary "./${binary_name}"
    
    cd /
    rm -rf "$temp_dir"
}

install_binary() {
    local binary_path="$1"
    local install_dir=$(get_install_directory)
    
    chmod +x "$binary_path"
    
    print_info "$(text "installing_to") $install_dir..."
    
    local final_binary_name="$BINARY_NAME"
    if is_windows && [[ "$binary_path" == *.exe ]]; then
        final_binary_name="${BINARY_NAME}.exe"
    fi
    
    cp "$binary_path" "${install_dir}/${final_binary_name}"
    add_to_path "$install_dir"
    
    local verification_attempts=3
    local verified=false
    
    for ((i=1; i<=verification_attempts; i++)); do
        if command -v "$BINARY_NAME" >/dev/null 2>&1 || \
           command -v "${install_dir}/${BINARY_NAME}" >/dev/null 2>&1 || \
           (is_windows && command -v "${BINARY_NAME}.exe" >/dev/null 2>&1); then
            verified=true
            break
        fi
        
        if [[ $i -lt $verification_attempts ]]; then
            print_info "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Thử xác minh lần $i thất bại, đang thử lại"; else echo "Verification attempt $i failed, retrying"; fi)..."
            sleep 1
            export PATH="$install_dir:$PATH"
        fi
    done
    
    if $verified; then
        print_success "$(text "install_success")"
        print_info "$(text "install_location"): ${install_dir}/${final_binary_name}"
    else
        print_warning "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Cài đặt hoàn tất nhưng xác minh thất bại"; else echo "Installation completed but verification failed"; fi)"
        print_info "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Binary đã được cài đặt tại"; else echo "Binary installed to"; fi): ${install_dir}/${final_binary_name}"
        print_info "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Bạn có thể cần khởi động lại terminal hoặc chạy 'source ~/.bashrc'"; else echo "You may need to restart your terminal or run 'source ~/.bashrc'"; fi)"
    fi
}

check_requirements() {
    print_info "$(text "checking_requirements")..."
    
    if ! command -v curl >/dev/null 2>&1 && ! command -v wget >/dev/null 2>&1; then
        print_error "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Không tìm thấy curl hoặc wget. Vui lòng cài đặt một trong hai"; else echo "Neither curl nor wget found. Please install one of them"; fi)."
        exit 1
    fi
    
    if ! command -v git >/dev/null 2>&1; then
        print_warning "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Git chưa được cài đặt. Một số tính năng có thể không hoạt động đúng"; else echo "Git is not installed. Some features may not work properly"; fi)."
        print_info "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Vui lòng cân nhắc cài đặt Git để có đầy đủ chức năng"; else echo "Please consider installing Git for full functionality"; fi)."
    fi
    
    if is_windows; then
        print_info "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Đã phát hiện môi trường Windows (Git Bash/MSYS2/Cygwin)"; else echo "Detected Windows environment (Git Bash/MSYS2/Cygwin)"; fi)"
        
        local test_dir="$HOME/.local"
        if ! mkdir -p "$test_dir" 2>/dev/null; then
            print_warning "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Không thể tạo thư mục người dùng. Cài đặt có thể thất bại"; else echo "Cannot create user directories. Installation may fail"; fi)."
        fi
    fi
    
    print_success "$(text "requirements_passed")"
}

# Get current installed version
get_current_version() {
    local binary_name="$BINARY_NAME"
    if is_windows && command -v "${BINARY_NAME}.exe" >/dev/null 2>&1; then
        binary_name="${BINARY_NAME}.exe"
    fi
    
    if command -v "$binary_name" >/dev/null 2>&1; then
        "$binary_name" --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1
    else
        echo ""
    fi
}

# Update mode function
update_existing_installation() {
    print_step "$(text "update_checking")..."
    
    local current_version=$(get_current_version)
    
    if [[ -z "$current_version" ]]; then
        print_warning "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Không thể xác định phiên bản hiện tại. Tiến hành cài đặt mới"; else echo "Cannot determine current version. Proceeding with fresh installation"; fi)."
        UPDATE_MODE=false
        return 1
    fi
    
    print_info "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Phiên bản hiện tại"; else echo "Current version"; fi): $current_version"
    print_info "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Phiên bản mới"; else echo "New version"; fi): $VERSION"
    
    # Simple version comparison
    if [[ "$current_version" == "$VERSION" ]]; then
        print_warning "$(text "update_same_version" "$current_version")"
        
        local force_update=""
        if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
            force_update=$(read_input "Bạn có muốn cài đặt lại? (y/n) [n]: " "n")
        else
            force_update=$(read_input "Do you want to reinstall anyway? (y/n) [n]: " "n")
        fi
        
        if [[ "$force_update" != "y" ]] && [[ "$force_update" != "yes" ]]; then
            print_info "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Hủy cập nhật"; else echo "Update cancelled"; fi)."
            exit 0
        fi
    else
        print_info "$(text "update_from_to" "$current_version" "$VERSION")"
    fi
    
    return 0
}

post_install_setup() {
    print_info "$(text "post_install")..."
    
    local tool_found=false
    
    if command -v "$BINARY_NAME" >/dev/null 2>&1; then
        tool_found=true
    elif is_windows && command -v "${BINARY_NAME}.exe" >/dev/null 2>&1; then
        tool_found=true
    else
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
        print_success "$(text "tool_ready")"
        print_info "$(text "run_settings")."
        print_info "$(text "run_help")."
    else
        print_warning "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Xác minh công cụ thất bại. Bạn có thể cần khởi động lại shell"; else echo "Tool verification failed. You may need to restart your shell"; fi)."
        if is_windows; then
            print_info "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Thử một trong những lệnh này"; else echo "Try one of these commands"; fi):"
            print_info "  - $(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Khởi động lại Git Bash"; else echo "Restart Git Bash"; fi)"
            print_info "  - $(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Chạy"; else echo "Run"; fi) 'source ~/.bash_profile' $(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "hoặc"; else echo "or"; fi) 'source ~/.bashrc'"
            print_info "  - $(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Thêm vào PATH thủ công"; else echo "Add to PATH manually"; fi): export PATH=\"\$HOME/.local/bin:\$PATH\""
        else
            print_info "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Chạy 'source ~/.bashrc' hoặc khởi động lại terminal"; else echo "Run 'source ~/.bashrc' or restart your terminal"; fi)."
        fi
    fi
}

# Show detailed command guide
show_command_guide() {
    echo -e "\n${WHITE}${BOLD}╔══════════════════════════════════════════════════════════════════════════════╗${RESET}"
    if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
        echo -e "${WHITE}${BOLD}║                          📖 HƯỚNG DẪN SỬ DỤNG CHI TIẾT                      ║${RESET}"
    else
        echo -e "${WHITE}${BOLD}║                           📖 DETAILED COMMAND GUIDE                         ║${RESET}"
    fi
    echo -e "${WHITE}${BOLD}╚══════════════════════════════════════════════════════════════════════════════╝${RESET}\n"
    
    if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
        echo -e "${CYAN}${BOLD}🚀 CÁC LỆNH CƠ BẢN:${RESET}"
        echo -e "${GREEN}  dev_tool --help${RESET}                 - Hiển thị trợ giúp"
        echo -e "${GREEN}  dev_tool --version${RESET}              - Kiểm tra phiên bản"
        echo -e "${GREEN}  dev_tool settings${RESET}               - Cấu hình cài đặt"
        echo ""
        echo -e "${CYAN}${BOLD}💬 TẠO COMMIT MESSAGE:${RESET}"
        echo -e "${GREEN}  dev_tool .${RESET}                 - Tạo commit message tự động"
        echo ""
        echo -e "${YELLOW}${BOLD}📋 VÍ DỤ SỬ DỤNG:${RESET}"
        echo -e "${DIM}  # Tạo commit tự động"
        echo -e "  git add ."
        echo -e "  dev_tool ."
    else
        echo -e "${CYAN}${BOLD}🚀 BASIC COMMANDS:${RESET}"
        echo -e "${GREEN}  dev_tool --help${RESET}                 - Show help information"
        echo -e "${GREEN}  dev_tool --version${RESET}              - Check version"
        echo -e "${GREEN}  dev_tool settings${RESET}               - Configure settings"
        echo ""
        echo -e "${CYAN}${BOLD}💬 COMMIT MESSAGE GENERATION:${RESET}"
        echo -e "${GREEN}  dev_tool commit${RESET}                 - Generate automatic commit message"
        echo -e "${GREEN}  dev_tool commit -m \"message\"${RESET}   - Commit with custom message"
        echo -e "${GREEN}  dev_tool commit --interactive${RESET}    - Interactive mode"
        echo ""
        echo -e "${CYAN}${BOLD}🔧 REPOSITORY MANAGEMENT:${RESET}"
        echo -e "${GREEN}  dev_tool init${RESET}                   - Initialize new repository"
        echo -e "${GREEN}  dev_tool status${RESET}                 - View repository status"
        echo -e "${GREEN}  dev_tool log${RESET}                    - View commit history"
        echo ""
        echo -e "${CYAN}${BOLD}🌟 ADVANCED FEATURES:${RESET}"
        echo -e "${GREEN}  dev_tool analyze${RESET}                - Analyze source code"
        echo -e "${GREEN}  dev_tool review${RESET}                 - Review code changes"
        echo -e "${GREEN}  dev_tool optimize${RESET}               - Optimize repository"
        echo ""
        echo -e "${CYAN}${BOLD}⚙️  CONFIGURATION:${RESET}"
        echo -e "${GREEN}  dev_tool config set <key> <value>${RESET} - Set configuration"
        echo -e "${GREEN}  dev_tool config get <key>${RESET}        - Get configuration value"
        echo -e "${GREEN}  dev_tool config list${RESET}             - List all configurations"
        echo ""
        echo -e "${YELLOW}${BOLD}📋 USAGE EXAMPLES:${RESET}"
        echo -e "${DIM}  # Auto-generate commit"
        echo -e "  git add ."
        echo -e "  dev_tool commit"
        echo ""
        echo -e "  # Configure AI provider"
        echo -e "  dev_tool config set ai.provider openai"
        echo -e "  dev_tool config set ai.api_key your-api-key${RESET}"
    fi
    
    echo ""
    if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
        echo -e "${MAGENTA}${BOLD}💡 MẸO:${RESET} ${MAGENTA}Sử dụng tab completion để tự động hoàn thành lệnh${RESET}"
        echo -e "${MAGENTA}${BOLD}🆘 HỖ TRỢ:${RESET} ${MAGENTA}Truy cập $REPO_URL để biết thêm chi tiết${RESET}"
        echo -e "${MAGENTA}${BOLD}📧 LIÊN HỆ:${RESET} ${MAGENTA}$CONTACT cho hỗ trợ kỹ thuật${RESET}"
    else
        echo -e "${MAGENTA}${BOLD}💡 TIP:${RESET} ${MAGENTA}Use tab completion for command auto-completion${RESET}"
        echo -e "${MAGENTA}${BOLD}🆘 SUPPORT:${RESET} ${MAGENTA}Visit $REPO_URL for more details${RESET}"
        echo -e "${MAGENTA}${BOLD}📧 CONTACT:${RESET} ${MAGENTA}$CONTACT for technical support${RESET}"
    fi
    echo ""
}

# Enhanced progress bar function
show_progress() {
    local current="$1"
    local total="$2"
    local message="$3"
    local width=50
    local percentage=$((current * 100 / total))
    local completed=$((current * width / total))
    local remaining=$((width - completed))
    
    printf "\r${CYAN}${BOLD}%s${RESET} [" "$message"
    printf "${GREEN}%*s" "$completed" | tr ' ' '█'
    printf "${DIM}%*s" "$remaining" | tr ' ' '░'
    printf "${RESET}] ${WHITE}${BOLD}%d%%${RESET}" "$percentage"
    
    if [[ $current -eq $total ]]; then
        echo ""
    fi
}

# Show installation summary
show_installation_summary() {
    echo ""
    echo -e "${WHITE}${BOLD}╔══════════════════════════════════════════════════════════════════════════════╗${RESET}"
    if [[ "$UPDATE_MODE" == true ]]; then
        if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
            echo -e "${WHITE}${BOLD}║                           📋 TÓM TẮT CẬP NHẬT                               ║${RESET}"
        else
            echo -e "${WHITE}${BOLD}║                            📋 UPDATE SUMMARY                               ║${RESET}"
        fi
    else
        if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
            echo -e "${WHITE}${BOLD}║                           📋 TÓM TẮT CÀI ĐẶT                                ║${RESET}"
        else
            echo -e "${WHITE}${BOLD}║                          📋 INSTALLATION SUMMARY                            ║${RESET}"
        fi
    fi
    echo -e "${WHITE}${BOLD}╚══════════════════════════════════════════════════════════════════════════════╝${RESET}"
    echo ""
    
    local final_binary="$BINARY_NAME"
    if is_windows && ! command -v "$BINARY_NAME" >/dev/null 2>&1 && command -v "${BINARY_NAME}.exe" >/dev/null 2>&1; then
        final_binary="${BINARY_NAME}.exe"
    fi
    
    if command -v "$final_binary" >/dev/null 2>&1; then
        local final_version=$("$final_binary" --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "$VERSION")
        
        if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
            if [[ "$UPDATE_MODE" == true ]]; then
                echo -e "${GREEN}✅ Trạng thái:${RESET}        Cập nhật thành công"
            else
                echo -e "${GREEN}✅ Trạng thái:${RESET}        Cài đặt thành công"
            fi
            echo -e "${BLUE}📦 Phiên bản:${RESET}         $final_version"
            echo -e "${CYAN}📁 Vị trí:${RESET}            $(which "$final_binary")"
            echo -e "${YELLOW}🛠️  Công cụ:${RESET}           $TOOL_NAME"
            echo -e "${MAGENTA}👨‍💻 Nhà phát triển:${RESET}    $DEVELOPER"
        else
            if [[ "$UPDATE_MODE" == true ]]; then
                echo -e "${GREEN}✅ Status:${RESET}            Successfully updated"
            else
                echo -e "${GREEN}✅ Status:${RESET}            Successfully installed"
            fi
            echo -e "${BLUE}📦 Version:${RESET}           $final_version"
            echo -e "${CYAN}📁 Location:${RESET}          $(which "$final_binary")"
            echo -e "${YELLOW}🛠️  Tool:${RESET}             $TOOL_NAME"
            echo -e "${MAGENTA}👨‍💻 Developer:${RESET}        $DEVELOPER"
        fi
    else
        if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
            if [[ "$UPDATE_MODE" == true ]]; then
                echo -e "${YELLOW}⚠️  Trạng thái:${RESET}        Cập nhật hoàn tất, cần xác minh"
            else
                echo -e "${YELLOW}⚠️  Trạng thái:${RESET}        Cài đặt hoàn tất, cần xác minh"
            fi
            echo -e "${BLUE}📦 Phiên bản:${RESET}         $VERSION"
            echo -e "${CYAN}📁 Vị trí dự kiến:${RESET}    $(get_install_directory)/$BINARY_NAME"
        else
            if [[ "$UPDATE_MODE" == true ]]; then
                echo -e "${YELLOW}⚠️  Status:${RESET}            Update complete, verification needed"
            else
                echo -e "${YELLOW}⚠️  Status:${RESET}            Installation complete, verification needed"
            fi
            echo -e "${BLUE}📦 Version:${RESET}           $VERSION"
            echo -e "${CYAN}📁 Expected location:${RESET} $(get_install_directory)/$BINARY_NAME"
        fi
    fi
    
    echo ""
    if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
        echo -e "${WHITE}${BOLD}🎯 BƯỚC TIẾP THEO:${RESET}"
        echo -e "${CYAN}  1.${RESET} Khởi động lại terminal hoặc chạy: ${GREEN}source ~/.bashrc${RESET}"
        echo -e "${CYAN}  2.${RESET} Kiểm tra cài đặt: ${GREEN}$final_binary --version${RESET}"
        echo -e "${CYAN}  3.${RESET} Xem hướng dẫn: ${GREEN}$final_binary --help${RESET}"
        echo -e "${CYAN}  4.${RESET} Cấu hình công cụ: ${GREEN}$final_binary settings${RESET}"
    else
        echo -e "${WHITE}${BOLD}🎯 NEXT STEPS:${RESET}"
        echo -e "${CYAN}  1.${RESET} Restart terminal or run: ${GREEN}source ~/.bashrc${RESET}"
        echo -e "${CYAN}  2.${RESET} Verify installation: ${GREEN}$final_binary --version${RESET}"
        echo -e "${CYAN}  3.${RESET} View help: ${GREEN}$final_binary --help${RESET}"
        echo -e "${CYAN}  4.${RESET} Configure tool: ${GREEN}$final_binary settings${RESET}"
    fi
    echo ""
}

# Enhanced main installation function
main() {
    # Process command line arguments first
    process_arguments "$@"
    
    # Detect and optionally change language
    detect_language
    
    # Show language selection if not explicitly set and not in update mode
    if [[ -z "$DEV_TOOL_LANG" ]] && [[ "$UPDATE_MODE" == false ]]; then
        show_language_menu
    fi
    
    print_header
    
    # Handle update mode
    if [[ "$UPDATE_MODE" == true ]]; then
        if ! update_existing_installation; then
            # Fall back to normal installation if update fails
            UPDATE_MODE=false
        fi
    fi
    
    # Platform detection with progress
    show_progress 1 5 "$(text "detecting_platform")"
    local platform=$(detect_platform)
    if is_windows; then
        print_info "$(text "detecting_platform"): $platform ($(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Môi trường Windows"; else echo "Windows environment"; fi))"
    else
        print_info "$(text "detecting_platform"): $platform"
    fi
    
    # Check system requirements with progress
    show_progress 2 5 "$(text "checking_requirements")"
    check_requirements
    
    # Check if already installed (skip if in update mode)
    show_progress 3 5 "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Kiểm tra cài đặt hiện tại"; else echo "Checking current installation"; fi)"
    if [[ "$UPDATE_MODE" == false ]]; then
        local tool_exists=false
        if command -v "$BINARY_NAME" >/dev/null 2>&1; then
            tool_exists=true
        elif is_windows && command -v "${BINARY_NAME}.exe" >/dev/null 2>&1; then
            tool_exists=true
            BINARY_NAME="${BINARY_NAME}.exe"
        fi
        
        if $tool_exists; then
            local current_version=$("$BINARY_NAME" --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "unknown")
            
            if [[ -z "$current_version" ]]; then
                current_version=$("$BINARY_NAME" --version 2>/dev/null || echo "unknown")
                current_version=$(echo "$current_version" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
            fi
            
            if [[ -z "$current_version" ]]; then
                current_version="unknown"
            fi
            
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                print_warning "$TOOL_NAME đã được cài đặt (phiên bản: $current_version)"
                print_info "Đang tiến hành cài đặt lại với phiên bản $VERSION"
            else
                print_warning "$TOOL_NAME is already installed (version: $current_version)"
                print_info "Proceeding with reinstallation of version $VERSION"
            fi
        else
            print_info "$(text "not_installed")."
            print_info "$(text "installing_version")..."
        fi
    else
        if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
            print_info "Chế độ cập nhật: Đang cập nhật lên phiên bản $VERSION"
        else
            print_info "Update mode: Updating to version $VERSION"
        fi
    fi
    
    # Installation process
    show_progress 4 5 "$(if [[ "$UPDATE_MODE" == true ]]; then
        if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Đang cập nhật"; else echo "Updating"; fi
    else
        if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Đang cài đặt"; else echo "Installing"; fi
    fi)"
    
    if ! check_go_installation; then
        install_go
    fi
    
    print_info "$(text "building_source")..."
    build_from_source
    
    # Final setup
    show_progress 5 5 "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Hoàn tất"; else echo "Finalizing"; fi)"
    post_install_setup
    
    # Show success message
    echo ""
    if [[ "$UPDATE_MODE" == true ]]; then
        print_success "$(text "update_success")"
    else
        print_success "$(text "install_complete")"
    fi
    
    # Show installation summary
    show_installation_summary
    
    # Show command guide (skip for update mode unless explicitly requested)
    local show_guide=""
    if [[ "$UPDATE_MODE" == false ]]; then
        if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
            show_guide=$(read_input "Bạn có muốn xem hướng dẫn sử dụng chi tiết? (y/n) [y]: " "y")
        else
            show_guide=$(read_input "Would you like to see the detailed command guide? (y/n) [y]: " "y")
        fi
        
        if [[ "$show_guide" != "n" ]] && [[ "$show_guide" != "no" ]]; then
            show_command_guide
        fi
    fi
    
    # Final message
    echo ""
    local final_binary="$BINARY_NAME"
    if is_windows && ! command -v "$BINARY_NAME" >/dev/null 2>&1 && command -v "${BINARY_NAME%.exe}.exe" >/dev/null 2>&1; then
        final_binary="${BINARY_NAME%.exe}.exe"
    fi
    
    if command -v "${final_binary%.exe}" >/dev/null 2>&1 || command -v "$final_binary" >/dev/null 2>&1; then
        local final_version=$("${final_binary%.exe}" --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "$VERSION")
        print_highlight "$(text "version_ready" "$final_version")"
    fi
    
    # Platform-specific instructions
    if is_windows; then
        echo ""
        if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
            print_info "📝 Hướng dẫn cho Windows:"
            print_info "   - Bạn có thể cần khởi động lại Git Bash hoặc terminal"
            print_info "   - Hoặc chạy: source ~/.bash_profile (hoặc ~/.bashrc)"
            print_info "   - Nếu vẫn không tìm thấy, thêm thủ công: export PATH=\"\$HOME/.local/bin:\$PATH\""
            print_info "   - Xác minh bằng: ${final_binary%.exe} --help"
        else
            print_info "📝 Windows-specific instructions:"
            print_info "   - You may need to restart Git Bash or your terminal"
            print_info "   - Or run: source ~/.bash_profile (or ~/.bashrc)"
            print_info "   - If still not found, add manually: export PATH=\"\$HOME/.local/bin:\$PATH\""
            print_info "   - Verify with: ${final_binary%.exe} --help"
        fi
    else
        print_info "$(text "restart_terminal")."
    fi
    
    print_info "$(text "get_started")"
    
    # Thank you message
    echo ""
    if [[ "$UPDATE_MODE" == true ]]; then
        if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
            print_highlight "🙏 Cảm ơn bạn đã cập nhật Dev Tool! Chúc bạn coding vui vẻ!"
        else
            print_highlight "🙏 Thank you for updating Dev Tool! Happy coding!"
        fi
    else
        if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
            print_highlight "🙏 Cảm ơn bạn đã sử dụng Dev Tool! Chúc bạn coding vui vẻ!"
        else
            print_highlight "🙏 Thank you for using Dev Tool! Happy coding!"
        fi
    fi
    echo ""
}

# Uninstall function
uninstall() {
    if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
        print_info "Đang gỡ cài đặt $TOOL_NAME..."
    else
        print_info "Uninstalling $TOOL_NAME..."
    fi
    
    local binary_locations=(
        "/usr/local/bin/${BINARY_NAME}"
        "$HOME/.local/bin/${BINARY_NAME}"
        "/usr/bin/${BINARY_NAME}"
    )
    
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
            if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
                print_success "Đã xóa $location"
            else
                print_success "Removed $location"
            fi
            found=true
        fi
    done
    
    if [[ "$found" == false ]]; then
        if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
            print_warning "Không tìm thấy binary trong các vị trí tiêu chuẩn"
        else
            print_warning "Binary not found in standard locations"
        fi
    fi
    
    if command -v "$BINARY_NAME" >/dev/null 2>&1; then
        "$BINARY_NAME" settings
    fi
    
    if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
        print_success "Gỡ cài đặt hoàn tất"
    else
        print_success "Uninstallation completed"
    fi
}

# Run main function
main "$@"