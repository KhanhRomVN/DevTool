#!/usr/bin/env python3
import subprocess
import sys
from typing import Dict

from .messages import get_message, print_error, print_section

# Commit type emojis
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

def get_git_diff() -> str:
    """Get the git diff of staged changes."""
    try:
        return subprocess.check_output(['git', 'diff', '--cached']).decode('utf-8')
    except subprocess.CalledProcessError:
        print_error("Error: Failed to get git diff. Are you in a git repository?")
        sys.exit(1)

def format_commit_message(message: str) -> str:
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

def commit_changes(commit_message: str, config: Dict) -> bool:
    """Commit changes and optionally push."""
    try:
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
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