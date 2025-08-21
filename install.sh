#!/bin/bash

# Dev Tool - AI-powered Git Commit Message Generator
# Enhanced Cross-platform installer with bilingual support
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
VERSION="2.0.7"
REPO_URL="https://github.com/KhanhRomVN/dev_tool"
BINARY_NAME="dev_tool"
DEVELOPER="KhanhRomVN"
CONTACT="khanhromvn@gmail.com"

# Language support
LANG_EN="en"
LANG_VI="vi"
CURRENT_LANG="$LANG_EN"

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
    echo "║                          🛠️  $(text "header_title")                           ║"
    echo "║                        $(text "header_subtitle")                        ║"
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
    local input=""
    
    if [ -t 0 ]; then
        read -p "$prompt" input
    elif [ -r /dev/tty ]; then
        read -p "$prompt" input < /dev/tty
    else
        print_warning "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Không thể đọc input, sử dụng mặc định"; else echo "Cannot read input, using default"; fi): $default"
        input="$default"
    fi
    
    echo "$input"
}

check_go_installation() {
    if command -v go >/dev/null 2>&1; then
        local go_version=$(go version | awk '{print $3}' | sed 's/go//')
        print_success "$(text "go_found"): version $go_version"
        return 0
    else
        print_warning "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Go chưa được cài đặt trên hệ thống này"; else echo "Go is not installed on this system"; fi)"
        return 1
    fi
}

build_from_source() {
    print_step "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Đang build $TOOL_NAME từ mã nguồn"; else echo "Building $TOOL_NAME from source"; fi)..."
    
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
    go mod tidy
    
    local binary_name="$BINARY_NAME"
    if is_windows; then
        binary_name="${BINARY_NAME}.exe"
    fi
    
    go build -o "$binary_name" .
    go build -o "dev_tool_v${VERSION}" .
    
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
    if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
        echo -e "${WHITE}${BOLD}║                           📋 TÓM TẮT CÀI ĐẶT                                ║${RESET}"
    else
        echo -e "${WHITE}${BOLD}║                          📋 INSTALLATION SUMMARY                            ║${RESET}"
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
            echo -e "${GREEN}✅ Trạng thái:${RESET}        Cài đặt thành công"
            echo -e "${BLUE}📦 Phiên bản:${RESET}         $final_version"
            echo -e "${CYAN}📁 Vị trí:${RESET}            $(which "$final_binary")"
            echo -e "${YELLOW}🛠️  Công cụ:${RESET}           $TOOL_NAME"
            echo -e "${MAGENTA}👨‍💻 Nhà phát triển:${RESET}    $DEVELOPER"
        else
            echo -e "${GREEN}✅ Status:${RESET}            Successfully installed"
            echo -e "${BLUE}📦 Version:${RESET}           $final_version"
            echo -e "${CYAN}📁 Location:${RESET}          $(which "$final_binary")"
            echo -e "${YELLOW}🛠️  Tool:${RESET}             $TOOL_NAME"
            echo -e "${MAGENTA}👨‍💻 Developer:${RESET}        $DEVELOPER"
        fi
    else
        if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
            echo -e "${YELLOW}⚠️  Trạng thái:${RESET}        Cài đặt hoàn tất, cần xác minh"
            echo -e "${BLUE}📦 Phiên bản:${RESET}         $VERSION"
            echo -e "${CYAN}📁 Vị trí dự kiến:${RESET}    $(get_install_directory)/$BINARY_NAME"
        else
            echo -e "${YELLOW}⚠️  Status:${RESET}            Installation complete, verification needed"
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
    # Detect and optionally change language
    detect_language
    
    # Show language selection if not explicitly set
    if [[ -z "$DEV_TOOL_LANG" ]]; then
        show_language_menu
    fi
    
    print_header
    
    # Check for uninstall flag
    if [[ "$1" == "--uninstall" ]]; then
        uninstall
        exit 0
    fi
    
    # Show command guide if requested
    if [[ "$1" == "--help" ]] || [[ "$1" == "--guide" ]]; then
        show_command_guide
        exit 0
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
    
    # Check if already installed
    show_progress 3 5 "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Kiểm tra cài đặt hiện tại"; else echo "Checking current installation"; fi)"
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
    
    # Installation process
    show_progress 4 5 "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Đang cài đặt"; else echo "Installing"; fi)"
    
    if ! check_go_installation; then
        if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
            print_error "Go không được tìm thấy. Vui lòng cài đặt Go từ https://golang.org/dl/"
        else
            print_error "Go not found. Please install Go from https://golang.org/dl/"
        fi
        exit 1
    else
        print_info "$(text "building_source")..."
        build_from_source
    fi
    
    # Final setup
    show_progress 5 5 "$(if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then echo "Hoàn tất"; else echo "Finalizing"; fi)"
    post_install_setup
    
    # Show success message
    echo ""
    print_success "$(text "install_complete")"
    
    # Show installation summary
    show_installation_summary
    
    # Show command guide
    local show_guide=""
    if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
        show_guide=$(read_input "Bạn có muốn xem hướng dẫn sử dụng chi tiết? (y/n) [y]: " "y")
    else
        show_guide=$(read_input "Would you like to see the detailed command guide? (y/n) [y]: " "y")
    fi
    
    if [[ "$show_guide" != "n" ]] && [[ "$show_guide" != "no" ]]; then
        show_command_guide
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
    if [[ "$CURRENT_LANG" == "$LANG_VI" ]]; then
        print_highlight "🙏 Cảm ơn bạn đã sử dụng Dev Tool! Chúc bạn coding vui vẻ!"
    else
        print_highlight "🙏 Thank you for using Dev Tool! Happy coding!"
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