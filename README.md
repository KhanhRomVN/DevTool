# Auto-Commit Tool

A command-line tool that automatically generates meaningful commit messages using Google's Gemini AI and handles git commits and pushes. It also includes automatic code review capabilities.

## Features

- Automatically generates commit messages based on staged changes
- Performs AI-powered code review before committing
- Uses Google's Gemini 2.0 AI models
- Supports both English and Vietnamese
- Proper emoji formatting for commit types
- Runs in isolated virtual environment

## Code Review Features

The tool automatically performs code review before committing, analyzing:
- 🐛 Potential bugs and issues
- 💡 Code improvement suggestions
- 🔍 Code smells and anti-patterns
- 🔒 Security concerns

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
- Enter your Gemini API key
- Choose your preferred model
- Select language (English/Tiếng Việt)

## How It Works

1. Code Review:
   - Analyzes staged changes for potential issues
   - Provides detailed feedback in multiple categories
   - Asks for confirmation before proceeding

2. Commit Message Generation:
   - Uses Gemini AI to understand changes
   - Formats message with appropriate emoji
   - Follows conventional commit format

3. Git Operations:
   - Commits changes with generated message
   - Optionally pushes to remote repository

## Available Models

1. **Gemini 2.0 Flash**
   - Advanced features and capabilities
   - Faster response times
   - Better for complex code analysis
   - Higher API usage cost

2. **Gemini 2.0 Flash-Lite**
   - Basic analysis capabilities
   - Lower latency
   - More cost-effective
   - Suitable for simple changes

## Usage

Basic usage:
```bash
# Stage your changes
git add .

# Full process (code review + commit + push)
auto-commit

# Skip code review
auto-commit --no-review

# Generate commit message without pushing
auto-commit --no-push

# Change settings (API key, model, language)
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

## Language Support

The tool supports:
- English: Professional commit messages and code reviews
- Tiếng Việt: Commit messages in Vietnamese

## Configuration

Settings are stored in `~/.config/auto-commit/config.json`:
- Gemini API key
- Model preference
- Language selection

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
test