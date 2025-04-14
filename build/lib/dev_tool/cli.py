#!/usr/bin/env python3
import sys
import argparse
from typing import Dict

from .config import load_config, configure_tool
from .messages import get_message, print_header, print_section, print_error
from .git_utils import get_git_diff, commit_changes, push_changes
from .ai_utils import review_code, generate_commit_message

def handle_auto_commit(args: argparse.Namespace, config: Dict) -> None:
    """Handle the auto-commit command."""
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
    
    if commit_changes(commit_message, config):
        if not args.no_push and config['auto_push']:
            push_changes(config)

def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description='Developer Tool - Auto-commit and code management')
    parser.add_argument('command', nargs='?', default='auto-commit',
                       help='Command to execute (auto-commit, config, help, flutter)')
    parser.add_argument('--no-push', action='store_true',
                       help='Skip automatic push after commit')
    parser.add_argument('--reconfigure', action='store_true',
                       help='Force reconfiguration')
    parser.add_argument('--no-review', action='store_true',
                       help='Skip code review')
    args = parser.parse_args()

    config = load_config()

    # Handle different commands
    if args.command == 'help':
        print_header("Developer Tool")
        print(get_message('help_text', config))
        return
    elif args.command == 'config' or args.reconfigure:
        configure_tool(config)
        return
    elif args.command == 'auto-commit':
        handle_auto_commit(args, config)
        return
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