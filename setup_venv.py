# setup_venv.py
#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

def setup_virtual_env():
    """Setup a portable virtual environment"""
    venv_dir = Path("venv")
    
    # Create virtual environment
    subprocess.check_call([sys.executable, "-m", "venv", str(venv_dir)])
    
    # Install dependencies
    pip_path = venv_dir / "Scripts" / "pip.exe" if os.name == "nt" else venv_dir / "bin" / "pip"
    subprocess.check_call([str(pip_path), "install", "-r", "requirements.txt"])
    
    print("✅ Virtual environment setup complete!")
    print("🔧 Activate with:")
    if os.name == "nt":
        print("    venv\\Scripts\\activate")
    else:
        print("    source venv/bin/activate")

if __name__ == "__main__":
    setup_virtual_env()