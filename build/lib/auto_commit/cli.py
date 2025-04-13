#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import argparse
from typing import Dict

CONFIG_DIR = os.path.expanduser("~/.config/auto-commit")
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

# Translations for UI messages
MESSAGES = {
    'en': {
        'welcome': "Auto-Commit Tool Configuration",
        'enter_api_key': "Please enter your Gemini API key:",
        'choose_model': "Choose your preferred model:",
        'model_1': "Gemini 2.0 Flash (recommended) - Advanced features, speed",
        'model_2': "Gemini 2.0 Flash-Lite - Cost-effective, low latency",
        'choose_ui_lang': "Choose interface language:",
        'lang_1': "English",
        'lang_2': "Tiếng Việt",
        'choose_commit_lang': "Choose commit message language:",
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
    },
    'vi': {
        'welcome': "Cấu Hình Công Cụ Auto-Commit",
        'enter_api_key': "Vui lòng nhập Gemini API key của bạn:",
        'choose_model': "Chọn model bạn muốn sử dụng:",
        'model_1': "Gemini 2.0 Flash (khuyến nghị) - Tính năng nâng cao, tốc độ nhanh",
        'model_2': "Gemini 2.0 Flash-Lite - Tiết kiệm, độ trễ thấp",
        'choose_ui_lang': "Chọn ngôn ngữ giao diện:",
        'lang_1': "Tiếng Anh",
        'lang_2': "Tiếng Việt",
        'choose_commit_lang': "Chọn ngôn ngữ cho commit message:",
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

def create_config():
    """Create configuration by prompting user."""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    
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
    
    ui_language = "en" if ui_lang_choice == "1" else "vi"
    
    # Now use the selected language for remaining prompts
    api_key = input(f"\n{get_message('enter_api_key', {'ui_language': ui_language})}: ")
    
    print_section(get_message('choose_model', {'ui_language': ui_language}))
    print(f"1) {get_message('model_1', {'ui_language': ui_language})}")
    print(f"2) {get_message('model_2', {'ui_language': ui_language})}")
    
    while True:
        model_choice = input("\nEnter choice (1/2): ")
        if model_choice in ['1', '2']:
            break
        print_error(get_message('invalid_choice', {'ui_language': ui_language}))
    
    print_section(get_message('choose_commit_lang', {'ui_language': ui_language}))
    print(f"1) {get_message('lang_1', {'ui_language': ui_language})}")
    print(f"2) {get_message('lang_2', {'ui_language': ui_language})}")
    
    while True:
        commit_lang_choice = input("\nEnter choice (1/2): ")
        if commit_lang_choice in ['1', '2']:
            break
        print_error(get_message('invalid_choice', {'ui_language': ui_language}))
    
    model = "gemini-2.0-flash" if model_choice == "1" else "gemini-2.0-flash-lite"
    commit_language = "en" if commit_lang_choice == "1" else "vi"
    
    config = {
        "api_key": api_key,
        "model": model,
        "ui_language": ui_language,
        "commit_language": commit_language
    }
    
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)
    
    print_section(get_message('config_saved', {'ui_language': ui_language}), 'GREEN')
    return config

def load_config():
    """Load configuration from the config file."""
    try:
        if not os.path.exists(CONFIG_PATH):
            return create_config()
        
        with open(CONFIG_PATH) as f:
            config = json.load(f)
            
        # Validate config
        required_keys = ['api_key', 'model', 'ui_language', 'commit_language']
        if not all(key in config for key in required_keys):
            return create_config()
            
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
    parser = argparse.ArgumentParser(description='Auto-generate commit messages and push changes')
    parser.add_argument('--no-push', action='store_true', help='Generate commit message without pushing')
    parser.add_argument('--reconfigure', action='store_true', help='Force reconfiguration')
    parser.add_argument('--no-review', action='store_true', help='Skip code review')
    args = parser.parse_args()

    # Force reconfiguration if requested
    if args.reconfigure:
        config = create_config()
    else:
        config = load_config()

    diff = get_git_diff()
    
    if not diff:
        print_error(get_message('no_changes', config))
        sys.exit(1)
    
    # Perform code review unless explicitly skipped
    if not args.no_review:
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
        
        if not args.no_push:
            subprocess.run(['git', 'push'], check=True)
            print_section(get_message('push_success', config), 'GREEN')
    except subprocess.CalledProcessError as e:
        print_error(f"{get_message('git_error', config)} {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()