# dev_tool/cli.py
#!/usr/bin/env python3
import sys
import argparse
from typing import Dict

from .config import load_config, configure_tool, reset_config, uninstall_tool
from .messages import get_message, print_header, print_section, print_error, print_success, print_info
from .git_utils import get_git_diff, commit_changes, push_changes, stage_all_changes
from .ai_utils import generate_commit_message

def handle_auto_commit(args: argparse.Namespace, config: Dict) -> None:
    """Handle the auto-commit command."""
    # Auto stage changes if enabled
    if config.get('auto_stage', False):
        if not stage_all_changes():
            print_error(get_message('git_error', config))
            sys.exit(1)
    
    diff = get_git_diff()
    
    if not diff:
        print_error(get_message('no_changes', config))
        sys.exit(1)
    
    # Show diff summary
    print_section(get_message('analyzing_changes', config))
    lines_added = diff.count('\n+') - diff.count('\n+++')
    lines_removed = diff.count('\n-') - diff.count('\n---')
    print(f"📊 {lines_added} additions, {lines_removed} deletions")
    
    # Get primary account for generation
    primary_account = None
    for account in config.get('accounts', []):
        if account.get('is_primary', False):
            primary_account = account
            break
    
    if not primary_account:
        print_error("❌ No primary account configured. Please set up an account in settings.")
        sys.exit(1)
    
    # Generate commit message
    commit_message = generate_commit_message(
        diff, 
        primary_account['api_key'], 
        primary_account['model'],
        config.get('commit_style', 'conventional'),
        config.get('commit_language', 'en')
    )
    
    print_section(get_message('generated_msg', config))
    print(f"\n{commit_message}\n")
    
    # Ask for confirmation if enabled
    if config.get('confirm_before_commit', True):
        while True:
            proceed = input(f"{get_message('proceed_commit', config)} ").lower()
            if proceed in ['y', 'yes', 'có']:
                break
            elif proceed in ['n', 'no', 'không', '']:
                print_error(get_message('commit_cancelled', config))
                sys.exit(0)
    
    # Commit changes
    if commit_changes(commit_message, config):
        if not args.no_push and config.get('auto_push', False):
            push_changes(config)

def show_settings_menu(config: Dict) -> None:
    """Show the settings menu."""
    from .ui import show_settings_interface
    show_settings_interface(config)

def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='🛠️  Dev Tool - AI-powered Git Commit Message Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  dev_tool                    Generate and commit with AI message
  dev_tool --no-push          Commit without pushing
  dev_tool settings           Open settings menu
  
Visit: https://github.com/your-repo/dev_tool
        """
    )
    
    parser.add_argument('command', nargs='?', default='auto-commit',
                       help='Command to execute (default: auto-commit)')
    parser.add_argument('--no-push', action='store_true',
                       help='Skip automatic push after commit')
    parser.add_argument('--version', action='version', version='Dev Tool 2.0.0')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config()
    
    # Handle different commands
    if args.command == 'settings':
        show_settings_menu(config)
        return
    elif args.command == 'help':
        parser.print_help()
        return
    elif args.command == 'auto-commit':
        handle_auto_commit(args, config)
        return
    else:
        print_error(f"Unknown command: {args.command}")
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()