#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import argparse
from typing import Dict

CONFIG_DIR = os.path.expanduser("~/.config/dtl")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

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

COMMIT_TYPES = {
    'feat': '✨',     # New feature
    'fix': '🐛',      # Bug fix
    'docs': '📚',     # Documentation
    'style': '💎',    # Code style/formatting
    'refactor': '♻️',  # Code refactoring
    'perf': '⚡️',     # Performance improvements
    'test': '🧪',     # Tests
    'chore': '🔧',    # Maintenance
    'ci': '👷',       # CI/CD
    'build': '📦',    # Build system
    'revert': '⏪',   # Revert changes
}

# Default configuration
DEFAULT_CONFIG = {
    "api_key": "",
    "model": "gemini-2.0-flash",
    "ui_language": "en",
    "commit_language": "en",
    "auto_push": False,
    "auto_review": True
}

# Translations for UI messages
MESSAGES = {
    'en': {
        'welcome': "DTL (Developer Tool) Configuration",
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
🛠️  DTL (Developer Tool) Help
============================

Available Commands:
-----------------
dtl help                     Show this help message
dtl config                   Configure tool settings
dtl auto-commit             Generate commit message and handle git operations
dtl flutter                 Flutter development tools and utilities

Auto-commit Options:
------------------
--no-push                   Skip automatic push after commit
--no-review                 Skip code review before commit

Configuration Options:
-------------------
- Interface language (English/Vietnamese)
- Commit message language
- AI model selection
- Auto-push settings
- Auto-review settings
- Gemini API key

Examples:
--------
dtl auto-commit             Normal commit with review and push
dtl auto-commit --no-push   Commit without pushing
dtl config                  Open configuration menu
dtl help                    Show this help message

For more information, visit: https://github.com/KhanhRomVN/dev_tool
"""
    },
    'vi': {
        'welcome': "Cấu Hình DTL (Developer Tool)",
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
🛠️  DTL (Developer Tool) - Trợ Giúp
==================================

Các Lệnh Có Sẵn:
---------------
dtl help                     Hiển thị trợ giúp này
dtl config                   Cấu hình thiết lập
dtl auto-commit             Tạo commit message và xử lý git
dtl flutter                 Công cụ và tiện ích phát triển Flutter

Tùy Chọn Auto-commit:
-------------------
--no-push                   Bỏ qua tự động push sau khi commit
--no-review                 Bỏ qua review code trước khi commit

Tùy Chọn Cấu Hình:
----------------
- Ngôn ngữ giao diện (Tiếng Anh/Tiếng Việt)
- Ngôn ngữ commit message
- Lựa chọn model AI
- Cài đặt tự động push
- Cài đặt tự động review
- Gemini API key

Ví Dụ Sử Dụng:
------------
dtl auto-commit             Commit bình thường với review và push
dtl auto-commit --no-push   Commit không push
dtl config                  Mở menu cấu hình
dtl help                    Hiển thị trợ giúp này

Để biết thêm thông tin, truy cập: https://github.com/KhanhRomVN/dev_tool
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

def configure_tool(config: Dict) -> Dict:
    """Interactive configuration menu."""
    while True:
        print_header(get_message('welcome', config))
        show_current_config(config)
        print(get_message('config_menu', config))
        
        choice = input(get_message('select_option', config))
        
        if choice == '1':
            print_section(get_message('choose_ui_lang', config))
            print(f"1) {get_message('lang_1', config)}")
            print(f"2) {get_message('lang_2', config)}")
            lang_choice = input("\nEnter choice (1/2): ")
            if lang_choice in ['1', '2']:
                config['ui_language'] = 'en' if lang_choice == '1' else 'vi'
        
        elif choice == '2':
            print_section(get_message('choose_commit_lang', config))
            print(f"1) {get_message('lang_1', config)}")
            print(f"2) {get_message('lang_2', config)}")
            lang_choice = input("\nEnter choice (1/2): ")
            if lang_choice in ['1', '2']:
                config['commit_language'] = 'en' if lang_choice == '1' else 'vi'
        
        elif choice == '3':
            api_key = input(f"\n{get_message('enter_api_key', config)}: ")
            if api_key.strip():
                config['api_key'] = api_key
        
        elif choice == '4':
            print_section(get_message('choose_model', config))
            print(f"1) {get_message('model_1', config)}")
            print(f"2) {get_message('model_2', config)}")
            model_choice = input("\nEnter choice (1/2): ")
            if model_choice in ['1', '2']:
                config['model'] = "gemini-2.0-flash" if model_choice == '1' else "gemini-2.0-flash-lite"
        
        elif choice == '5':
            auto_push = input(f"\n{get_message('choose_auto_push', config)} ").lower()
            config['auto_push'] = auto_push in ['y', 'yes']
        
        elif choice == '6':
            auto_review = input(f"\n{get_message('choose_auto_review', config)} ").lower()
            config['auto_review'] = auto_review not in ['n', 'no']
        
        elif choice == '7':
            with open(CONFIG_PATH, 'w') as f:
                json.dump(config, f, indent=4)
            print_section(get_message('save_exit', config), 'GREEN')
            break
        
        else:
            print_error(get_message('invalid_option', config))
    
    return config

def create_config():
    """Create initial configuration."""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    
    config = DEFAULT_CONFIG.copy()
    
    print_header(MESSAGES['en']['welcome'])
    
    # First, choose UI language
    print_section(MESSAGES['en']['choose_ui_lang'])
    print(f"1) {MESSAGES['en']['lang_1']}")
    print(f"2) {MESSAGES['en']['lang_2']}")
    
    while True:
        ui_lang_choice = input("\nEnter choice (1/2): ")
        if ui_lang_choice in ['1', '2']:
            break
        print_error(MESSAGES['en']['invalid_choice'])
    
    config['ui_language'] = "en" if ui_lang_choice == "1" else "vi"
    
    # Now use the selected language for remaining prompts
    api_key = input(f"\n{get_message('enter_api_key', config)}: ")
    config['api_key'] = api_key
    
    print_section(get_message('choose_model', config))
    print(f"1) {get_message('model_1', config)}")
    print(f"2) {get_message('model_2', config)}")
    
    while True:
        model_choice = input("\nEnter choice (1/2): ")
        if model_choice in ['1', '2']:
            break
        print_error(get_message('invalid_choice', config))
    
    config['model'] = "gemini-2.0-flash" if model_choice == "1" else "gemini-2.0-flash-lite"
    
    print_section(get_message('choose_commit_lang', config))
    print(f"1) {get_message('lang_1', config)}")
    print(f"2) {get_message('lang_2', config)}")
    
    while True:
        commit_lang_choice = input("\nEnter choice (1/2): ")
        if commit_lang_choice in ['1', '2']:
            break
        print_error(get_message('invalid_choice', config))
    
    config['commit_language'] = "en" if commit_lang_choice == "1" else "vi"
    
    # Configure auto-push and auto-review
    auto_push = input(f"\n{get_message('choose_auto_push', config)} ").lower()
    config['auto_push'] = auto_push in ['y', 'yes']
    
    auto_review = input(f"\n{get_message('choose_auto_review', config)} ").lower()
    config['auto_review'] = auto_review not in ['n', 'no']
    
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)
    
    print_section(get_message('config_saved', config), 'GREEN')
    return config

def load_config():
    """Load configuration from the config file."""
    try:
        if not os.path.exists(CONFIG_PATH):
            return create_config()
        
        with open(CONFIG_PATH) as f:
            config = json.load(f)
            
        # Validate config and set defaults for new fields
        for key, value in DEFAULT_CONFIG.items():
            if key not in config:
                config[key] = value
            
        return config
    except Exception as e:
        print_error(f"Error loading config: {e}")
        return create_config()

def get_git_diff():
    """Get the git diff of staged changes."""
    try:
        return subprocess.check_output(['git', 'diff', '--cached']).decode('utf-8')
    except subprocess.CalledProcessError:
        print_error("Error: Failed to get git diff. Are you in a git repository?")
        sys.exit(1)

def format_commit_message(message):
    """Format the commit message with emoji."""
    lines = message.strip().split('\n')
    if not lines:
        return message
    
    # Handle the title line
    title = lines[0]
    if ':' in title:
        type_part = title.split(':', 1)[0].lower()
        if type_part in COMMIT_TYPES:
            emoji = COMMIT_TYPES[type_part]
            title = f"{type_part}: {emoji} {title.split(':', 1)[1].strip()}"
            lines[0] = title
    
    # Clean up any backticks from bullet points
    lines = [line.replace('`', '') for line in lines]
    
    return '\n'.join(lines)

def review_code(diff_text, config):
    """Perform code review using Gemini AI."""
    import google.generativeai as genai
    genai.configure(api_key=config['api_key'])
    model = genai.GenerativeModel(config['model'])
    
    review_prompt = f"""
    Perform a thorough code review of the following changes.
    Focus on:
    1. Potential bugs or issues
    2. Code improvement suggestions
    3. Code smells or anti-patterns
    4. Security concerns
    
    Format your response in clear sections.
    Be specific but concise.
    If no issues are found in a category, say "No issues found."
    Do not use markdown formatting.
    Keep bullet points simple with just "-" prefix.
    
    Changes to review:
    {diff_text}
    """
    
    try:
        response = model.generate_content(review_prompt)
        review = response.text.strip()
        
        # Format the review with emojis and sections
        sections = {
            "🐛 Potential Bugs": [],
            "💡 Improvements": [],
            "🔍 Code Smells": [],
            "🔒 Security": []
        }
        
        current_section = None
        for line in review.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Try to match section headers
            lower_line = line.lower()
            if "bug" in lower_line or "issue" in lower_line:
                current_section = "🐛 Potential Bugs"
            elif "improve" in lower_line or "suggest" in lower_line:
                current_section = "💡 Improvements"
            elif "smell" in lower_line or "pattern" in lower_line:
                current_section = "🔍 Code Smells"
            elif "security" in lower_line or "vulnerab" in lower_line:
                current_section = "🔒 Security"
            elif current_section and line.startswith(("-", "*", "•")):
                # Clean up the line
                clean_line = line.lstrip("-*• ").strip()
                clean_line = clean_line.replace("**", "").replace("*", "").replace("`", "")
                sections[current_section].append(clean_line)
        
        # Format the final review
        formatted_review = f"\n{COLORS['BLUE']}{COLORS['BOLD']}📋 Code Review Results{COLORS['END']}\n"
        formatted_review += "=" * 50 + "\n\n"
        
        for section, items in sections.items():
            formatted_review += f"{COLORS['YELLOW']}{section}:{COLORS['END']}\n"
            if items:
                for item in items:
                    formatted_review += f"- {item}\n"
            else:
                formatted_review += f"{COLORS['GREEN']}✅ No issues found{COLORS['END']}\n"
            formatted_review += "\n"
        
        return formatted_review
    except Exception as e:
        print_error(get_message('review_error', config))
        print(e)
        return None

def generate_commit_message(diff_text, config):
    """Generate commit message using Gemini AI."""
    import google.generativeai as genai
    genai.configure(api_key=config['api_key'])
    
    model_map = {
        'gemini-2.0-flash': 'gemini-2.0-flash',
        'gemini-2.0-flash-lite': 'gemini-2.0-flash-lite'
    }
    
    model_name = model_map.get(config['model'], 'gemini-2.0-flash')
    model = genai.GenerativeModel(model_name)
    
    prompt = f"""
    Analyze the following git diff and generate a structured commit message.
    Generate the message in {'Vietnamese' if config['commit_language'] == 'vi' else 'English'}.
    
    Rules:
    1. Start with a type (one of: feat, fix, docs, style, refactor, perf, test, chore, ci, build, revert)
    2. Follow with a concise title
    3. Add 2-3 bullet points describing specific changes
    4. Do not use any markdown formatting (no backticks, no code blocks)
    5. Keep descriptions plain and simple
    
    Format:
    type: Title of the change
    - Change detail 1 (plain text, no formatting)
    - Change detail 2 (plain text, no formatting)
    
    Git diff:
    {diff_text}
    """
    
    try:
        response = model.generate_content(prompt)
        message = response.text.strip()
        return format_commit_message(message)
    except Exception as e:
        print_error(get_message('git_error', config))
        print(e)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Developer Tool - Auto-commit and code management')
    parser.add_argument('command', nargs='?', default='auto-commit', help='Command to execute (auto-commit, config, help)')
    parser.add_argument('--no-push', action='store_true', help='Skip automatic push after commit')
    parser.add_argument('--reconfigure', action='store_true', help='Force reconfiguration')
    parser.add_argument('--no-review', action='store_true', help='Skip code review')
    args = parser.parse_args()

    config = load_config()

    # Handle different commands
    if args.command == 'help':
        print_header("DTL (Developer Tool)")
        print(get_message('help_text', config))
        return
    elif args.command == 'config' or args.reconfigure:
        config = configure_tool(config)
        return
    elif args.command == 'auto-commit':
        diff = get_git_diff()
        
        if not diff:
            print_error(get_message('no_changes', config))
            sys.exit(1)
        
        # Perform code review unless explicitly skipped or disabled in config
        if not args.no_review and config['auto_review']:
            print_section(get_message('performing_review', config))
            review_results = review_code(diff, config)
            if review_results:
                print(review_results)
                
                # Ask if user wants to proceed
                while True:
                    proceed = input(f"\n{get_message('proceed_commit', config)} ").lower()
                    if proceed in ['y', 'yes']:
                        break
                    elif proceed in ['n', 'no', '']:
                        print_error(get_message('commit_cancelled', config))
                        sys.exit(0)
        
        commit_message = generate_commit_message(diff, config)
        print_section(get_message('generated_msg', config))
        print(f"\n{commit_message}\n")
        
        try:
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            print_section(get_message('commit_success', config), 'GREEN')
            
            if not args.no_push and config['auto_push']:
                subprocess.run(['git', 'push'], check=True)
                print_section(get_message('push_success', config), 'GREEN')
        except subprocess.CalledProcessError as e:
            print_error(f"{get_message('git_error', config)} {e}")
            sys.exit(1)
    elif args.command == 'flutter':
        from . import flutter
        flutter.show_flutter_menu(config)
        return
    else:
        print_error(f"Unknown command: {args.command}")
        print(get_message('help_text', config))
        sys.exit(1)

if __name__ == "__main__":
    main()