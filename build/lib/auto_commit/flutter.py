#!/usr/bin/env python3
import os
import sys
import subprocess
from typing import Optional, Dict

# Translations for all messages
MESSAGES = {
    'en': {
        'menu_title': "🛠️  Flutter Development Tools",
        'menu_items': [
            "Build App Bundle (clean + build)",
            "Setup Wireless Debugging",
            "Uninstall App",
            "Clean Project",
            "Get Dependencies",
            "Run Flutter Doctor",
            "Setup Development Environment"
        ],
        'enter_choice': "Enter your choice (0-7): ",
        'error_cmd': "Error executing command: ",
        'building': "Building App Bundle...",
        'executing': "Executing: ",
        'build_failed': "Build failed at step: ",
        'build_success': "App Bundle built successfully!",
        'ip_error': "Error: Could not get device IP. Make sure device is connected via USB.",
        'setup_wireless': "Setting up wireless debugging for IP: ",
        'tcp_success': "Enabled TCP/IP mode successfully",
        'connect_success': "Successfully connected to ",
        'wireless_ready': "You can now unplug the USB cable and debug wirelessly!",
        'connect_failed': "Failed to connect to device",
        'tcp_failed': "Failed to enable TCP/IP mode",
        'pkg_detect_error': "Error: Could not detect package name from pubspec.yaml",
        'enter_pkg_manual': "Please enter the package name manually: ",
        'no_pkg_cancel': "No package name provided. Operation cancelled.",
        'uninstalling': "Uninstalling ",
        'uninstall_success': "Successfully uninstalled ",
        'uninstall_failed': "Failed to uninstall ",
        'detected_pkg': "Detected package name: ",
        'use_pkg': "Use this package name? (Y/n): ",
        'enter_pkg': "Enter package name: ",
        'enter_ip': "Enter device IP (press Enter to detect automatically): ",
        'invalid_choice': "Invalid choice. Please try again.",
        'press_continue': "Press Enter to continue...",
        'no_devices': "No Android devices found. Please connect a device via USB.",
        'select_device': "Select a device to uninstall from:",
        'enter_device_choice': "Enter device number (or press Enter to cancel): ",
        'invalid_device_choice': "Invalid device selection. Please try again.",
        'setup_env_title': "Development Environment Setup",
        'select_ide': "Select IDE to install:",
        'ide_options': [
            "Visual Studio Code",
            "Android Studio",
            "Both"
        ],
        'installing': "Installing ",
        'setup_success': "Setup completed successfully!",
        'setup_failed': "Setup failed: ",
        'select_flutter_version': "Select Flutter version to install:",
        'downloading': "Downloading ",
        'extracting': "Extracting ",
        'configuring': "Configuring environment...",
        'installing_deps': "Installing dependencies...",
        'setup_complete': "Environment setup complete!",
        'already_installed': "Already installed: ",
        'checking_installed': "Checking installed components...",
        'setup_instructions': """
Setup will include:
1. Install required system packages
2. Install selected IDE(s)
3. Install Flutter SDK
4. Configure environment variables
5. Install Android SDK
6. Verify installation
"""
    },
    'vi': {
        'menu_title': "🛠️  Công Cụ Phát Triển Flutter",
        'menu_items': [
            "Tạo App Bundle (clean + build)",
            "Thiết lập Debug không dây",
            "Gỡ cài đặt ứng dụng",
            "Dọn dẹp dự án",
            "Cập nhật Dependencies",
            "Chạy Flutter Doctor",
            "Thiết lập Môi trường Phát triển"
        ],
        'enter_choice': "Nhập lựa chọn của bạn (0-7): ",
        'error_cmd': "Lỗi thực thi lệnh: ",
        'building': "Đang tạo App Bundle...",
        'executing': "Đang thực thi: ",
        'build_failed': "Tạo bundle thất bại ở bước: ",
        'build_success': "Tạo App Bundle thành công!",
        'ip_error': "Lỗi: Không thể lấy IP thiết bị. Hãy đảm bảo thiết bị được kết nối qua USB.",
        'setup_wireless': "Đang thiết lập debug không dây cho IP: ",
        'tcp_success': "Đã bật chế độ TCP/IP thành công",
        'connect_success': "Đã kết nối thành công tới ",
        'wireless_ready': "Bạn có thể rút cáp USB và debug không dây!",
        'connect_failed': "Không thể kết nối tới thiết bị",
        'tcp_failed': "Không thể bật chế độ TCP/IP",
        'pkg_detect_error': "Lỗi: Không thể tìm thấy package name trong pubspec.yaml",
        'enter_pkg_manual': "Vui lòng nhập package name thủ công: ",
        'no_pkg_cancel': "Không có package name. Đã hủy thao tác.",
        'uninstalling': "Đang gỡ cài đặt ",
        'uninstall_success': "Đã gỡ cài đặt thành công ",
        'uninstall_failed': "Không thể gỡ cài đặt ",
        'detected_pkg': "Đã phát hiện package name: ",
        'use_pkg': "Sử dụng package name này? (Y/n): ",
        'enter_pkg': "Nhập package name: ",
        'enter_ip': "Nhập IP thiết bị (nhấn Enter để tự động phát hiện): ",
        'invalid_choice': "Lựa chọn không hợp lệ. Vui lòng thử lại.",
        'press_continue': "Nhấn Enter để tiếp tục...",
        'no_devices': "Không tìm thấy thiết bị Android nào. Vui lòng kết nối thiết bị qua USB.",
        'select_device': "Chọn thiết bị để gỡ cài đặt:",
        'enter_device_choice': "Nhập số thiết bị (hoặc nhấn Enter để hủy): ",
        'invalid_device_choice': "Lựa chọn thiết bị không hợp lệ. Vui lòng thử lại.",
        'setup_env_title': "Thiết lập Môi trường Phát triển",
        'select_ide': "Chọn IDE để cài đặt:",
        'ide_options': [
            "Visual Studio Code",
            "Android Studio",
            "Cả hai"
        ],
        'installing': "Đang cài đặt ",
        'setup_success': "Thiết lập hoàn tất thành công!",
        'setup_failed': "Thiết lập thất bại: ",
        'select_flutter_version': "Chọn phiên bản Flutter để cài đặt:",
        'downloading': "Đang tải xuống ",
        'extracting': "Đang giải nén ",
        'configuring': "Đang cấu hình môi trường...",
        'installing_deps': "Đang cài đặt các gói phụ thuộc...",
        'setup_complete': "Thiết lập môi trường hoàn tất!",
        'already_installed': "Đã được cài đặt: ",
        'checking_installed': "Đang kiểm tra các thành phần đã cài đặt...",
        'setup_instructions': """
Quá trình thiết lập bao gồm:
1. Cài đặt các gói hệ thống cần thiết
2. Cài đặt IDE đã chọn
3. Cài đặt Flutter SDK
4. Cấu hình biến môi trường
5. Cài đặt Android SDK
6. Kiểm tra cài đặt
"""
    }
}

def get_message(key: str, lang: str) -> str:
    """Get translated message."""
    return MESSAGES[lang][key]

def run_command(command: str, lang: str = 'en') -> bool:
    """Run a shell command and return True if successful."""
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\033[91m{get_message('error_cmd', lang)}{e}\033[0m")
        return False

def get_device_ip() -> Optional[str]:
    """Get the IP address of the connected Android device."""
    try:
        result = subprocess.run(
            ['adb', 'shell', 'ip', 'route'], 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0:
            # Parse the output to get IP address
            for line in result.stdout.split('\n'):
                if 'wlan0' in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == 'src':
                            return parts[i + 1]
        return None
    except Exception:
        return None

def get_android_devices(lang: str = 'en') -> list:
    """Get list of connected Android devices."""
    try:
        result = subprocess.run(
            ['adb', 'devices', '-l'],
            capture_output=True,
            text=True
        )
        devices = []
        lines = result.stdout.strip().split('\n')[1:]  # Skip first line (header)
        
        for line in lines:
            if line.strip():
                parts = line.split()
                if len(parts) >= 2 and 'unauthorized' not in line and 'offline' not in line:
                    device_id = parts[0]
                    # Get device model
                    model_result = subprocess.run(
                        ['adb', '-s', device_id, 'shell', 'getprop', 'ro.product.model'],
                        capture_output=True,
                        text=True
                    )
                    model = model_result.stdout.strip() or device_id
                    # Only add if it's a mobile device (not emulator/desktop)
                    if not any(x in line.lower() for x in ['desktop', 'linux', 'chrome', 'web']):
                        devices.append({
                            'id': device_id,
                            'name': f"{model} ({device_id})"
                        })
        return devices
    except Exception as e:
        print(f"\033[91mError getting devices: {e}\033[0m")
        return []

def select_device(devices: list, lang: str = 'en') -> Optional[str]:
    """Show device selection menu and return selected device ID."""
    if not devices:
        print(f"\033[91m{get_message('no_devices', lang)}\033[0m")
        return None
    
    print(f"\n{get_message('select_device', lang)}")
    for i, device in enumerate(devices, 1):
        print(f"{i}) {device['name']}")
    
    while True:
        try:
            choice = input(f"\n{get_message('enter_device_choice', lang)}")
            if not choice.strip():
                return None
            
            idx = int(choice) - 1
            if 0 <= idx < len(devices):
                return devices[idx]['id']
        except ValueError:
            pass
        print(f"\033[91m{get_message('invalid_device_choice', lang)}\033[0m")

def setup_wireless_debug(ip: Optional[str] = None, lang: str = 'en') -> None:
    """Setup wireless debugging for Flutter."""
    if not ip:
        ip = get_device_ip()
        if not ip:
            print(f"\033[91m{get_message('ip_error', lang)}\033[0m")
            return

    print(f"\n\033[94m{get_message('setup_wireless', lang)}{ip}\033[0m")
    
    if run_command('adb tcpip 5555', lang):
        print(f"\033[92m{get_message('tcp_success', lang)}\033[0m")
        
        if run_command(f'adb connect {ip}:5555', lang):
            print(f"\033[92m{get_message('connect_success', lang)}{ip}:5555\033[0m")
            print(f"\n\033[93m{get_message('wireless_ready', lang)}\033[0m")
        else:
            print(f"\033[91m{get_message('connect_failed', lang)}\033[0m")
    else:
        print(f"\033[91m{get_message('tcp_failed', lang)}\033[0m")

def build_app_bundle(lang: str = 'en') -> None:
    """Build Android App Bundle with cleanup."""
    print(f"\n\033[94m{get_message('building', lang)}\033[0m")
    commands = [
        "flutter clean",
        "flutter pub get",
        "flutter build appbundle"
    ]
    
    for cmd in commands:
        print(f"\n\033[93m{get_message('executing', lang)}{cmd}\033[0m")
        if not run_command(cmd, lang):
            print(f"\033[91m{get_message('build_failed', lang)}{cmd}\033[0m")
            return
    
    print(f"\n\033[92m{get_message('build_success', lang)}\033[0m")

def find_pubspec() -> Optional[str]:
    """Find pubspec.yaml file in current directory or subdirectories."""
    # First check current directory
    if os.path.exists('pubspec.yaml'):
        return 'pubspec.yaml'
    
    # Then check immediate subdirectories
    for item in os.listdir('.'):
        if os.path.isdir(item):
            pubspec_path = os.path.join(item, 'pubspec.yaml')
            if os.path.exists(pubspec_path):
                return pubspec_path
    
    return None

def get_package_name() -> Optional[str]:
    """Get package name from pubspec.yaml file."""
    pubspec_path = find_pubspec()
    if not pubspec_path:
        return None

    try:
        with open(pubspec_path, 'r') as f:
            content = f.read()
            name = None
            org = None
            
            # Parse pubspec.yaml
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('name:'):
                    name = line.split('name:')[1].strip()
                elif 'applicationId' in line:  # build.gradle style
                    return line.split('applicationId')[1].strip().strip('"\'')
                elif 'PACKAGE_NAME' in line:  # Alternative style
                    return line.split('PACKAGE_NAME')[1].strip().strip('"\'')
            
            # If we found a name, construct the package name
            if name:
                # Check android/app/build.gradle for organization
                gradle_path = os.path.join(os.path.dirname(pubspec_path), 'android/app/build.gradle')
                if os.path.exists(gradle_path):
                    with open(gradle_path, 'r') as f:
                        gradle_content = f.read()
                        for line in gradle_content.split('\n'):
                            if 'applicationId' in line:
                                org = line.split('applicationId')[1].strip().strip('"\'').rsplit('.', 1)[0]
                                break
                
                # Use default org if not found
                if not org:
                    org = "com.zenoravn"
                
                return f"{org}.{name}"
            
    except Exception as e:
        print(f"\033[91mError reading package info: {e}\033[0m")
    return None

def uninstall_app(package_name: str = None, lang: str = 'en') -> None:
    """Uninstall app from connected device."""
    if not package_name:
        package_name = get_package_name()
        if not package_name:
            print(f"\033[91m{get_message('pkg_detect_error', lang)}\033[0m")
            package_name = input(f"\n{get_message('enter_pkg_manual', lang)}").strip()
            if not package_name:
                print(f"\033[91m{get_message('no_pkg_cancel', lang)}\033[0m")
                return
    
    # Get available devices
    devices = get_android_devices(lang)
    if not devices:
        print(f"\033[91m{get_message('no_devices', lang)}\033[0m")
        return
    
    # If multiple devices, let user select one
    device_id = devices[0]['id'] if len(devices) == 1 else select_device(devices, lang)
    if not device_id:
        return
    
    print(f"\n\033[94m{get_message('uninstalling', lang)}{package_name}...\033[0m")
    if run_command(f'adb -s {device_id} shell pm uninstall {package_name}', lang):
        print(f"\033[92m{get_message('uninstall_success', lang)}{package_name}\033[0m")
    else:
        print(f"\033[91m{get_message('uninstall_failed', lang)}{package_name}\033[0m")

def check_vscode_installed() -> bool:
    """Check if VSCode is installed."""
    try:
        result = subprocess.run(['which', 'code'], capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False

def check_android_studio_installed() -> bool:
    """Check if Android Studio is installed."""
    try:
        result = subprocess.run(['which', 'android-studio'], capture_output=True, text=True)
        return result.returncode == 0 or os.path.exists('/usr/local/android-studio')
    except Exception:
        return False

def check_flutter_installed() -> bool:
    """Check if Flutter SDK is installed."""
    try:
        result = subprocess.run(['which', 'flutter'], capture_output=True, text=True)
        if result.returncode == 0:
            # Also check if it's working properly
            version_result = subprocess.run(['flutter', '--version'], capture_output=True, text=True)
            return version_result.returncode == 0
        return False
    except Exception:
        return False

def install_vscode(lang: str = 'en') -> bool:
    """Install Visual Studio Code on Ubuntu."""
    if check_vscode_installed():
        print(f"\n\033[93m{get_message('already_installed', lang)}Visual Studio Code\033[0m")
        # Just install/update Flutter extension
        run_command('code --install-extension Dart-Code.flutter', lang)
        return True

    print(f"\n\033[94m{get_message('installing', lang)}Visual Studio Code...\033[0m")
    
    try:
        # Add Microsoft GPG key and repository
        run_command('wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg', lang)
        run_command('sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg', lang)
        run_command('sudo sh -c \'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list\'', lang)
        
        # Install VSCode
        run_command('sudo apt-get update', lang)
        if run_command('sudo apt-get install -y code', lang):
            # Install Flutter extension
            run_command('code --install-extension Dart-Code.flutter', lang)
            return True
    except Exception as e:
        print(f"\033[91m{get_message('setup_failed', lang)}{e}\033[0m")
    
    return False

def install_android_studio(lang: str = 'en') -> bool:
    """Install Android Studio on Ubuntu."""
    if check_android_studio_installed():
        print(f"\n\033[93m{get_message('already_installed', lang)}Android Studio\033[0m")
        return True

    print(f"\n\033[94m{get_message('installing', lang)}Android Studio...\033[0m")
    
    try:
        # Add repository and install
        run_command('sudo add-apt-repository -y ppa:maarten-fonville/android-studio', lang)
        run_command('sudo apt-get update', lang)
        return run_command('sudo apt-get install -y android-studio', lang)
    except Exception as e:
        print(f"\033[91m{get_message('setup_failed', lang)}{e}\033[0m")
    
    return False

def install_flutter_sdk(lang: str = 'en') -> bool:
    """Install Flutter SDK."""
    if check_flutter_installed():
        print(f"\n\033[93m{get_message('already_installed', lang)}Flutter SDK\033[0m")
        return True

    print(f"\n\033[94m{get_message('installing', lang)}Flutter SDK...\033[0m")
    
    try:
        # Install dependencies
        print(f"\n{get_message('installing_deps', lang)}")
        deps = [
            'curl',
            'git',
            'unzip',
            'xz-utils',
            'zip',
            'libglu1-mesa',
            'openjdk-11-jdk'
        ]
        run_command(f'sudo apt-get install -y {" ".join(deps)}', lang)
        
        # Download and extract Flutter SDK
        home = os.path.expanduser('~')
        sdk_path = os.path.join(home, 'development', 'flutter')
        
        if not os.path.exists(os.path.dirname(sdk_path)):
            os.makedirs(os.path.dirname(sdk_path))
        
        print(f"\n{get_message('downloading', lang)}Flutter SDK...")
        run_command('curl -O https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_3.19.3-stable.tar.xz', lang)
        
        print(f"\n{get_message('extracting', lang)}Flutter SDK...")
        run_command('tar xf flutter_linux_3.19.3-stable.tar.xz -C ~/development', lang)
        
        # Add to PATH
        print(f"\n{get_message('configuring', lang)}")
        bashrc_path = os.path.join(home, '.bashrc')
        flutter_path = f'export PATH="$PATH:{sdk_path}/bin"'
        
        with open(bashrc_path, 'a') as f:
            f.write(f'\n# Flutter\n{flutter_path}\n')
        
        # Initial setup
        os.environ['PATH'] = f"{os.environ['PATH']}:{sdk_path}/bin"
        run_command('flutter precache', lang)
        run_command('flutter doctor --android-licenses', lang)
        
        return True
    except Exception as e:
        print(f"\033[91m{get_message('setup_failed', lang)}{e}\033[0m")
    
    return False

def setup_environment(lang: str = 'en') -> None:
    """Setup development environment."""
    print(f"\n{get_message('setup_instructions', lang)}")
    
    # Check what's already installed
    print(f"\n{get_message('checking_installed', lang)}")
    vscode_installed = check_vscode_installed()
    android_studio_installed = check_android_studio_installed()
    flutter_installed = check_flutter_installed()
    
    if vscode_installed:
        print(f"\033[93m{get_message('already_installed', lang)}Visual Studio Code\033[0m")
    if android_studio_installed:
        print(f"\033[93m{get_message('already_installed', lang)}Android Studio\033[0m")
    if flutter_installed:
        print(f"\033[93m{get_message('already_installed', lang)}Flutter SDK\033[0m")
    
    # Only show IDE selection if not all are installed
    if not (vscode_installed and android_studio_installed):
        print(f"\n{get_message('select_ide', lang)}")
        ide_options = get_message('ide_options', lang)
        for i, option in enumerate(ide_options, 1):
            print(f"{i}) {option}")
        
        while True:
            try:
                choice = int(input("\nEnter choice (1-3): "))
                if 1 <= choice <= 3:
                    break
            except ValueError:
                pass
            print(f"\033[91m{get_message('invalid_choice', lang)}\033[0m")
        
        # Install selected IDE(s)
        if choice in [1, 3] and not vscode_installed:
            if not install_vscode(lang):
                return
        if choice in [2, 3] and not android_studio_installed:
            if not install_android_studio(lang):
                return
    
    # Install Flutter SDK if not installed
    if not flutter_installed:
        if not install_flutter_sdk(lang):
            return
    
    print(f"\n\033[92m{get_message('setup_complete', lang)}\033[0m")

def show_flutter_menu(config: Dict = None):
    """Show interactive Flutter tools menu."""
    lang = 'vi' if config and config.get('ui_language') == 'vi' else 'en'
    
    while True:
        print(f"""
\033[94m{get_message('menu_title', lang)}\033[0m
================================""")
        for i, item in enumerate(get_message('menu_items', lang), 1):
            print(f"{i}) {item}")
        print("0) Exit\n")
        
        choice = input(get_message('enter_choice', lang))
        
        if choice == '1':
            build_app_bundle(lang)
        elif choice == '2':
            ip = input(f"\n{get_message('enter_ip', lang)}").strip()
            setup_wireless_debug(ip if ip else None, lang)
        elif choice == '3':
            detected_pkg = get_package_name()
            if detected_pkg:
                print(f"\n\033[93m{get_message('detected_pkg', lang)}{detected_pkg}\033[0m")
                if input(get_message('use_pkg', lang)).lower() not in ['n', 'no']:
                    uninstall_app(detected_pkg, lang)
                    input(f"\n{get_message('press_continue', lang)}")
                    continue
            pkg = input(f"\n{get_message('enter_pkg', lang)}").strip()
            if pkg:
                uninstall_app(pkg, lang)
        elif choice == '4':
            run_command('flutter clean', lang)
        elif choice == '5':
            run_command('flutter pub get', lang)
        elif choice == '6':
            run_command('flutter doctor', lang)
        elif choice == '7':
            setup_environment(lang)
        elif choice == '0':
            break
        else:
            print(f"\033[91m{get_message('invalid_choice', lang)}\033[0m")
        
        input(f"\n{get_message('press_continue', lang)}")

if __name__ == "__main__":
    show_flutter_menu()