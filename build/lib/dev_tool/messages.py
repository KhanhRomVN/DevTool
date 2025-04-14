#!/usr/bin/env python3
from typing import Dict

# ANSI color codes
COLORS = {
    'BLUE': '\033[94m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'RED': '\033[91m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
    'END': '\033[0m'
}

# Translations for UI messages
MESSAGES = {
    'en': {
        'welcome': "Developer Tool Configuration",
        'enter_api_key': "Please enter your Gemini API key:",
        'choose_model': "Choose your preferred model:",
        'model_1': "Gemini 2.0 Flash (recommended) - Advanced features, speed",
        'model_2': "Gemini 2.0 Flash-Lite - Cost-effective, low latency",
        'choose_ui_lang': "Choose interface language:",
        'lang_1': "English",
        'lang_2': "Tiếng Việt",
        'choose_commit_lang': "Choose commit message language:",
        'choose_auto_push': "Enable automatic push after commit? (y/N):",
        'choose_auto_review': "Enable automatic code review? (Y/n):",
        'invalid_choice': "Invalid choice. Please enter 1 or 2.",
        'config_saved': "Configuration saved successfully!",
        'performing_review': "Performing code review...",
        'proceed_commit': "Do you want to proceed with the commit? (y/N):",
        'commit_cancelled': "Commit cancelled. Please review and fix the issues.",
        'no_changes': "No staged changes found. Use 'git add' to stage your changes.",
        'commit_success': "Changes committed successfully!",
        'push_success': "Changes pushed successfully!",
        'git_error': "Error during git operations:",
        'review_error': "Error performing code review:",
        'generated_msg': "Generated commit message:",
        'config_menu': """
Configuration Menu:
1) Change interface language
2) Change commit message language
3) Update Gemini API key
4) Change AI model
5) Configure auto-push
6) Configure auto-review
7) Save and exit
""",
        'current_config': "Current configuration:",
        'ui_lang': "Interface language",
        'commit_lang': "Commit language",
        'auto_push': "Auto-push",
        'auto_review': "Auto-review",
        'enabled': "Enabled",
        'disabled': "Disabled",
        'select_option': "Select an option (1-7):",
        'invalid_option': "Invalid option. Please try again.",
        'save_exit': "Configuration saved. Exiting...",
        'help_text': """
| 🛠️  Developer Tool Help
| =====================

| Available Commands:
| -----------------
| dev_tool help                     Show this help message
| dev_tool config                   Configure tool settings
| dev_tool auto-commit             Generate commit message and handle git operations
| dev_tool flutter                 Flutter development tools and utilities

| Auto-commit Options:
| ------------------
| --no-push                   Skip automatic push after commit
| --no-review                 Skip code review before commit

| Configuration Options:
| -------------------
| - Interface language (English/Vietnamese)
| - Commit message language
| - AI model selection
| - Auto-push settings
| - Auto-review settings
| - Gemini API key

| Examples:
| --------
| dev_tool auto-commit             Normal commit with review and push
| dev_tool auto-commit --no-push   Commit without pushing
| dev_tool config                  Open configuration menu
| dev_tool help                    Show this help message

| For more information, visit: https://github.com/KhanhRomVN/dev_tool
"""
    },
    'vi': {
        'welcome': "Cấu Hình Developer Tool",
        'enter_api_key': "Vui lòng nhập Gemini API key của bạn:",
        'choose_model': "Chọn model bạn muốn sử dụng:",
        'model_1': "Gemini 2.0 Flash (khuyến nghị) - Tính năng nâng cao, tốc độ nhanh",
        'model_2': "Gemini 2.0 Flash-Lite - Tiết kiệm, độ trễ thấp",
        'choose_ui_lang': "Chọn ngôn ngữ giao diện:",
        'lang_1': "Tiếng Anh",
        'lang_2': "Tiếng Việt",
        'choose_commit_lang': "Chọn ngôn ngữ cho commit message:",
        'choose_auto_push': "Bật tự động push sau khi commit? (y/N):",
        'choose_auto_review': "Bật tự động review code? (Y/n):",
        'invalid_choice': "Lựa chọn không hợp lệ. Vui lòng nhập 1 hoặc 2.",
        'config_saved': "Đã lưu cấu hình thành công!",
        'performing_review': "Đang thực hiện code review...",
        'proceed_commit': "Bạn có muốn tiếp tục commit không? (y/N):",
        'commit_cancelled': "Đã hủy commit. Vui lòng xem xét và sửa các vấn đề.",
        'no_changes': "Không tìm thấy thay đổi nào. Sử dụng 'git add' để stage các thay đổi.",
        'commit_success': "Đã commit thay đổi thành công!",
        'push_success': "Đã push code thành công!",
        'git_error': "Lỗi trong quá trình thực hiện git:",
        'review_error': "Lỗi khi thực hiện code review:",
        'generated_msg': "Commit message đã tạo:",
        'config_menu': """
Menu Cấu Hình:
1) Thay đổi ngôn ngữ giao diện
2) Thay đổi ngôn ngữ commit message
3) Cập nhật Gemini API key
4) Thay đổi model AI
5) Cấu hình tự động push
6) Cấu hình tự động review
7) Lưu và thoát
""",
        'current_config': "Cấu hình hiện tại:",
        'ui_lang': "Ngôn ngữ giao diện",
        'commit_lang': "Ngôn ngữ commit",
        'auto_push': "Tự động push",
        'auto_review': "Tự động review",
        'enabled': "Bật",
        'disabled': "Tắt",
        'select_option': "Chọn một tùy chọn (1-7):",
        'invalid_option': "Tùy chọn không hợp lệ. Vui lòng thử lại.",
        'save_exit': "Đã lưu cấu hình. Đang thoát...",
        'help_text': """
| 🛠️  Developer Tool - Trợ Giúp
| ============================

| Các Lệnh Có Sẵn:
| ---------------
| dev_tool help                     Hiển thị trợ giúp này
| dev_tool config                   Cấu hình thiết lập
| dev_tool auto-commit             Tạo commit message và xử lý git
| dev_tool flutter                 Công cụ và tiện ích phát triển Flutter

| Tùy Chọn Auto-commit:
| -------------------
| --no-push                   Bỏ qua tự động push sau khi commit
| --no-review                 Bỏ qua review code trước khi commit

| Tùy Chọn Cấu Hình:
| ----------------
| - Ngôn ngữ giao diện (Tiếng Anh/Tiếng Việt)
| - Ngôn ngữ commit message
| - Lựa chọn model AI
| - Cài đặt tự động push
| - Cài đặt tự động review
| - Gemini API key

| Ví Dụ Sử Dụng:
| ------------
| dev_tool auto-commit             Commit bình thường với review và push
| dev_tool auto-commit --no-push   Commit không push
| dev_tool config                  Mở menu cấu hình
| dev_tool help                    Hiển thị trợ giúp này

| Để biết thêm thông tin, truy cập: https://github.com/KhanhRomVN/dev_tool
"""
    }
}

def print_header(text: str, color: str = 'BLUE') -> None:
    """Print a formatted header."""
    print(f"\n{COLORS[color]}{COLORS['BOLD']}{text}{COLORS['END']}")
    print("=" * 50)

def print_section(text: str, color: str = 'GREEN') -> None:
    """Print a formatted section header."""
    print(f"\n{COLORS[color]}{text}{COLORS['END']}")

def print_error(text: str) -> None:
    """Print an error message."""
    print(f"{COLORS['RED']}{text}{COLORS['END']}")

def get_message(key: str, config: Dict) -> str:
    """Get a translated message based on UI language."""
    return MESSAGES[config['ui_language']][key]

def show_current_config(config: Dict) -> None:
    """Display current configuration settings."""
    print_section(get_message('current_config', config))
    print(f"{COLORS['YELLOW']}{get_message('ui_lang', config)}:{COLORS['END']} " + 
          ("English" if config['ui_language'] == 'en' else "Tiếng Việt"))
    print(f"{COLORS['YELLOW']}{get_message('commit_lang', config)}:{COLORS['END']} " + 
          ("English" if config['commit_language'] == 'en' else "Tiếng Việt"))
    print(f"{COLORS['YELLOW']}{get_message('auto_push', config)}:{COLORS['END']} " + 
          (get_message('enabled', config) if config['auto_push'] else get_message('disabled', config)))
    print(f"{COLORS['YELLOW']}{get_message('auto_review', config)}:{COLORS['END']} " + 
          (get_message('enabled', config) if config['auto_review'] else get_message('disabled', config)))