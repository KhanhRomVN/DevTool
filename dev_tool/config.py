# dev_tool/config.py
#!/usr/bin/env python3
import os
import json
import shutil
import platform
from typing import Dict, List
from pathlib import Path

# Cross-platform configuration directory
def get_config_dir():
    system = platform.system().lower()
    if system == "windows":
        return Path(os.environ.get('APPDATA', '~')) / 'dev_tool'
    elif system == "darwin":  # macOS
        return Path.home() / 'Library' / 'Application Support' / 'dev_tool'
    else:  # Linux and others
        return Path.home() / '.config' / 'dev_tool'

CONFIG_DIR = get_config_dir()
CONFIG_PATH = CONFIG_DIR / "config.json"

# Available Gemini models
GEMINI_MODELS = [
    "gemini-2.5-pro",
    "gemini-2.5-flash", 
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash"
]

# Default configuration
DEFAULT_CONFIG = {
    "accounts": [],
    "ui_language": "en",
    "commit_language": "en", 
    "auto_push": False,
    "auto_stage": False,
    "commit_style": "conventional",
    "max_line_length": 72,
    "show_diff_stats": True,
    "confirm_before_commit": True
}

def load_config() -> Dict:
    """Load configuration from the config file."""
    try:
        if not CONFIG_PATH.exists():
            return create_initial_config()
        
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        # Validate config and set defaults for new fields
        for key, value in DEFAULT_CONFIG.items():
            if key not in config:
                config[key] = value
                
        # Migrate old config format (if exists)
        if "api_key" in config and "model" in config:
            # Convert old single account to new multi-account format
            if config["api_key"] and not config["accounts"]:
                config["accounts"] = [{
                    "email": "primary@example.com",
                    "api_key": config["api_key"],
                    "model": config["model"],
                    "is_primary": True
                }]
            
            # Remove old fields
            if "api_key" in config:
                del config["api_key"]
            if "model" in config:
                del config["model"]
                
        return config
    except Exception as e:
        from .messages import print_error
        print_error(f"Error loading config: {e}")
        return create_initial_config()

def save_config(config: Dict) -> None:
    """Save configuration to file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

def create_initial_config() -> Dict:
    """Create initial configuration through interactive setup."""
    from .messages import (
        print_header, print_section, print_error,
        get_message, show_welcome_banner
    )
    
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    config = DEFAULT_CONFIG.copy()
    
    show_welcome_banner()
    
    # Choose UI language first
    print_section("🌐 Choose Interface Language")
    print("1️⃣  English")
    print("2️⃣  Tiếng Việt")
    
    while True:
        ui_lang_choice = input("\n🔤 Enter choice (1/2): ").strip()
        if ui_lang_choice in ['1', '2']:
            break
        print_error("❌ Invalid choice. Please try again.")
    
    config['ui_language'] = "en" if ui_lang_choice == "1" else "vi"
    
    # Add first account
    print_section(get_message('add_first_account', config))
    
    account = {
        "email": "",
        "api_key": "", 
        "model": "gemini-2.0-flash",
        "is_primary": True
    }
    
    # Get email
    while not account["email"]:
        account["email"] = input("📧 Email: ").strip()
        if not account["email"]:
            print_error("❌ Email is required.")
    
    # Get API key
    while not account["api_key"]:
        account["api_key"] = input("🔑 API Key: ").strip()
        if not account["api_key"]:
            print_error("❌ API Key is required.")
    
    # Choose model
    print_section(get_message('choose_model', config))
    for i, model in enumerate(GEMINI_MODELS, 1):
        print(f"{i}️⃣  {model}")
    
    while True:
        try:
            model_choice = int(input("\n🤖 Enter choice (1-4): ").strip())
            if 1 <= model_choice <= len(GEMINI_MODELS):
                account["model"] = GEMINI_MODELS[model_choice-1]
                break
            print_error("❌ Invalid choice. Please try again.")
        except ValueError:
            print_error("❌ Please enter a number.")
    
    config["accounts"] = [account]
    
    # Choose commit language
    print_section(get_message('choose_commit_lang', config))
    print("1️⃣  " + get_message('lang_1', config))
    print("2️⃣  " + get_message('lang_2', config))
    
    while True:
        commit_lang_choice = input("\n💬 Enter choice (1/2): ").strip()
        if commit_lang_choice in ['1', '2']:
            break
        print_error(get_message('invalid_choice', config))
    
    config['commit_language'] = "en" if commit_lang_choice == "1" else "vi"
    
    # Choose commit style
    print_section(get_message('choose_commit_style', config))
    print("1️⃣  Conventional Commits (feat: add new feature)")
    print("2️⃣  Emoji Style (✨ add new feature)")
    print("3️⃣  Descriptive (Add user authentication system)")
    
    while True:
        style_choice = input("\n🎨 Enter choice (1-3): ").strip()
        if style_choice in ['1', '2', '3']:
            break
        print_error(get_message('invalid_choice', config))
    
    styles = {'1': 'conventional', '2': 'emoji', '3': 'descriptive'}
    config['commit_style'] = styles[style_choice]
    
    # Configure auto-stage
    auto_stage = input(f"\n📦 {get_message('choose_auto_stage', config)} ").lower()
    config['auto_stage'] = auto_stage in ['y', 'yes', 'có']
    
    # Configure auto-push
    auto_push = input(f"\n🚀 {get_message('choose_auto_push', config)} ").lower()
    config['auto_push'] = auto_push in ['y', 'yes', 'có']
    
    save_config(config)
    print_section(get_message('config_saved', config), 'GREEN')
    return config

def reset_config() -> Dict:
    """Reset configuration to defaults."""
    from .messages import print_success
    
    if CONFIG_PATH.exists():
        CONFIG_PATH.unlink()
    
    config = create_initial_config()
    print_success("🔄 Configuration reset successfully!")
    return config

def uninstall_tool() -> None:
    """Uninstall the tool completely."""
    from .messages import print_warning, print_success, print_error
    
    print_warning("⚠️  This will completely remove dev_tool and all its data!")
    confirm = input("Are you sure you want to uninstall? (yes/no): ").lower()
    
    if confirm not in ['yes', 'y']:
        print_error("Uninstall cancelled.")
        return
    
    try:
        # Remove config directory
        if CONFIG_DIR.exists():
            shutil.rmtree(CONFIG_DIR)
        
        print_success("✅ dev_tool has been uninstalled successfully!")
        print("To reinstall, run: pip install dev_tool")
        
    except Exception as e:
        print_error(f"Error during uninstall: {e}")

def configure_tool(config: Dict) -> Dict:
    """Interactive configuration menu."""
    from .ui import show_configuration_interface
    return show_configuration_interface(config)