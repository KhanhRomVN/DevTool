"""
Developer Tool - A comprehensive development toolkit

Features:
- AI-powered commit message generation
- Automated code review
- Flutter development tools
- Multi-language support (English/Vietnamese)
"""

from .cli import main
from .config import load_config, configure_tool
from .messages import get_message, print_header, print_section, print_error
from .git_utils import get_git_diff, commit_changes, push_changes
from .ai_utils import review_code, generate_commit_message

__version__ = "1.0.0"
__author__ = "KhanhRomVN"