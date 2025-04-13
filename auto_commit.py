#!/bin/bash

# Get the user's home directory reliably
USER_HOME="$HOME"
VENV_PATH="$USER_HOME/.local/share/auto-commit/venv"

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "Error: Virtual environment not found. Please reinstall the tool."
    exit 1
fi

# Activate virtual environment and run embedded Python script
source "$VENV_PATH/bin/activate"

python3 - "$@" << 'END_PYTHON'
#!/usr/bin/env python3
import os
import sys
import json
from pathlib import Path
import subprocess
import argparse
import google.generativeai as genai

CONFIG_PATH = os.path.expanduser("~/.config/auto-commit/config.json")

def load_config():
    """Load configuration from the config file."""
    if not os.path.exists(CONFIG_PATH):
        print("Error: Configuration not found. Please run install.sh first.")
        sys.exit(1)
    
    with open(CONFIG_PATH) as f:
        return json.load(f)

def get_git_diff():
    """Get the git diff of staged changes."""
    try:
        return subprocess.check_output(['git', 'diff', '--cached']).decode('utf-8')
    except subprocess.CalledProcessError:
        print("Error: Failed to get git diff. Are you in a git repository?")
        sys.exit(1)

def generate_commit_message(diff_text, config):
    """Generate commit message using Gemini AI."""
    genai.configure(api_key=config['api_key'])
    
    model_map = {
        'gemini-2.0-flash': 'gemini-2.0-flash',
        'gemini-2.0-flash-lite': 'gemini-2.0-flash-lite'
    }
    
    model_name = model_map.get(config['model'], 'gemini-2.0-flash')
    model = genai.GenerativeModel(model_name)
    
    prompt = f"""
    Based on the following git diff, generate a clear and concise commit message.
    The message should follow conventional commit format.
    Focus on the main changes and their purpose.
    Keep it brief but descriptive.
    
    Git diff:
    {diff_text}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating commit message: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Auto-generate commit messages and push changes')
    parser.add_argument('--no-push', action='store_true', help='Generate commit message without pushing')
    args = parser.parse_args()

    config = load_config()
    diff = get_git_diff()
    
    if not diff:
        print("No staged changes found. Use 'git add' to stage your changes.")
        sys.exit(1)
    
    commit_message = generate_commit_message(diff, config)
    print(f"\nGenerated commit message:\n{commit_message}\n")
    
    try:
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print("Changes committed successfully!")
        
        if not args.no_push:
            subprocess.run(['git', 'push'], check=True)
            print("Changes pushed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during git operations: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
END_PYTHON
