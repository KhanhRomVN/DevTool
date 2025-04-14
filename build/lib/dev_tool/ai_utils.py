#!/usr/bin/env python3
from typing import Dict, Optional
import google.generativeai as genai

from .messages import get_message, print_error, COLORS
from .git_utils import format_commit_message

def init_ai(config: Dict) -> genai.GenerativeModel:
    """Initialize the AI model with the given configuration."""
    genai.configure(api_key=config['api_key'])
    model_map = {
        'gemini-2.0-flash': 'gemini-2.0-flash',
        'gemini-2.0-flash-lite': 'gemini-2.0-flash-lite'
    }
    model_name = model_map.get(config['model'], 'gemini-2.0-flash')
    return genai.GenerativeModel(model_name)

def review_code(diff_text: str, config: Dict) -> Optional[str]:
    """Perform code review using Gemini AI."""
    try:
        model = init_ai(config)
        review_prompt = f"""
    Perform a thorough code review of the following changes.
    Focus on:
    1. Potential bugs or issues
    2. Code improvement suggestions
    3. Code smells or anti-patterns
    4. Security concerns
    
    Format your response in clear sections.
    Be specific but concise.
    If no issues are found in a category, say "No issues found."
    Do not use markdown formatting.
    Keep bullet points simple with just "-" prefix.
    
    Changes to review:
    {diff_text}
    """
        
        response = model.generate_content(review_prompt)
        review = response.text.strip()
        
        # Format the review with emojis and sections
        sections = {
            "🐛 Potential Bugs": [],
            "💡 Improvements": [],
            "🔍 Code Smells": [],
            "🔒 Security": []
        }
        
        current_section = None
        for line in review.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Try to match section headers
            lower_line = line.lower()
            if "bug" in lower_line or "issue" in lower_line:
                current_section = "🐛 Potential Bugs"
            elif "improve" in lower_line or "suggest" in lower_line:
                current_section = "💡 Improvements"
            elif "smell" in lower_line or "pattern" in lower_line:
                current_section = "🔍 Code Smells"
            elif "security" in lower_line or "vulnerab" in lower_line:
                current_section = "🔒 Security"
            elif current_section and line.startswith(("-", "*", "•")):
                # Clean up the line
                clean_line = line.lstrip("-*• ").strip()
                clean_line = clean_line.replace("**", "").replace("*", "").replace("`", "")
                sections[current_section].append(clean_line)
        
        # Format the final review
        formatted_review = f"\n{COLORS['BLUE']}{COLORS['BOLD']}📋 Code Review Results{COLORS['END']}\n"
        formatted_review += "=" * 50 + "\n\n"
        
        for section, items in sections.items():
            formatted_review += f"{COLORS['YELLOW']}{section}:{COLORS['END']}\n"
            if items:
                for item in items:
                    formatted_review += f"- {item}\n"
            else:
                formatted_review += f"{COLORS['GREEN']}✅ No issues found{COLORS['END']}\n"
            formatted_review += "\n"
        
        return formatted_review
    except Exception as e:
        print_error(get_message('review_error', config))
        print(e)
        return None

def generate_commit_message(diff_text: str, config: Dict) -> str:
    """Generate commit message using Gemini AI."""
    try:
        model = init_ai(config)
        prompt = f"""
    Analyze the following git diff and generate a structured commit message.
    Generate the message in {'Vietnamese' if config['commit_language'] == 'vi' else 'English'}.
    
    Rules:
    1. Start with a type (one of: feat, fix, docs, style, refactor, perf, test, chore, ci, build, revert)
    2. Follow with a concise title
    3. Add 2-3 bullet points describing specific changes
    4. Do not use any markdown formatting (no backticks, no code blocks)
    5. Keep descriptions plain and simple
    
    Format:
    type: Title of the change
    - Change detail 1 (plain text, no formatting)
    - Change detail 2 (plain text, no formatting)
    
    Git diff:
    {diff_text}
    """
        
        response = model.generate_content(prompt)
        message = response.text.strip()
        return format_commit_message(message)
    except Exception as e:
        print_error(get_message('git_error', config))
        print(e)
        sys.exit(1)