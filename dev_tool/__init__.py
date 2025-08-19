"""
Developer Tool - A comprehensive development toolkit

Features:
- AI-powered commit message generation
- Multi-language support (English/Vietnamese)
- Multiple commit styles
- Cross-platform compatibility
"""

from .cli import main
from .config import load_config, configure_tool
from .messages import get_message, print_header, print_section, print_error
from .git_utils import get_git_diff, commit_changes, push_changes
from .ai_utils import generate_commit_message

__version__ = "2.0.0"
__author__ = "KhanhRomVN"