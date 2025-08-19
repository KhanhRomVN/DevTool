# dev_tool/ai_utils.py
#!/usr/bin/env python3
from typing import Dict, Optional, List
import sys
import google.generativeai as genai

from .messages import get_message, print_error, COLORS

def init_ai(api_key: str, model: str) -> genai.GenerativeModel:
    """Initialize the AI model with the given configuration."""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model)

def get_commit_prompt(commit_style: str, commit_language: str, diff_text: str) -> str:
    """Generate the appropriate commit prompt based on style and language."""
    
    # Extended commit types with more categories
    COMMIT_TYPES = {
        'en': {
            'feat': 'New feature',
            'fix': 'Bug fix',
            'docs': 'Documentation',
            'style': 'Code style/formatting',
            'refactor': 'Code refactoring',
            'perf': 'Performance improvement',
            'test': 'Testing',
            'chore': 'Maintenance tasks',
            'ci': 'CI/CD configuration',
            'build': 'Build system',
            'revert': 'Revert changes',
            'security': 'Security related',
            'config': 'Configuration changes',
            'database': 'Database changes',
            'ui': 'User interface changes',
            'i18n': 'Internationalization',
            'access': 'Accessibility',
            'analytics': 'Analytics tracking',
            'deprecate': 'Deprecation notices'
        },
        'vi': {
            'feat': 'Tính năng mới',
            'fix': 'Sửa lỗi',
            'docs': 'Tài liệu',
            'style': 'Định dạng/kiểu code',
            'refactor': 'Tái cấu trúc code',
            'perf': 'Cải thiện hiệu năng',
            'test': 'Kiểm thử',
            'chore': 'Công việc bảo trì',
            'ci': 'Cấu hình CI/CD',
            'build': 'Hệ thống build',
            'revert': 'Hoàn tác thay đổi',
            'security': 'Liên quan bảo mật',
            'config': 'Thay đổi cấu hình',
            'database': 'Thay đổi database',
            'ui': 'Thay đổi giao diện',
            'i18n': 'Quốc tế hóa',
            'access': 'Khả năng truy cập',
            'analytics': 'Theo dõi phân tích',
            'deprecate': 'Thông báo không dùng nữa'
        }
    }
    
    # Language-specific instructions
    lang_instructions = {
        'en': {
            'conventional': f"""
Generate a conventional commit message in English following these rules:
1. Format: type(scope): description
2. Types: {', '.join(COMMIT_TYPES['en'].keys())}
3. Keep title under 72 characters
4. Use imperative mood (add, fix, update, not added, fixed, updated)
5. Add 3-5 bullet points with specific details
6. No markdown formatting, keep plain text

Example format:
feat(auth): add user authentication system
- Implement login/logout functionality with JWT tokens
- Add password encryption using bcrypt with 12 rounds
- Create user session management with Redis storage
- Add email verification for new registrations
- Implement rate limiting on authentication endpoints
""",
            'emoji': f"""
Generate an emoji-style commit message in English following these rules:
1. Format: emoji description (no type prefix)
2. Use appropriate emoji for the change type:
   ✨ feat | 🐛 fix | 📚 docs | 💎 style | ♻️ refactor | ⚡ perf | 🧪 test | 🔧 chore | 👷 ci | 📦 build | ⏪ revert | 🔒 security | ⚙️ config | 🗄️ database | 🎨 ui | 🌐 i18n | ♿ access | 📊 analytics | 🗑️ deprecate
3. Keep title under 72 characters
4. Use imperative mood
5. Add 3-5 bullet points with specific details

Example format:
✨ add user authentication system
- Implement login/logout functionality with JWT tokens
- Add password encryption using bcrypt with 12 rounds  
- Create user session management with Redis storage
- Add email verification for new registrations
- Implement rate limiting on authentication endpoints
""",
            'descriptive': """
Generate a descriptive commit message in English following these rules:
1. Write a clear, descriptive title (no prefixes or emojis)
2. Capitalize first letter, no period at end
3. Keep title under 72 characters
4. Use imperative mood
5. Add 3-5 bullet points with specific details
6. Focus on what and why, not how

Example format:
Add comprehensive user authentication system with security enhancements
- Implement secure login and logout functionality using JWT tokens
- Include password encryption with bcrypt using 12 rounds for security
- Provide session management with Redis for scalability
- Add email verification process for new user registrations
- Implement rate limiting to prevent brute force attacks
"""
        },
        'vi': {
            'conventional': f"""
Tạo commit message theo quy ước conventional commits bằng tiếng Việt:
1. Định dạng: type(scope): mô tả
2. Types: {', '.join(COMMIT_TYPES['vi'].keys())}
3. Giữ tiêu đề dưới 72 ký tự
4. Sử dụng thể mệnh lệnh (thêm, sửa, cập nhật)
5. Thêm 3-5 điểm chi tiết cụ thể
6. Không sử dụng markdown, giữ văn bản thuần

Ví dụ định dạng:
feat(auth): thêm hệ thống xác thực người dùng
- Triển khai chức năng đăng nhập/đăng xuất với JWT tokens
- Thêm mã hóa mật khẩu bằng bcrypt với 12 rounds
- Tạo quản lý phiên người dùng với Redis storage
- Thêm xác thực email cho đăng ký mới
- Triển khai rate limiting trên endpoints xác thực
""",
            'emoji': f"""
Tạo commit message theo phong cách emoji bằng tiếng Việt:
1. Định dạng: emoji mô tả (không có tiền tố type)
2. Sử dụng emoji phù hợp:
   ✨ feat | 🐛 fix | 📚 docs | 💎 style | ♻️ refactor | ⚡ perf | 🧪 test | 🔧 chore | 👷 ci | 📦 build | ⏪ revert | 🔒 security | ⚙️ config | 🗄️ database | 🎨 ui | 🌐 i18n | ♿ access | 📊 analytics | 🗑️ deprecate
3. Giữ tiêu đề dưới 72 ký tự
4. Sử dụng thể mệnh lệnh
5. Thêm 3-5 điểm chi tiết cụ thể

Ví dụ định dạng:
✨ thêm hệ thống xác thực người dùng
- Triển khai chức năng đăng nhập/đăng xuất với JWT tokens
- Thêm mã hóa mật khẩu bằng bcrypt với 12 rounds
- Tạo quản lý phiên người dùng với Redis storage
- Thêm xác thực email cho đăng ký mới
- Triển khai rate limiting trên endpoints xác thực
""",
            'descriptive': """
Tạo commit message mô tả chi tiết bằng tiếng Việt:
1. Viết tiêu đề rõ ràng, mô tả (không có tiền tố hay emoji)
2. Viết hoa chữ cái đầu, không có dấu chấm cuối
3. Giữ tiêu đề dưới 72 ký tự  
4. Sử dụng thể mệnh lệnh
5. Thêm 3-5 điểm chi tiết cụ thể
6. Tập trung vào cái gì và tại sao, không phải cách thực hiện

Ví dụ định dạng:
Thêm hệ thống xác thực người dùng toàn diện với các cải tiến bảo mật
- Triển khai chức năng đăng nhập và đăng xuất bảo mật sử dụng JWT tokens
- Bao gồm mã hóa mật khẩu với bcrypt sử dụng 12 rounds cho bảo mật
- Cung cấp quản lý phiên với Redis để mở rộng
- Thêm quy trình xác thực email cho đăng ký người dùng mới
- Triển khai rate limiting để ngăn chặn tấn công brute force
"""
        }
    }
    
    # Get the appropriate prompt template
    template = lang_instructions[commit_language][commit_style]
    
    return f"""{template}

Now analyze the following git diff and generate a commit message:

{diff_text}"""

def generate_commit_message(diff_text: str, api_key: str, model: str, commit_style: str, commit_language: str) -> str:
    """Generate commit message using Gemini AI with enhanced prompts."""
    try:
        if not api_key:
            print_error("❌ API key not configured. Run 'dev_tool settings' to set it up.")
            sys.exit(1)
            
        ai_model = init_ai(api_key, model)
        
        prompt = get_commit_prompt(commit_style, commit_language, diff_text)
        
        response = ai_model.generate_content(prompt)
        message = response.text.strip()
        
        # Post-process the message to ensure consistency
        message = format_commit_message(message, commit_style)
        
        return message
        
    except Exception as e:
        print_error(f"❌ Error generating commit message: {e}")
        print_error("💡 Please check your API key and internet connection.")
        sys.exit(1)

def format_commit_message(message: str, commit_style: str) -> str:
    """Format and clean up the commit message."""
    lines = message.strip().split('\n')
    if not lines:
        return message
    
    # Clean up any unwanted markdown or formatting
    cleaned_lines = []
    for line in lines:
        # Remove markdown formatting
        line = line.replace('**', '').replace('*', '').replace('`', '')
        # Remove extra spaces
        line = ' '.join(line.split())
        if line:  # Only add non-empty lines
            cleaned_lines.append(line)
    
    # Ensure the first line meets length requirements
    if cleaned_lines and len(cleaned_lines[0]) > 72:
        title = cleaned_lines[0]
        if ': ' in title:
            type_part, desc_part = title.split(': ', 1)
            if len(desc_part) > 50:  # Truncate description if too long
                cleaned_lines[0] = f"{type_part}: {desc_part[:47]}..."
        elif len(title) > 69:  # For emoji or descriptive style
            cleaned_lines[0] = title[:69] + "..."
    
    return '\n'.join(cleaned_lines)

def analyze_diff_complexity(diff_text: str) -> Dict:
    """Analyze the complexity and type of changes in the diff."""
    analysis = {
        'files_changed': 0,
        'lines_added': 0,
        'lines_removed': 0,
        'has_new_files': False,
        'has_deleted_files': False,
        'file_types': set(),
        'change_type': 'modification'
    }
    
    lines = diff_text.split('\n')
    current_file = None
    
    for line in lines:
        if line.startswith('diff --git'):
            analysis['files_changed'] += 1
            # Extract file path
            if 'a/' in line and 'b/' in line:
                file_path = line.split('b/')[-1]
                if '.' in file_path:
                    ext = file_path.split('.')[-1]
                    analysis['file_types'].add(ext)
        
        elif line.startswith('new file mode'):
            analysis['has_new_files'] = True
            analysis['change_type'] = 'addition'
            
        elif line.startswith('deleted file mode'):
            analysis['has_deleted_files'] = True
            analysis['change_type'] = 'deletion'
            
        elif line.startswith('+') and not line.startswith('+++'):
            analysis['lines_added'] += 1
            
        elif line.startswith('-') and not line.startswith('---'):
            analysis['lines_removed'] += 1
    
    # Determine overall change type
    if analysis['has_new_files'] and not analysis['has_deleted_files']:
        analysis['change_type'] = 'addition'
    elif analysis['has_deleted_files'] and not analysis['has_new_files']:
        analysis['change_type'] = 'deletion'
    elif analysis['lines_added'] > analysis['lines_removed'] * 2:
        analysis['change_type'] = 'major_addition'
    elif analysis['lines_removed'] > analysis['lines_added'] * 2:
        analysis['change_type'] = 'major_removal'
    else:
        analysis['change_type'] = 'modification'
    
    return analysis