#!/usr/bin/env python3
import os
import json
from typing import Dict

CONFIG_DIR = os.path.expanduser("~/.config/dev_tool")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

# Default configuration
DEFAULT_CONFIG = {
    "api_key": "",
    "model": "gemini-2.0-flash",
    "ui_language": "en",
    "commit_language": "en",
    "auto_push": False,
    "auto_review": True
}

def load_config() -> Dict:
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
        from .messages import print_error
        print_error(f"Error loading config: {e}")
        return create_config()

def save_config(config: Dict) -> None:
    """Save configuration to file."""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)

def create_config() -> Dict:
    """Create initial configuration through interactive setup."""
    from .messages import (
        MESSAGES, print_header, print_section, print_error,
        get_message, show_current_config
    )
    
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
    
    save_config(config)
    print_section(get_message('config_saved', config), 'GREEN')
    return config

def configure_tool(config: Dict) -> Dict:
    """Interactive configuration menu."""
    from .messages import (
        print_header, print_section, print_error,
        get_message, show_current_config
    )
    
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
            save_config(config)
            print_section(get_message('save_exit', config), 'GREEN')
            break
        
        else:
            print_error(get_message('invalid_option', config))
    
    return config