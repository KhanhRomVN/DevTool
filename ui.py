#!/usr/bin/env python3
from typing import Dict
from .messages import (
    print_header, print_section, print_error, print_success, print_warning,
    get_message, show_menu_divider, COLORS
)
from .config import save_config, reset_config, uninstall_tool

def show_current_config(config: Dict) -> None:
    """Display current configuration in a beautiful format."""
    print_section(get_message('current_config', config), 'PURPLE')
    
    # Language settings
    ui_lang_display = "🇺🇸 English" if config['ui_language'] == 'en' else "🇻🇳 Tiếng Việt"
    commit_lang_display = "🇺🇸 English" if config['commit_language'] == 'en' else "🇻🇳 Tiếng Việt"
    
    # Commit style display
    style_display = {
        'conventional': '📋 Conventional Commits',
        'emoji': '😄 Emoji Style', 
        'descriptive': '📝 Descriptive'
    }.get(config.get('commit_style', 'conventional'), '📋 Conventional')
    
    # Model display
    model_display = {
        'gemini-2.0-flash': '🚀 Gemini 2.0 Flash',
        'gemini-2.0-flash-lite': '⚡ Gemini 2.0 Flash-Lite'
    }.get(config.get('model', 'gemini-2.0-flash'), '🚀 Gemini 2.0 Flash')
    
    print(f"""
{COLORS['CYAN']}┌─────────────────────────────────────────────────┐
│                 Configuration                   │
├─────────────────────────────────────────────────┤{COLORS['END']}
│ {COLORS['YELLOW']}🌐 Interface Language:{COLORS['END']} {ui_lang_display:<20} │
│ {COLORS['YELLOW']}💬 Commit Language:{COLORS['END']}   {commit_lang_display:<20} │  
│ {COLORS['YELLOW']}🎨 Commit Style:{COLORS['END']}      {style_display:<20} │
│ {COLORS['YELLOW']}🤖 AI Model:{COLORS['END']}          {model_display:<20} │
│ {COLORS['YELLOW']}🚀 Auto Push:{COLORS['END']}         {get_status_display(config.get('auto_push', False)):<20} │
{COLORS['CYAN']}└─────────────────────────────────────────────────┘{COLORS['END']}
    """)

def get_status_display(enabled: bool) -> str:
    """Get colored status display."""
    if enabled:
        return f"{COLORS['GREEN']}✅ Enabled{COLORS['END']}"
    else:
        return f"{COLORS['RED']}❌ Disabled{COLORS['END']}"

def show_settings_interface(config: Dict) -> None:
    """Show the main settings interface."""
    while True:
        print_header(get_message('settings_menu', config))
        show_current_config(config)
        
        print(f"""
{COLORS['BLUE']}┌─────────────────────────────────────────────────┐
│                    Options                      │
├─────────────────────────────────────────────────┤{COLORS['END']}
│ {COLORS['GREEN']}1{COLORS['END']} │ ⚙️  Edit Configuration                        │
│ {COLORS['YELLOW']}2{COLORS['END']} │ 🔄 Reset to Defaults                         │
│ {COLORS['RED']}3{COLORS['END']} │ 🗑️  Uninstall Tool                           │
│ {COLORS['CYAN']}4{COLORS['END']} │ ❓ Help & Information                        │
│ {COLORS['WHITE']}0{COLORS['END']} │ 🚪 Exit                                      │
{COLORS['BLUE']}└─────────────────────────────────────────────────┘{COLORS['END']}
        """)
        
        choice = input(f"\n{COLORS['BOLD']}🎯 {get_message('select_option', config)} (0-4): {COLORS['END']}").strip()
        
        if choice == '1':
            config = show_configuration_interface(config)
        elif choice == '2':
            if confirm_action(get_message('reset_confirm', config)):
                config = reset_config()
        elif choice == '3':
            if confirm_action(get_message('uninstall_confirm', config)):
                uninstall_tool()
                return
        elif choice == '4':
            show_help(config)
        elif choice == '0':
            print_success("👋 Goodbye!")
            break
        else:
            print_error(get_message('invalid_option', config))

def show_configuration_interface(config: Dict) -> Dict:
    """Show detailed configuration interface."""
    while True:
        print_header("⚙️  Edit Configuration")
        show_current_config(config)
        
        print(f"""
{COLORS['BLUE']}┌─────────────────────────────────────────────────┐
│                Edit Options                     │  
├─────────────────────────────────────────────────┤{COLORS['END']}
│ {COLORS['GREEN']}1{COLORS['END']} │ 🌐 Change Interface Language                 │
│ {COLORS['GREEN']}2{COLORS['END']} │ 💬 Change Commit Language                    │
│ {COLORS['GREEN']}3{COLORS['END']} │ 🔑 Update API Key                            │
│ {COLORS['GREEN']}4{COLORS['END']} │ 🤖 Change AI Model                          │
│ {COLORS['GREEN']}5{COLORS['END']} │ 🎨 Change Commit Style                      │
│ {COLORS['GREEN']}6{COLORS['END']} │ 🚀 Toggle Auto Push                         │
│ {COLORS['CYAN']}7{COLORS['END']} │ 💾 Save & Back to Menu                      │
│ {COLORS['WHITE']}0{COLORS['END']} │ ⬅️  Back without Saving                      │
{COLORS['BLUE']}└─────────────────────────────────────────────────┘{COLORS['END']}
        """)
        
        choice = input(f"\n{COLORS['BOLD']}🎯 {get_message('select_option', config)} (0-7): {COLORS['END']}").strip()
        
        if choice == '1':
            config = change_ui_language(config)
        elif choice == '2':
            config = change_commit_language(config)
        elif choice == '3':
            config = update_api_key(config)
        elif choice == '4':
            config = change_ai_model(config)
        elif choice == '5':
            config = change_commit_style(config)
        elif choice == '6':
            config = toggle_auto_push(config)
        elif choice == '7':
            save_config(config)
            print_success(get_message('save_exit', config))
            return config
        elif choice == '0':
            return config
        else:
            print_error(get_message('invalid_option', config))

def change_ui_language(config: Dict) -> Dict:
    """Change interface language."""
    print_section("🌐 Change Interface Language")
    print(f"""
{COLORS['BLUE']}Available Languages:{COLORS['END']}
1️⃣  🇺🇸 English
2️⃣  🇻🇳 Tiếng Việt
    """)
    
    while True:
        choice = input(f"{COLORS['BOLD']}Select language (1-2): {COLORS['END']}").strip()
        if choice == '1':
            config['ui_language'] = 'en'
            print_success("✅ Interface language changed to English!")
            break
        elif choice == '2':
            config['ui_language'] = 'vi'
            print_success("✅ Đã thay đổi ngôn ngữ giao diện sang Tiếng Việt!")
            break
        else:
            print_error("❌ Invalid choice. Please select 1 or 2.")
    
    return config

def change_commit_language(config: Dict) -> Dict:
    """Change commit message language."""
    print_section("💬 Change Commit Language")
    print(f"""
{COLORS['BLUE']}Available Languages:{COLORS['END']}
1️⃣  🇺🇸 English (feat: add user authentication)
2️⃣  🇻🇳 Tiếng Việt (feat: thêm xác thực người dùng)
    """)
    
    while True:
        choice = input(f"{COLORS['BOLD']}Select language (1-2): {COLORS['END']}").strip()
        if choice == '1':
            config['commit_language'] = 'en'
            print_success("✅ Commit language changed to English!")
            break
        elif choice == '2':
            config['commit_language'] = 'vi'
            print_success("✅ Đã thay đổi ngôn ngữ commit sang Tiếng Việt!")
            break
        else:
            print_error("❌ Invalid choice. Please select 1 or 2.")
    
    return config

def update_api_key(config: Dict) -> Dict:
    """Update Gemini API key."""
    print_section("🔑 Update API Key")
    
    current_key = config.get('api_key', '')
    if current_key:
        masked_key = current_key[:8] + '*' * (len(current_key) - 12) + current_key[-4:] if len(current_key) > 12 else '*' * len(current_key)
        print(f"Current API key: {COLORS['DIM']}{masked_key}{COLORS['END']}")
    
    new_key = input(f"\n{COLORS['BOLD']}🔑 Enter new API key (or press Enter to keep current): {COLORS['END']}").strip()
    
    if new_key:
        config['api_key'] = new_key
        print_success("✅ API key updated successfully!")
    else:
        print_info("ℹ️  API key unchanged.")
    
    return config

def change_ai_model(config: Dict) -> Dict:
    """Change AI model."""
    print_section("🤖 Change AI Model")
    print(f"""
{COLORS['BLUE']}Available Models:{COLORS['END']}
1️⃣  🚀 Gemini 2.0 Flash - {COLORS['GREEN']}Recommended{COLORS['END']} (Best quality, faster)
2️⃣  ⚡ Gemini 2.0 Flash-Lite - {COLORS['YELLOW']}Cost-effective{COLORS['END']} (Good quality, cheaper)
    """)
    
    current_model = "1" if config.get('model', 'gemini-2.0-flash') == 'gemini-2.0-flash' else "2"
    print(f"Current selection: {current_model}")
    
    while True:
        choice = input(f"{COLORS['BOLD']}Select model (1-2): {COLORS['END']}").strip()
        if choice == '1':
            config['model'] = 'gemini-2.0-flash'
            print_success("🚀 Changed to Gemini 2.0 Flash!")
            break
        elif choice == '2':
            config['model'] = 'gemini-2.0-flash-lite'
            print_success("⚡ Changed to Gemini 2.0 Flash-Lite!")
            break
        else:
            print_error("❌ Invalid choice. Please select 1 or 2.")
    
    return config

def change_commit_style(config: Dict) -> Dict:
    """Change commit message style."""
    print_section("🎨 Change Commit Style")
    print(f"""
{COLORS['BLUE']}Available Styles:{COLORS['END']}

1️⃣  📋 {COLORS['BOLD']}Conventional Commits{COLORS['END']}
    Example: {COLORS['GREEN']}feat: add user authentication system{COLORS['END']}
    
2️⃣  😄 {COLORS['BOLD']}Emoji Style{COLORS['END']}  
    Example: {COLORS['GREEN']}✨ add user authentication system{COLORS['END']}
    
3️⃣  📝 {COLORS['BOLD']}Descriptive{COLORS['END']}
    Example: {COLORS['GREEN']}Add comprehensive user authentication system{COLORS['END']}
    """)
    
    current_style = config.get('commit_style', 'conventional')
    style_map = {'conventional': '1', 'emoji': '2', 'descriptive': '3'}
    print(f"Current selection: {style_map.get(current_style, '1')}")
    
    while True:
        choice = input(f"{COLORS['BOLD']}Select style (1-3): {COLORS['END']}").strip()
        if choice == '1':
            config['commit_style'] = 'conventional'
            print_success("📋 Changed to Conventional Commits!")
            break
        elif choice == '2':
            config['commit_style'] = 'emoji'
            print_success("😄 Changed to Emoji Style!")
            break
        elif choice == '3':
            config['commit_style'] = 'descriptive'
            print_success("📝 Changed to Descriptive Style!")
            break
        else:
            print_error("❌ Invalid choice. Please select 1, 2, or 3.")
    
    return config

def toggle_auto_push(config: Dict) -> Dict:
    """Toggle auto push setting."""
    print_section("🚀 Toggle Auto Push")
    
    current_status = config.get('auto_push', False)
    status_text = "enabled" if current_status else "disabled"
    new_status = not current_status
    new_status_text = "enable" if new_status else "disable"
    
    print(f"Auto push is currently {COLORS['BOLD']}{status_text}{COLORS['END']}")
    
    confirm = input(f"Do you want to {COLORS['BOLD']}{new_status_text}{COLORS['END']} auto push? (y/N): ").lower()
    
    if confirm in ['y', 'yes']:
        config['auto_push'] = new_status
        emoji = "✅" if new_status else "❌"
        action = "enabled" if new_status else "disabled"
        print_success(f"{emoji} Auto push {action}!")
    else:
        print_info("ℹ️  Auto push setting unchanged.")
    
    return config

def show_help(config: Dict) -> None:
    """Show help information."""
    print_header("❓ Help & Information")
    print(get_message('help_text', config))
    input(f"\n{COLORS['DIM']}Press Enter to continue...{COLORS['END']}")

def confirm_action(message: str) -> bool:
    """Confirm dangerous actions."""
    print_warning(message)
    confirm = input("Type 'yes' to confirm: ").lower().strip()
    return confirm == 'yes'