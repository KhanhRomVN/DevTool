# dev_tool/ui.py
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
    
    # Language settings - use the translated messages
    ui_lang_display = get_message('lang_1', config) if config['ui_language'] == 'en' else get_message('lang_2', config)
    commit_lang_display = get_message('lang_1', config) if config['commit_language'] == 'en' else get_message('lang_2', config)
    
    # Commit style display - use translated messages
    style_map = {
        'conventional': '📋 ' + ('Conventional Commits' if config['ui_language'] == 'en' else 'Conventional Commits'),
        'emoji': '😄 ' + ('Emoji Style' if config['ui_language'] == 'en' else 'Emoji Style'), 
        'descriptive': '📝 ' + ('Descriptive' if config['ui_language'] == 'en' else 'Descriptive')
    }
    style_display = style_map.get(config.get('commit_style', 'conventional'), '📋 Conventional')
    
    # Model display
    model_display = {
        'gemini-2.0-flash': '🚀 Gemini 2.0 Flash',
        'gemini-2.0-flash-lite': '⚡ Gemini 2.0 Flash-Lite',
        'gemini-2.5-pro': '🚀 Gemini 2.5 Pro',
        'gemini-2.5-flash': '⚡ Gemini 2.5 Flash',
        'gemini-2.5-flash-lite': '💡 Gemini 2.5 Flash-Lite'
    }.get(config.get('model', 'gemini-2.0-flash'), '🚀 Gemini 2.0 Flash')
    
    # Get account info
    primary_account = None
    for account in config.get('accounts', []):
        if account.get('is_primary', False):
            primary_account = account
            break
    
    account_info = ""
    if primary_account:
        email = primary_account.get('email', 'No email')
        model = primary_account.get('model', 'Unknown model')
        account_info = f"{COLORS['YELLOW']}📧 Primary Account:{COLORS['END']} {email}\n{COLORS['YELLOW']}🤖 Account Model:{COLORS['END']}   {model}\n"
    
    print(f"""
{COLORS['CYAN']}==================================================={COLORS['END']}
{COLORS['BOLD']}{get_message('current_config', config).center(51)}{COLORS['END']}
{COLORS['CYAN']}---------------------------------------------------{COLORS['END']}
{COLORS['YELLOW']}🌐 {get_message('ui_lang', config)}:{COLORS['END']} {ui_lang_display}
{COLORS['YELLOW']}💬 {get_message('commit_lang', config)}:{COLORS['END']}   {commit_lang_display}
{COLORS['YELLOW']}🎨 {get_message('commit_style', config)}:{COLORS['END']}      {style_display}
{account_info}{COLORS['YELLOW']}🚀 {get_message('auto_push', config)}:{COLORS['END']}         {get_status_display(config.get('auto_push', False), config)}
{COLORS['YELLOW']}📦 {get_message('auto_stage', config)}:{COLORS['END']}        {get_status_display(config.get('auto_stage', False), config)}
{COLORS['CYAN']}==================================================={COLORS['END']}
    """)

def get_status_display(enabled: bool, config: Dict) -> str:
    """Get colored status display with translation."""
    if enabled:
        return f"{COLORS['GREEN']}✅ {get_message('enabled', config)}{COLORS['END']}"
    else:
        return f"{COLORS['RED']}❌ {get_message('disabled', config)}{COLORS['END']}"

def show_settings_interface(config: Dict) -> None:
    """Show the main settings interface."""
    while True:
        print_header(get_message('settings_menu', config))
        show_current_config(config)
        
        options_text = f"""
{COLORS['BLUE']}==================================================={COLORS['END']}
{COLORS['BOLD']}{get_message('options', config).center(51)}{COLORS['END']}
{COLORS['BLUE']}---------------------------------------------------{COLORS['END']}
{COLORS['GREEN']}1{COLORS['END']} │ ⚙️  {get_message('edit_config', config)}
{COLORS['YELLOW']}2{COLORS['END']} │ 🔄 {get_message('reset_defaults', config)}
{COLORS['RED']}3{COLORS['END']} │ 🗑️  {get_message('uninstall_tool', config)}
{COLORS['CYAN']}4{COLORS['END']} │ ❓ {get_message('help_info', config)}
{COLORS['WHITE']}0{COLORS['END']} │ 🚪 {get_message('exit', config)}
{COLORS['BLUE']}==================================================={COLORS['END']}
        """
        print(options_text)
        
        choice = input(f"\n{COLORS['BOLD']}🎯 {get_message('select_option', config)} (0-4): {COLORS['END']}").strip()
        
        if choice == '1':
            config = show_configuration_interface(config)
        elif choice == '2':
            if confirm_action(get_message('reset_confirm', config), config):
                config = reset_config()
        elif choice == '3':
            if confirm_action(get_message('uninstall_confirm', config), config):
                uninstall_tool()
                return
        elif choice == '4':
            show_help(config)
        elif choice == '0':
            print_success("👋 " + get_message('exit', config))
            break
        else:
            print_error(get_message('invalid_option', config))

def show_configuration_interface(config: Dict) -> Dict:
    """Show detailed configuration interface."""
    while True:
        print_header("⚙️  " + get_message('edit_config', config))
        show_current_config(config)
        
        edit_options = f"""
{COLORS['BLUE']}==================================================={COLORS['END']}
{COLORS['BOLD']}{get_message('edit_options', config).center(51)}{COLORS['END']}
{COLORS['BLUE']}---------------------------------------------------{COLORS['END']}
{COLORS['GREEN']}1{COLORS['END']} │ 🌐 {get_message('change_ui_lang', config)}
{COLORS['GREEN']}2{COLORS['END']} │ 💬 {get_message('change_commit_lang', config)}
{COLORS['GREEN']}3{COLORS['END']} │ 🔑 {get_message('update_api_key', config)}
{COLORS['GREEN']}4{COLORS['END']} │ 🤖 {get_message('change_ai_model', config)}
{COLORS['GREEN']}5{COLORS['END']} │ 🎨 {get_message('change_commit_style', config)}
{COLORS['GREEN']}6{COLORS['END']} │ 🚀 {get_message('toggle_auto_push', config)}
{COLORS['CYAN']}7{COLORS['END']} │ 💾 {get_message('save_back', config)}
{COLORS['WHITE']}0{COLORS['END']} │ ⬅️  {get_message('back_no_save', config)}
{COLORS['BLUE']}==================================================={COLORS['END']}
        """
        print(edit_options)
        
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
    print_section("🌐 " + get_message('change_ui_lang', config))
    print(f"""
{COLORS['BLUE']}{get_message('available_langs', config)}:{COLORS['END']}
1️⃣  🇺🇸 {get_message('lang_1', config)}
2️⃣  🇻🇳 {get_message('lang_2', config)}
    """)
    
    while True:
        choice = input(f"{COLORS['BOLD']}{get_message('select_lang', config)} (1-2): {COLORS['END']}").strip()
        if choice == '1':
            config['ui_language'] = 'en'
            print_success("✅ " + ("Interface language changed to English!" if config['ui_language'] == 'en' else "Đã thay đổi ngôn ngữ giao diện sang Tiếng Anh!"))
            break
        elif choice == '2':
            config['ui_language'] = 'vi'
            print_success("✅ " + ("Interface language changed to Vietnamese!" if config['ui_language'] == 'en' else "Đã thay đổi ngôn ngữ giao diện sang Tiếng Việt!"))
            break
        else:
            print_error(get_message('invalid_choice', config))
    
    return config

def change_commit_language(config: Dict) -> Dict:
    """Change commit message language."""
    print_section("💬 " + get_message('change_commit_lang', config))
    print(f"""
{COLORS['BLUE']}{get_message('available_langs', config)}:{COLORS['END']}
1️⃣  🇺🇸 {get_message('lang_1', config)} (feat: add user authentication)
2️⃣  🇻🇳 {get_message('lang_2', config)} (feat: thêm xác thực người dùng)
    """)
    
    while True:
        choice = input(f"{COLORS['BOLD']}{get_message('select_lang', config)} (1-2): {COLORS['END']}").strip()
        if choice == '1':
            config['commit_language'] = 'en'
            print_success("✅ " + ("Commit language changed to English!" if config['ui_language'] == 'en' else "Đã thay đổi ngôn ngữ commit sang Tiếng Anh!"))
            break
        elif choice == '2':
            config['commit_language'] = 'vi'
            print_success("✅ " + ("Commit language changed to Vietnamese!" if config['ui_language'] == 'en' else "Đã thay đổi ngôn ngữ commit sang Tiếng Việt!"))
            break
        else:
            print_error(get_message('invalid_choice', config))
    
    return config

def update_api_key(config: Dict) -> Dict:
    """Update Gemini API key."""
    print_section("🔑 " + get_message('update_api_key', config))
    
    # Get primary account
    primary_account = None
    account_index = -1
    for i, account in enumerate(config.get('accounts', [])):
        if account.get('is_primary', False):
            primary_account = account
            account_index = i
            break
    
    if primary_account:
        current_key = primary_account.get('api_key', '')
        if current_key:
            masked_key = current_key[:8] + '*' * (len(current_key) - 12) + current_key[-4:] if len(current_key) > 12 else '*' * len(current_key)
            print(f"Current API key: {COLORS['DIM']}{masked_key}{COLORS['END']}")
    
    new_key = input(f"\n{COLORS['BOLD']}{get_message('enter_api_key_prompt', config)}: {COLORS['END']}").strip()
    
    if new_key:
        if primary_account:
            config['accounts'][account_index]['api_key'] = new_key
        else:
            # Create new account if none exists
            config['accounts'] = [{
                "email": "primary@example.com",
                "api_key": new_key,
                "model": config.get('model', 'gemini-2.0-flash'),
                "is_primary": True
            }]
        print_success("✅ " + ("API key updated successfully!" if config['ui_language'] == 'en' else "Đã cập nhật API key thành công!"))
    else:
        print_info("ℹ️  " + ("API key unchanged." if config['ui_language'] == 'en' else "API key không thay đổi."))
    
    return config

def change_ai_model(config: Dict) -> Dict:
    """Change AI model."""
    print_section("🤖 " + get_message('change_ai_model', config))
    print(f"""
{COLORS['BLUE']}{get_message('available_models', config)}:{COLORS['END']}
1️⃣  🚀 Gemini 2.5 Pro - {COLORS['GREEN']}Recommended{COLORS['END']} (Best quality)
2️⃣  ⚡ Gemini 2.5 Flash - {COLORS['YELLOW']}Fast{COLORS['END']} (Good quality, fast)
3️⃣  💡 Gemini 2.5 Flash-Lite - {COLORS['BLUE']}Efficient{COLORS['END']} (Lightweight)
4️⃣  🚀 Gemini 2.0 Flash - {COLORS['DIM']}Legacy{COLORS['END']} (Compatible)
    """)
    
    # Get primary account model
    primary_model = 'gemini-2.0-flash'
    for account in config.get('accounts', []):
        if account.get('is_primary', False):
            primary_model = account.get('model', 'gemini-2.0-flash')
            break
    
    model_map = {
        'gemini-2.5-pro': '1',
        'gemini-2.5-flash': '2',
        'gemini-2.5-flash-lite': '3',
        'gemini-2.0-flash': '4'
    }
    
    current_choice = model_map.get(primary_model, '4')
    print(f"Current selection: {current_choice}")
    
    while True:
        choice = input(f"{COLORS['BOLD']}{get_message('select_model', config)} (1-4): {COLORS['END']}").strip()
        if choice in ['1', '2', '3', '4']:
            model_choices = {
                '1': 'gemini-2.5-pro',
                '2': 'gemini-2.5-flash',
                '3': 'gemini-2.5-flash-lite',
                '4': 'gemini-2.0-flash'
            }
            new_model = model_choices[choice]
            
            # Update primary account model
            for i, account in enumerate(config.get('accounts', [])):
                if account.get('is_primary', False):
                    config['accounts'][i]['model'] = new_model
                    break
            
            success_msgs = {
                '1': "🚀 Changed to Gemini 2.5 Pro!",
                '2': "⚡ Changed to Gemini 2.5 Flash!",
                '3': "💡 Changed to Gemini 2.5 Flash-Lite!",
                '4': "🚀 Changed to Gemini 2.0 Flash!"
            }
            print_success(success_msgs[choice])
            break
        else:
            print_error(get_message('invalid_choice', config))
    
    return config

def change_commit_style(config: Dict) -> Dict:
    """Change commit message style."""
    print_section("🎨 " + get_message('change_commit_style', config))
    print(f"""
{COLORS['BLUE']}{get_message('available_styles', config)}:{COLORS['END']}

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
        choice = input(f"{COLORS['BOLD']}{get_message('select_style', config)} (1-3): {COLORS['END']}").strip()
        if choice == '1':
            config['commit_style'] = 'conventional'
            print_success("📋 " + ("Changed to Conventional Commits!" if config['ui_language'] == 'en' else "Đã đổi sang Conventional Commits!"))
            break
        elif choice == '2':
            config['commit_style'] = 'emoji'
            print_success("😄 " + ("Changed to Emoji Style!" if config['ui_language'] == 'en' else "Đã đổi sang Emoji Style!"))
            break
        elif choice == '3':
            config['commit_style'] = 'descriptive'
            print_success("📝 " + ("Changed to Descriptive Style!" if config['ui_language'] == 'en' else "Đã đổi sang Descriptive Style!"))
            break
        else:
            print_error(get_message('invalid_choice', config))
    
    return config

def toggle_auto_push(config: Dict) -> Dict:
    """Toggle auto push setting."""
    print_section("🚀 " + get_message('toggle_auto_push', config))
    
    current_status = config.get('auto_push', False)
    status_text = get_message('enabled', config) if current_status else get_message('disabled', config)
    new_status = not current_status
    action_text = get_message('enable', config) if new_status else get_message('disable', config)
    
    print(f"{get_message('auto_push', config)} {get_message('is_currently', config)} {COLORS['BOLD']}{status_text}{COLORS['END']}")
    
    confirm = input(f"{get_message('confirm_toggle', config)} {COLORS['BOLD']}{action_text}{COLORS['END']}? (y/N): ").lower()
    
    if confirm in ['y', 'yes', 'có']:
        config['auto_push'] = new_status
        emoji = "✅" if new_status else "❌"
        status = get_message('enabled', config) if new_status else get_message('disabled', config)
        print_success(f"{emoji} {get_message('auto_push', config)} {status}!")
    else:
        print_info("ℹ️  " + ("Auto push setting unchanged." if config['ui_language'] == 'en' else "Cài đặt auto push không thay đổi."))
    
    return config

def show_help(config: Dict) -> None:
    """Show help information."""
    print_header("❓ " + get_message('help_info', config))
    print(get_message('help_text', config))
    input(f"\n{COLORS['DIM']}{get_message('press_enter_continue', config)}...{COLORS['END']}")

def confirm_action(message: str, config: Dict) -> bool:
    """Confirm dangerous actions."""
    print_warning(message)
    confirm = input(get_message('type_yes_confirm', config) if config['ui_language'] == 'en' else "Gõ 'yes' để xác nhận: ").lower().strip()
    return confirm == 'yes'