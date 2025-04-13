# Auto-Commit Tool

A command-line tool that automatically generates meaningful commit messages using Google's Gemini AI and handles git commits and pushes. It also includes automatic code review capabilities.

## Features

- Beautiful terminal interface with colors and formatting
- Dual language support (English/Tiếng Việt) for:
  * Terminal interface
  * Commit messages
- AI-powered code review
- Automatic commit message generation
- Proper emoji formatting for commit types
- Runs in isolated virtual environment

## Interface Languages

The tool supports two separate language settings:

1. **Terminal Interface Language**
   - English: All prompts and messages in English
   - Tiếng Việt: All prompts and messages in Vietnamese
   - Selected during installation
   - Can be changed with --reconfigure

2. **Commit Message Language**
   - English: Professional commit messages
   - Tiếng Việt: Commit messages in Vietnamese
   - Independent from interface language
   - Can be different from interface language

## Prerequisites

- Python 3.x
- Git
- A Gemini API key (get it from [Google AI Studio](https://makersuite.google.com/app/apikey))

## Installation

1. Clone or download this repository
2. Navigate to the tool directory
3. Run the installation script:

```bash
chmod +x install.sh
./install.sh
```

During installation, you'll be prompted to:
1. Choose interface language (English/Tiếng Việt)
2. Enter your Gemini API key
3. Choose your preferred model
4. Select commit message language

## Code Review Features

The tool performs automatic code review with beautiful formatting:
- 🐛 Potential bugs and issues
- 💡 Code improvement suggestions
- 🔍 Code smells and anti-patterns
- 🔒 Security concerns

## Usage

Basic usage:
```bash
# Full process (code review + commit + push)
auto-commit

# Skip code review
auto-commit --no-review

# Generate commit message without pushing
auto-commit --no-push

# Change settings (languages, API key, model)
auto-commit --reconfigure
```

## Commit Message Format

Messages are formatted with emojis based on type. Examples:

```
✨ feat: Add user authentication
- Implement JWT token validation
- Add login endpoints
```

```
🐛 fix: Resolve memory leak in worker pool
- Fix resource cleanup in worker threads
- Add proper error handling
```

Available types:
- ✨ feat: New features
- 🐛 fix: Bug fixes
- 📚 docs: Documentation
- 💎 style: Code style
- ♻️ refactor: Code refactoring
- ⚡️ perf: Performance
- 🧪 test: Testing
- 🔧 chore: Maintenance
- 👷 ci: CI/CD
- 📦 build: Build
- ⏪ revert: Reverts

## Configuration

Settings are stored in `~/.config/auto-commit/config.json`:
- Gemini API key
- Model preference
- Interface language
- Commit message language

## Uninstallation

To remove the tool:
```bash
./uninstall.sh
```

## Security Note

Your API key is stored locally in the configuration file. Keep it secure and never share it.

## Troubleshooting

If you encounter issues:
1. Check terminal PATH after installation
2. Verify Gemini API key
3. Ensure git repository is initialized
4. Check virtual environment activation

## License

MIT License - Feel free to modify and distribute this tool as needed.