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

The installation script will automatically install other required dependencies (pipx).

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
- Choose your preferred model (Flash or Flash-Lite)
- Select language (English/Tiếng Việt)

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

## Code Review Process

When you run `auto-commit`, the tool will:
1. Analyze your staged changes
2. Provide a detailed code review with:
   - Potential bugs detection
   - Code improvement suggestions
   - Code smell identification
   - Security concern checks
3. Ask if you want to proceed with the commit
4. Generate and apply the commit message if you proceed

To skip the code review:
```bash
auto-commit --no-review
```

## Commit Message Format

Messages are formatted with emojis based on type:
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

The tool stores its configuration in `~/.config/auto-commit/config.json`. This includes:
- Your Gemini API key
- Your chosen model preference
- Language preference (English/Vietnamese)

## Language Support

The tool supports:
- English: Professional commit messages and code reviews
- Tiếng Việt: Commit messages in Vietnamese

## Uninstallation

To remove the tool from your system:

```bash
chmod +x uninstall.sh
./uninstall.sh
```

This will:
- Remove the auto-commit command
- Delete the virtual environment
- Remove all tool files and configurations

## Security Note

Your API key is stored locally in the configuration file. Make sure to keep it secure and never share it with others.

## Troubleshooting

If you encounter any issues:
1. Make sure you've opened a new terminal or sourced ~/.bashrc after installation
2. Check if ~/.local/bin is in your PATH
3. Verify that your Gemini API key is valid
4. Ensure you're in a git repository when using the command

## License

MIT License - Feel free to modify and distribute this tool as needed.