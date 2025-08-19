# build.py
#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
import platform
import argparse
from pathlib import Path

def get_version():
    """Read version from __init__.py"""
    init_file = Path(__file__).parent / "dev_tool" / "__init__.py"
    version = "2.0.0"  # default
    
    if init_file.exists():
        with open(init_file, "r") as f:
            for line in f:
                if line.startswith("__version__"):
                    version = line.split('"')[1]
                    break
    return version

def build_windows_exe(version):
    """Build Windows executable (only works on Windows)"""
    if platform.system().lower() != "windows":
        print("⚠️  Windows EXE can only be built on Windows platform")
        print("💡 Use GitHub Actions or Docker for cross-compilation")
        return None
        
    try:
        # Install PyInstaller if not available
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        
        base_dir = Path(__file__).parent
        build_dir = base_dir / "build"
        dist_dir = base_dir / "dist"
        
        # Create dist directory
        dist_dir.mkdir(exist_ok=True)
        
        # Clean previous builds
        if build_dir.exists():
            shutil.rmtree(build_dir)
        
        # Build with PyInstaller
        dev_tool_dir = base_dir / "dev_tool"
        
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--name=dev_tool",
            "--onefile",
            "--console",
            f"--add-data={dev_tool_dir};dev_tool",
            "--hidden-import=google.generativeai",
            "--hidden-import=colorama",
            # Add Windows specific optimizations
            "--noupx",
            "--clean",
            str(dev_tool_dir / "cli.py")
        ]
        
        # Add icon if exists
        icon_path = base_dir / "icon.ico"
        if icon_path.exists():
            cmd.append(f"--icon={icon_path}")
        
        print("🔨 Building Windows executable...")
        subprocess.check_call(cmd, cwd=base_dir)
        
        # Rename with version
        original_exe = dist_dir / "dev_tool.exe"
        versioned_exe = dist_dir / f"dev_tool_v{version}_windows_amd64.exe"
        
        if original_exe.exists():
            shutil.move(str(original_exe), str(versioned_exe))
            print(f"✅ Windows EXE built: {versioned_exe}")
            return versioned_exe
        return None
        
    except Exception as e:
        print(f"❌ Windows EXE build failed: {e}")
        return None

def build_linux_snap(version):
    """Build Linux Snap package"""
    if platform.system().lower() != "linux":
        print("⚠️  Snap packages can only be built on Linux")
        return None
        
    try:
        # Check if snapcraft is available
        if not shutil.which("snapcraft"):
            print("❌ Snapcraft not found. Installing...")
            try:
                subprocess.check_call(["sudo", "snap", "install", "snapcraft", "--classic"])
            except subprocess.CalledProcessError:
                print("❌ Failed to install snapcraft. Please install manually:")
                print("   sudo snap install snapcraft --classic")
                return None
        
        base_dir = Path(__file__).parent
        snap_dir = base_dir / "snap"
        snap_dir.mkdir(exist_ok=True)
        
        # Create optimized snapcraft.yaml
        snapcraft_content = f'''name: dev-tool
base: core22
version: '{version}'
summary: AI-powered Git commit message generator
description: |
  Dev Tool is an AI-powered assistant that generates meaningful
  commit messages based on your code changes using Google's Gemini AI.
  
  Features:
  - Smart commit message generation
  - Multi-language support (English/Vietnamese)
  - Multiple commit styles (Conventional/Emoji/Descriptive)
  - Cross-platform compatibility

grade: stable
confinement: strict

apps:
  dev-tool:
    command: bin/dev_tool
    plugs: 
      - home
      - network
      - network-bind
      - removable-media
    environment:
      LC_ALL: C.UTF-8
      LANG: C.UTF-8

parts:
  dev-tool:
    plugin: python
    source: .
    python-requirements:
      - requirements.txt
    stage-packages:
      - git
    override-build: |
      craftctl default
      # Create wrapper script
      mkdir -p $CRAFTCTL_PART_INSTALL/bin
      cat > $CRAFTCTL_PART_INSTALL/bin/dev_tool << 'EOF'
#!/bin/bash
export PYTHONPATH="$SNAP/lib/python3.10/site-packages:$PYTHONPATH"
cd "$HOME" || cd /tmp
exec "$SNAP/bin/python3" -m dev_tool.cli "$@"
EOF
      chmod +x $CRAFTCTL_PART_INSTALL/bin/dev_tool
'''
        
        snapcraft_file = snap_dir / "snapcraft.yaml"
        with open(snapcraft_file, "w") as f:
            f.write(snapcraft_content)
        
        # Build Snap
        print("🔨 Building Linux Snap package...")
        subprocess.check_call(["snapcraft", "--verbose"], cwd=base_dir)
        
        # Find and rename snap file
        snap_files = list(base_dir.glob("*.snap"))
        if snap_files:
            snap_path = snap_files[0]
            dist_dir = base_dir / "dist" 
            dist_dir.mkdir(exist_ok=True)
            
            new_name = f"dev-tool_v{version}_linux_amd64.snap"
            final_snap = dist_dir / new_name
            
            shutil.move(str(snap_path), str(final_snap))
            print(f"✅ Linux Snap built: {final_snap}")
            return final_snap
        return None
        
    except Exception as e:
        print(f"❌ Snap build failed: {e}")
        print("💡 Make sure you have snapcraft installed: sudo snap install snapcraft --classic")
        return None

def create_github_actions_workflow(version):
    """Create GitHub Actions workflow for cross-platform builds"""
    base_dir = Path(__file__).parent
    github_dir = base_dir / ".github" / "workflows"
    github_dir.mkdir(parents=True, exist_ok=True)
    
    workflow_content = f'''name: Build Cross-Platform Packages

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to build'
        required: true
        default: '{version}'

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pyinstaller
          
      - name: Build Windows EXE
        run: python build.py --platform windows
        
      - name: Upload Windows artifacts
        uses: actions/upload-artifact@v3
        with:
          name: windows-exe
          path: dist/*.exe

  build-linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          
      - name: Install Snapcraft
        run: |
          sudo snap install snapcraft --classic
          sudo snap install multipass
          
      - name: Build Linux Snap
        run: python build.py --platform linux
        
      - name: Upload Linux artifacts
        uses: actions/upload-artifact@v3
        with:
          name: linux-snap
          path: dist/*.snap

  create-release:
    needs: [build-windows, build-linux]
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/')
    
    steps:
      - name: Download all artifacts
        uses: actions/download-artifact@v3
        
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            windows-exe/*
            linux-snap/*
          generate_release_notes: true
        env:
          GITHUB_TOKEN: ${{{{ secrets.GITHUB_TOKEN }}}}
'''
    
    workflow_file = github_dir / "build.yml"
    with open(workflow_file, "w") as f:
        f.write(workflow_content)
    
    print(f"✅ GitHub Actions workflow created: {workflow_file}")
    print("💡 Push to GitHub with tags to trigger cross-platform builds")
    return workflow_file

def build_python_wheel(version):
    """Build Python wheel package"""
    try:
        base_dir = Path(__file__).parent
        
        # Ensure setup.py exists
        setup_file = base_dir / "setup.py"
        if not setup_file.exists():
            print("❌ setup.py not found in root directory")
            return None
        
        print("🔨 Building Python wheel...")
        subprocess.check_call([sys.executable, "setup.py", "bdist_wheel"], cwd=base_dir)
        
        # Find the wheel file
        wheel_dir = base_dir / "dist"
        wheel_files = list(wheel_dir.glob("*.whl"))
        
        if wheel_files:
            wheel_path = wheel_files[-1]
            print(f"✅ Python wheel built: {wheel_path}")
            return wheel_path
        return None
        
    except Exception as e:
        print(f"❌ Wheel build failed: {e}")
        return None

def show_cross_platform_help():
    """Show help for cross-platform building"""
    current_platform = platform.system().lower()
    
    print(f"""
🌍 Cross-Platform Build Guide
============================

Current platform: {current_platform.title()}

Available builds:
{"✅ Windows EXE" if current_platform == "windows" else "❌ Windows EXE (requires Windows)"}
{"✅ Linux Snap" if current_platform == "linux" else "❌ Linux Snap (requires Linux)"}
✅ Python Wheel (any platform)

🚀 Recommended approaches:

1️⃣  GitHub Actions (Automatic):
   - Push code to GitHub
   - Create workflow: python build.py --create-workflow
   - Tag release: git tag v2.0.0 && git push --tags

2️⃣  Docker (Manual cross-compilation):
   - Install Docker
   - Run: python build.py --docker

3️⃣  Platform-specific VMs:
   - Windows VM for .exe
   - Linux VM for .snap

4️⃣  Python wheel (universal):
   - Works on all platforms
   - Users install with: pip install dev_tool-2.0.0-py3-none-any.whl
    """)

def main():
    """Main build function"""
    parser = argparse.ArgumentParser(
        description="Build Dev Tool packages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python build.py --platform windows    # Build Windows EXE (Windows only)
  python build.py --platform linux      # Build Linux Snap (Linux only)
  python build.py --platform python     # Build Python wheel (any platform)
  python build.py --create-workflow     # Create GitHub Actions workflow
  python build.py --help-cross          # Show cross-platform help
        """
    )
    
    parser.add_argument("--platform", choices=["windows", "linux", "python"], 
                       help="Target platform to build for")
    parser.add_argument("--version", help="Set version (optional)")
    parser.add_argument("--create-workflow", action="store_true", 
                       help="Create GitHub Actions workflow")
    parser.add_argument("--help-cross", action="store_true",
                       help="Show cross-platform build help")
    
    args = parser.parse_args()
    
    if args.help_cross:
        show_cross_platform_help()
        return
    
    current_version = get_version()
    
    # Handle version update
    if args.version:
        current_version = args.version
        print(f"✅ Version set to: {current_version}")
    else:
        print(f"📦 Current version: {current_version}")
        new_version = input("🆕 Enter new version (or press Enter to keep current): ").strip()
        if new_version:
            current_version = new_version
            print(f"✅ Version updated to: {current_version}")
    
    # Create GitHub Actions workflow
    if args.create_workflow:
        create_github_actions_workflow(current_version)
        return
    
    # Auto-detect platform if not specified
    if not args.platform:
        current_os = platform.system().lower()
        if current_os == "windows":
            args.platform = "windows"
        elif current_os == "linux":
            args.platform = "linux"
        else:
            args.platform = "python"
        print(f"🎯 Auto-detected platform: {args.platform}")
    
    # Create dist directory
    dist_dir = Path(__file__).parent / "dist"
    dist_dir.mkdir(exist_ok=True)
    
    artifacts = []
    
    # Build for specified platform
    if args.platform == "windows":
        exe_path = build_windows_exe(current_version)
        if exe_path:
            artifacts.append(exe_path)
    
    elif args.platform == "linux":
        snap_path = build_linux_snap(current_version)
        if snap_path:
            artifacts.append(snap_path)
    
    elif args.platform == "python":
        wheel_path = build_python_wheel(current_version)
        if wheel_path:
            artifacts.append(wheel_path)
    
    # Show results
    print(f"\n🎉 Build process completed!")
    print(f"📁 Build artifacts in: {dist_dir}")
    
    if artifacts:
        print(f"✅ Successfully built:")
        for artifact in artifacts:
            print(f"   📦 {artifact.name}")
            
        # Show usage instructions
        print(f"\n📋 Usage Instructions:")
        if args.platform == "windows":
            print(f"   Windows: Double-click {artifacts[0].name}")
        elif args.platform == "linux":
            print(f"   Linux: sudo snap install {artifacts[0].name} --dangerous")
        elif args.platform == "python":
            print(f"   Any OS: pip install {artifacts[0].name}")
    else:
        print("⚠️  No packages were successfully built.")
        print("💡 Run with --help-cross for cross-platform options")

if __name__ == "__main__":
    main()