# dev_tool/git_utils.py
#!/usr/bin/env python3
import subprocess
import sys
from typing import Dict

from .messages import get_message, print_error, print_section

# Extended commit type emojis
COMMIT_TYPES = {
    'feat': '✨',      # New feature
    'fix': '🐛',       # Bug fix
    'docs': '📚',      # Documentation
    'style': '💎',     # Code style/formatting
    'refactor': '♻️',  # Code refactoring
    'perf': '⚡️',      # Performance improvements
    'test': '🧪',      # Tests
    'chore': '🔧',     # Maintenance
    'ci': '👷',        # CI/CD
    'build': '📦',     # Build system
    'revert': '⏪',    # Revert changes
    'security': '🔒',  # Security related
    'config': '⚙️',    # Configuration changes
    'database': '🗄️',  # Database changes
    'ui': '🎨',        # User interface changes
    'i18n': '🌐',      # Internationalization
    'access': '♿',     # Accessibility
    'analytics': '📊', # Analytics tracking
    'deprecate': '🗑️', # Deprecation notices
}

def get_git_diff() -> str:
    """Get the git diff of staged changes."""
    try:
        return subprocess.check_output(['git', 'diff', '--cached']).decode('utf-8')
    except subprocess.CalledProcessError:
        print_error("Error: Failed to get git diff. Are you in a git repository?")
        sys.exit(1)

def stage_all_changes() -> bool:
    """Stage all changes (git add .)."""
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Error staging changes: {e}")
        return False

def format_commit_message(message: str, style: str = 'conventional') -> str:
    """Format the commit message with emoji based on style."""
    lines = message.strip().split('\n')
    if not lines:
        return message
    
    # Handle different commit styles
    if style == 'emoji':
        # For emoji style, add emoji to the beginning
        title = lines[0]
        if ': ' in title:
            type_part = title.split(':', 1)[0].lower()
            if type_part in COMMIT_TYPES:
                emoji = COMMIT_TYPES[type_part]
                lines[0] = f"{emoji} {title.split(':', 1)[1].strip()}"
        else:
            # Try to detect type from first word
            first_word = title.split()[0].lower()
            if first_word in COMMIT_TYPES.values():
                # Already has emoji
                pass
            else:
                # Add generic emoji if no type detected
                lines[0] = f"📝 {title}"
    
    # Clean up any backticks from bullet points
    lines = [line.replace('`', '') for line in lines]
    
    return '\n'.join(lines)

def commit_changes(commit_message: str, config: Dict) -> bool:
    """Commit changes and optionally push."""
    try:
        # Format the message based on style
        formatted_message = format_commit_message(commit_message, config.get('commit_style', 'conventional'))
        
        subprocess.run(['git', 'commit', '-m', formatted_message], check=True)
        print_section(get_message('commit_success', config), 'GREEN')
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"{get_message('git_error', config)} {e}")
        return False

def push_changes(config: Dict) -> bool:
    """Push changes to remote repository."""
    try:
        subprocess.run(['git', 'push'], check=True)
        print_section(get_message('push_success', config), 'GREEN')
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"{get_message('git_error', config)} {e}")
        return False