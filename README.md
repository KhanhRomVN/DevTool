# Auto-Commit Tool

A command-line tool that automatically generates meaningful commit messages using Google's Gemini AI and handles git commits and pushes.

## Features

- Automatically generates commit messages based on staged changes
- Uses Google's Gemini 2.0 AI models for intelligent message generation
- Supports both commit and push operations
- Persistent configuration (only asks for API key once)
- Proper isolation using pipx

## Available Models

1. **Gemini 2.0 Flash**
   - Advanced features and speed
   - Real-time streaming capabilities
   - Recommended for most users

2. **Gemini 2.0 Flash-Lite**
   - Cost-effective option
   - Lower latency
   - Ideal for basic commit messages

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

The script will:
- Install pipx if not present
- Install the tool using pipx (with automatic virtual environment management)
- Add ~/.local/bin to PATH if needed

After installation:
1. Open a new terminal, or
2. Run: `source ~/.bashrc`

## First Run Setup

On first run, you'll be prompted once to:
1. Enter your Gemini API key
2. Choose your preferred model (Gemini 2.0 Flash or Flash-Lite)

This configuration will be saved and reused for future runs.

## Usage

Basic usage:
```bash
# Stage your changes first
git add .

# Generate commit message and push changes
auto-commit

# Generate commit message without pushing
auto-commit --no-push

# Reconfigure API key and model choice
auto-commit --reconfigure
```

## How It Works

The tool:
1. Checks for staged changes in git
2. Uses the configured Gemini model to analyze changes
3. Generates a meaningful commit message
4. Handles the commit and push operations

## Configuration

The tool stores its configuration in `~/.config/auto-commit/config.json`. This includes:
- Your Gemini API key
- Your chosen model preference

To change your configuration:
```bash
auto-commit --reconfigure
```

## Uninstallation

To remove the tool from your system:

```bash
chmod +x uninstall.sh
./uninstall.sh
```

This will:
- Uninstall the package using pipx
- Remove the configuration directory
- Clean up all tool files

## Security Note

Your API key is stored locally in the configuration file. Make sure to keep it secure and never share it with others.

## Troubleshooting

If you encounter any issues:
1. Make sure you've opened a new terminal or sourced ~/.bashrc after installation
2. Check if ~/.local/bin is in your PATH
3. Verify that your Gemini API key is valid
4. Ensure you're in a git repository when using the command

If you need to change your API key or model:
```bash
auto-commit --reconfigure
```

If the tool isn't found:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Why pipx?

We use pipx because:
- It's the recommended way to install Python applications on Ubuntu
- It automatically manages virtual environments
- It avoids conflicts with system Python packages
- It provides proper isolation for the tool

## License

MIT License - Feel free to modify and distribute this tool as needed.

sss