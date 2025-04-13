#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import argparse
import google.generativeai as genai

CONFIG_DIR = os.path.expanduser("~/.config/auto-commit")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

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

def create_config():
    """Create configuration by prompting user."""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    
    api_key = input("Please enter your Gemini API key: ")
    
    print("\nChoose your preferred model:")
    print("1) Gemini 2.0 Flash (recommended) - Advanced features, speed")
    print("2) Gemini 2.0 Flash-Lite - Cost-effective, low latency")
    
    while True:
        choice = input("Enter choice (1/2): ")
        if choice in ['1', '2']:
            break
        print("Invalid choice. Please enter 1 or 2.")
    
    print("\nChoose commit message language:")
    print("1) English")
    print("2) Tiếng Việt")
    
    while True:
        lang_choice = input("Enter choice (1/2): ")
        if lang_choice in ['1', '2']:
            break
        print("Invalid choice. Please enter 1 or 2.")
    
    model = "gemini-2.0-flash" if choice == "1" else "gemini-2.0-flash-lite"
    language = "en" if lang_choice == "1" else "vi"
    
    config = {
        "api_key": api_key,
        "model": model,
        "language": language
    }
    
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)
    
    print("\nConfiguration saved successfully!")
    return config

def load_config():
    """Load configuration from the config file."""
    try:
        if not os.path.exists(CONFIG_PATH):
            return create_config()
        
        with open(CONFIG_PATH) as f:
            config = json.load(f)
            
        # Validate config
        if not config.get("api_key") or not config.get("model") or not config.get("language"):
            return create_config()
            
        return config
    except Exception as e:
        print(f"Error loading config: {e}")
        return create_config()

def get_git_diff():
    """Get the git diff of staged changes."""
    try:
        return subprocess.check_output(['git', 'diff', '--cached']).decode('utf-8')
    except subprocess.CalledProcessError:
        print("Error: Failed to get git diff. Are you in a git repository?")
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

def get_prompt_by_language(language, diff_text):
    """Get the appropriate prompt based on language."""
    if language == "vi":
        return f"""
        Phân tích git diff sau và tạo commit message có cấu trúc.
        
        Quy tắc:
        1. Bắt đầu với một loại (chọn một trong: feat, fix, docs, style, refactor, perf, test, chore, ci, build, revert)
        2. Tiếp theo là tiêu đề ngắn gọn mô tả thay đổi chính
        3. Thêm 2-3 điểm mô tả chi tiết các thay đổi cụ thể
        4. Không sử dụng định dạng markdown (không backticks, không code blocks)
        5. Giữ mô tả đơn giản và rõ ràng
        
        Định dạng:
        loại: Tiêu đề thay đổi
        - Chi tiết thay đổi 1 (văn bản thuần, không định dạng)
        - Chi tiết thay đổi 2 (văn bản thuần, không định dạng)
        
        Git diff:
        {diff_text}
        """
    else:
        return f"""
        Analyze the following git diff and generate a structured commit message.
        
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

def review_code(diff_text, config):
    """Perform code review using Gemini AI."""
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
        formatted_review = "\n📋 Code Review Results\n"
        formatted_review += "=" * 50 + "\n\n"
        
        for section, items in sections.items():
            formatted_review += f"{section}:\n"
            if items:
                for item in items:
                    formatted_review += f"- {item}\n"
            else:
                formatted_review += "✅ No issues found\n"
            formatted_review += "\n"
        
        return formatted_review
    except Exception as e:
        print(f"Error performing code review: {e}")
        return None

def generate_commit_message(diff_text, config):
    """Generate commit message using Gemini AI."""
    genai.configure(api_key=config['api_key'])
    
    model_map = {
        'gemini-2.0-flash': 'gemini-2.0-flash',
        'gemini-2.0-flash-lite': 'gemini-2.0-flash-lite'
    }
    
    model_name = model_map.get(config['model'], 'gemini-2.0-flash')
    model = genai.GenerativeModel(model_name)
    
    prompt = get_prompt_by_language(config['language'], diff_text)
    
    try:
        response = model.generate_content(prompt)
        message = response.text.strip()
        return format_commit_message(message)
    except Exception as e:
        print(f"Error generating commit message: {e}")
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
        print("No staged changes found. Use 'git add' to stage your changes.")
        sys.exit(1)
    
    # Perform code review unless explicitly skipped
    if not args.no_review:
        print("\nPerforming code review...")
        review_results = review_code(diff, config)
        if review_results:
            print(review_results)
            
            # Ask if user wants to proceed
            while True:
                proceed = input("\nDo you want to proceed with the commit? (y/N): ").lower()
                if proceed in ['y', 'yes']:
                    break
                elif proceed in ['n', 'no', '']:
                    print("Commit cancelled. Please review and fix the issues.")
                    sys.exit(0)
    
    commit_message = generate_commit_message(diff, config)
    print(f"\nGenerated commit message:\n{commit_message}\n")
    
    try:
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print("Changes committed successfully!")
        
        if not args.no_push:
            subprocess.run(['git', 'push'], check=True)
            print("Changes pushed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during git operations: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()