# run.py
#!/usr/bin/env python3
import os
import sys
from pathlib import Path

def run_direct():
    """Run the tool directly using the virtual environment"""
    venv_dir = Path("venv")
    
    if not venv_dir.exists():
        print("❌ Virtual environment not found. Run setup_venv.py first.")
        return False
    
    # Add virtual environment to path
    if os.name == "nt":
        python_path = venv_dir / "Scripts" / "python.exe"
    else:
        python_path = venv_dir / "bin" / "python"
    
    # Run the tool
    os.execl(str(python_path), str(python_path), "-m", "dev_tool", *sys.argv[1:])

if __name__ == "__main__":
    run_direct()