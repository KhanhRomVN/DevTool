# build.py
#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
from pathlib import Path

def build_exe():
    """Build standalone executable using PyInstaller"""
    try:
        # Install PyInstaller if not available
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        
        # Create build directory
        build_dir = Path("build")
        dist_dir = Path("dist")
        
        # Clean previous builds
        if build_dir.exists():
            shutil.rmtree(build_dir)
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
        
        # Build with PyInstaller
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--name=dev_tool",
            "--onefile",
            "--console",
            "--add-data=dev_tool;dev_tool",
            "--hidden-import=google.generativeai",
            "--hidden-import=colorama",
            "dev_tool/cli.py"
        ]
        
        subprocess.check_call(cmd)
        print("✅ Build completed successfully!")
        print(f"📦 Executable location: {dist_dir/'dev_tool.exe'}")
        
    except Exception as e:
        print(f"❌ Build failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    build_exe()