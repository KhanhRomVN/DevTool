# dev_tool/messages.py
#!/usr/bin/env python3
import platform
from typing import Dict

# ANSI color codes with fallback for Windows
def get_colors():
    system = platform.system().lower()
    if system == "windows":
        try:
            import colorama
            colorama.init()
        except ImportError:
            pass
    
    return {
        'BLUE': '\033[94m',
        'GREEN': '\033[92m',
        'YELLOW': '\033[93m',
        'RED': '\033[91m',
        'PURPLE': '\033[95m',
        'CYAN': '\033[96m',
        'WHITE': '\033[97m',
        'BOLD': '\033[1m',
        'UNDERLINE': '\033[4m',
        'DIM': '\033[2m',
        'END': '\033[0m'
    }

COLORS = get_colors()

# Enhanced translations with more comprehensive messages
MESSAGES = {
    'en': {
        'welcome': "Dev Tool - AI Git Assistant",
        'enter_api_key': "Enter your Gemini API key",
        'add_first_account': "Add your first Gemini account",
        'choose_model': "Choose your preferred AI model",
        'model_1': "Gemini 2.5 Pro - Most advanced (Recommended)",
        'model_2': "Gemini 2.5 Flash - Fast and capable",
        'model_3': "Gemini 2.5 Flash-Lite - Lightweight and efficient",
        'model_4': "Gemini 2.0 Flash - Legacy model",
        'choose_ui_lang': "Choose interface language",
        'lang_1': "English",
        'lang_2': "Tiếng Việt",
        'choose_commit_lang': "Choose commit message language",
        'choose_commit_style': "Choose commit message style",
        'choose_auto_stage': "Enable automatic staging (git add .)? (y/N)",
        'choose_auto_push': "Enable automatic push after commit? (y/N)",
        'invalid_choice': "❌ Invalid choice. Please try again.",
        'config_saved': "✅ Configuration saved successfully!",
        'no_changes': "❌ No staged changes found. Use 'git add' to stage your changes.",
        'analyzing_changes': "🔍 Analyzing your changes...",
        'generated_msg': "📝 Generated commit message",
        'proceed_commit': "🚀 Proceed with commit? (y/N)",
        'commit_cancelled': "❌ Commit cancelled.",
        'commit_success': "✅ Changes committed successfully!",
        'push_success': "🚀 Changes pushed successfully!",
        'git_error': "❌ Git operation failed",
        'review_error': "❌ Code review failed",
        'settings_menu': "⚙️  Settings Menu",
        'current_config': "📋 Current Configuration",
        'ui_lang': "Interface Language",
        'commit_lang': "Commit Language", 
        'commit_style': "Commit Style",
        'auto_push': "Auto Push",
        'auto_stage': "Auto Stage",
        'enabled': "Enabled",
        'disabled': "Disabled",
        'select_option': "Select an option",
        'invalid_option': "❌ Invalid option. Please try again.",
        'save_exit': "💾 Configuration saved successfully!",
        'reset_confirm': "⚠️  This will reset all settings to defaults. Continue?",
        'reset_success': "🔄 Settings reset successfully!",
        'uninstall_confirm': "⚠️  This will completely remove dev_tool. Continue?",
        'uninstall_success': "✅ dev_tool uninstalled successfully!",
        'back_to_menu': "⬅️  Back to menu",
        'exit': "🚪 Exit",
        'account_manager': "👥 Account Manager",
        'add_account': "➕ Add Account",
        'edit_account': "✏️ Edit Account",
        'delete_account': "🗑️ Delete Account",
        'set_primary': "⭐ Set as Primary",
        'no_accounts': "❌ No accounts configured",
        'account_email': "📧 Email",
        'account_model': "🤖 Model",
        'account_status': "🔑 Status",
        'primary': "⭐ Primary",
        'secondary': "🔑 Secondary",
        'help_text': """
🛠️  Dev Tool - AI Git Assistant
================================

📚 Available Commands:
  dev_tool              Generate AI commit message and commit
  dev_tool --no-push    Commit without pushing to remote
  dev_tool settings     Open settings menu
  dev_tool --version    Show version information

⚙️  Settings Menu Options:
  Edit Configuration    Modify language, model, and preferences
  Account Manager       Manage multiple Gemini accounts
  Reset to Defaults     Reset all settings to initial state
  Uninstall Tool        Completely remove dev_tool

🎨 Commit Styles:
  Conventional          feat: add user authentication
  Emoji                 ✨ add user authentication  
  Descriptive           Add comprehensive user authentication system

🌍 Supported Languages:
  Interface: English, Vietnamese
  Commits: English, Vietnamese

🤖 Supported Models:
  Gemini 2.5 Pro        Most advanced model (recommended)
  Gemini 2.5 Flash      Fast and capable
  Gemini 2.5 Flash-Lite Lightweight and efficient
  Gemini 2.0 Flash      Legacy model

📖 For more help: https://github.com/your-repo/dev_tool
        """,
        'edit_config': "Edit Configuration",
        'reset_defaults': "Reset to Defaults",
        'uninstall_tool': "Uninstall Tool",
        'help_info': "Help & Information",
        'options': "Options",
        'change_ui_lang': "Change Interface Language",
        'change_commit_lang': "Change Commit Language",
        'update_api_key': "Update API Key",
        'change_ai_model': "Change AI Model",
        'change_commit_style': "Change Commit Style",
        'toggle_auto_push': "Toggle Auto Push",
        'save_back': "Save & Back to Menu",
        'back_no_save': "Back without Saving",
        'edit_options': "Edit Options",
        'available_langs': "Available Languages",
        'select_lang': "Select language",
        'enter_api_key_prompt': "Enter new API key",
        'available_models': "Available Models",
        'select_model': "Select model",
        'available_styles': "Available Styles",
        'select_style': "Select style",
        'confirm_toggle': "Do you want to",
        'enable': "enable",
        'disable': "disable",
        'press_enter_continue': "Press Enter to continue"
    },
    'vi': {
        'welcome': "Dev Tool - Trợ Lý Git AI",
        'enter_api_key': "Nhập Gemini API key của bạn",
        'add_first_account': "Thêm tài khoản Gemini đầu tiên",
        'choose_model': "Chọn model AI ưa thích",
        'model_1': "Gemini 2.5 Pro - Tiên tiến nhất (Khuyên dùng)",
        'model_2': "Gemini 2.5 Flash - Nhanh và mạnh mẽ",
        'model_3': "Gemini 2.5 Flash-Lite - Nhẹ và hiệu quả",
        'model_4': "Gemini 2.0 Flash - Model cũ",
        'choose_ui_lang': "Chọn ngôn ngữ giao diện",
        'lang_1': "Tiếng Anh",
        'lang_2': "Tiếng Việt",
        'choose_commit_lang': "Chọn ngôn ngữ commit message",
        'choose_commit_style': "Chọn phong cách commit message",
        'choose_auto_stage': "Bật tự động staging (git add .)? (y/N)",
        'choose_auto_push': "Bật tự động push sau khi commit? (y/N)",
        'invalid_choice': "❌ Lựa chọn không hợp lệ. Vui lòng thử lại.",
        'config_saved': "✅ Đã lưu cấu hình thành công!",
        'no_changes': "❌ Không có thay đổi nào được staged. Dùng 'git add' để stage thay đổi.",
        'analyzing_changes': "🔍 Đang phân tích các thay đổi của bạn...",
        'generated_msg': "📝 Commit message đã tạo",
        'proceed_commit': "🚀 Tiếp tục commit? (y/N)",
        'commit_cancelled': "❌ Đã hủy commit.",
        'commit_success': "✅ Đã commit thay đổi thành công!",
        'push_success': "🚀 Đã push thay đổi thành công!",
        'git_error': "❌ Thao tác git thất bại",
        'review_error': "❌ Review code thất bại",
        'settings_menu': "⚙️  Menu Cài Đặt",
        'current_config': "📋 Cấu Hình Hiện Tại",
        'ui_lang': "Ngôn Ngữ Giao Diện",
        'commit_lang': "Ngôn Ngữ Commit",
        'commit_style': "Phong Cách Commit",
        'auto_push': "Tự Động Push",
        'auto_stage': "Tự Động Stage",
        'enabled': "Bật",
        'disabled': "Tắt",
        'select_option': "Chọn một tùy chọn",
        'invalid_option': "❌ Tùy chọn không hợp lệ. Vui lòng thử lại.",
        'save_exit': "💾 Đã lưu cấu hình thành công!",
        'reset_confirm': "⚠️  Điều này sẽ đặt lại tất cả cài đặt về mặc định. Tiếp tục?",
        'reset_success': "🔄 Đã đặt lại cài đặt thành công!",
        'uninstall_confirm': "⚠️  Điều này sẽ gỡ bỏ hoàn toàn dev_tool. Tiếp tục?",
        'uninstall_success': "✅ Đã gỡ cài đặt dev_tool thành công!",
        'back_to_menu': "⬅️  Quay lại menu",
        'exit': "🚪 Thoát",
        'account_manager': "👥 Quản Lý Tài Khoản",
        'add_account': "➕ Thêm Tài Khoản",
        'edit_account': "✏️ Sửa Tài Khoản",
        'delete_account': "🗑️ Xóa Tài Khoản",
        'set_primary': "⭐ Đặt làm Chính",
        'no_accounts': "❌ Chưa có tài khoản nào",
        'account_email': "📧 Email",
        'account_model': "🤖 Model",
        'account_status': "🔑 Trạng Thái",
        'primary': "⭐ Chính",
        'secondary': "🔑 Phụ",
        'help_text': """
🛠️  Dev Tool - Trợ Lý Git AI
============================

📚 Lệnh Có Sẵn:
  dev_tool              Tạo commit message AI và commit
  dev_tool --no-push    Commit mà không push lên remote
  dev_tool settings     Mở menu cài đặt
  dev_tool --version    Hiển thị thông tin phiên bản

⚙️  Tùy Chọn Menu Cài Đặt:
  Chỉnh Sửa Cấu Hình    Thay đổi ngôn ngữ, model, và preferences
  Quản Lý Tài Khoản     Quản lý nhiều tài khoản Gemini
  Đặt Lại Mặc Định      Đặt lại tất cả cài đặt về trạng thái ban đầu
  Gỡ Cài Đặt Tool       Gỡ bỏ hoàn toàn dev_tool

🎨 Phong Cách Commit:
  Conventional          feat: thêm xác thực người dùng
  Emoji                 ✨ thêm xác thực người dùng
  Descriptive           Thêm hệ thống xác thực người dùng toàn diện

🌍 Ngôn Ngữ Hỗ Trợ:
  Giao diện: Tiếng Anh, Tiếng Việt
  Commit: Tiếng Anh, Tiếng Việt

🤖 Model Hỗ Trợ:
  Gemini 2.5 Pro        Model tiên tiến nhất (khuyên dùng)
  Gemini 2.5 Flash      Nhanh và mạnh mẽ
  Gemini 2.5 Flash-Lite Nhẹ và hiệu quả
  Gemini 2.0 Flash      Model cũ

📖 Để biết thêm: https://github.com/your-repo/dev_tool
        """,
        'edit_config': "Chỉnh Sửa Cấu Hình",
        'reset_defaults': "Đặt Lại Mặc Định",
        'uninstall_tool': "Gỡ Cài Đặt Tool",
        'help_info': "Trợ Giúp & Thông Tin",
        'options': "Tùy Chọn",
        'change_ui_lang': "Thay Đổi Ngôn Ngữ Giao Diện",
        'change_commit_lang': "Thay Đổi Ngôn Ngữ Commit",
        'update_api_key': "Cập Nhật API Key",
        'change_ai_model': "Thay Đổi Model AI",
        'change_commit_style': "Thay Đổi Phong Cách Commit",
        'toggle_auto_push': "Bật/Tắt Tự Động Push",
        'save_back': "Lưu & Quay Lại Menu",
        'back_no_save': "Quay Lại Không Lưu",
        'edit_options': "Tùy Chọn Chỉnh Sửa",
        'available_langs': "Ngôn Ngữ Có Sẵn",
        'select_lang': "Chọn ngôn ngữ",
        'enter_api_key_prompt': "Nhập API key mới",
        'available_models': "Model Có Sẵn",
        'select_model': "Chọn model",
        'available_styles': "Phong Cách Có Sẵn",
        'select_style': "Chọn phong cách",
        'confirm_toggle': "Bạn có muốn",
        'enable': "bật",
        'disable': "tắt",
        'press_enter_continue': "Nhấn Enter để tiếp tục"
    }
}

def print_header(text: str, color: str = 'CYAN') -> None:
    """Print a beautiful formatted header."""
    width = max(len(text) + 4, 50)
    border = "=" * width
    
    print(f"\n{COLORS[color]}{COLORS['BOLD']}")
    print(border)
    print(text.center(width))
    print(border)
    print(f"{COLORS['END']}")

def print_section(text: str, color: str = 'BLUE') -> None:
    """Print a formatted section header."""
    print(f"\n{COLORS[color]}{COLORS['BOLD']}▶ {text}{COLORS['END']}")

def print_error(text: str) -> None:
    """Print a styled error message."""
    print(f"{COLORS['RED']}{COLORS['BOLD']}❌ {text}{COLORS['END']}")

def print_success(text: str) -> None:
    """Print a styled success message."""
    print(f"{COLORS['GREEN']}{COLORS['BOLD']}✅ {text}{COLORS['END']}")

def print_warning(text: str) -> None:
    """Print a styled warning message."""
    print(f"{COLORS['YELLOW']}{COLORS['BOLD']}⚠️  {text}{COLORS['END']}")

def print_info(text: str) -> None:
    """Print a styled info message."""
    print(f"{COLORS['CYAN']}ℹ️  {text}{COLORS['END']}")

def get_message(key: str, config: Dict) -> str:
    """Get a translated message based on UI language."""
    lang = config.get('ui_language', 'en')
    return MESSAGES.get(lang, MESSAGES['en']).get(key, key)

def show_welcome_banner() -> None:
    """Display a beautiful welcome banner."""
    banner = f"""
{COLORS['CYAN']}{COLORS['BOLD']}
==================================================
              🛠️  DEV TOOL 2.0                
          AI-Powered Git Assistant            
                                                  
   🤖 Smart commit messages                       
   🌍 Multi-language support                      
   🎨 Multiple commit styles                      
   👥 Multi-account management                   
   ⚙️  Cross-platform compatibility              
==================================================
{COLORS['END']}
Welcome! Let's set up your AI git assistant.
    """
    print(banner)

def show_menu_divider() -> None:
    """Show a decorative menu divider."""
    print(f"{COLORS['DIM']}{'-' * 50}{COLORS['END']}")

def create_progress_bar(current: int, total: int, width: int = 30) -> str:
    """Create a simple progress bar."""
    progress = int((current / total) * width)
    bar = "█" * progress + "░" * (width - progress)
    percentage = int((current / total) * 100)
    return f"{COLORS['CYAN']}[{bar}] {percentage}%{COLORS['END']}"