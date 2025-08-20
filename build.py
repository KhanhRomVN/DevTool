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

def update_version(new_version):
    """Update version in all relevant files"""
    # Update __init__.py
    init_file = Path(__file__).parent / "dev_tool" / "__init__.py"
    if init_file.exists():
        content = init_file.read_text()
        current_version = get_version()
        content = content.replace(f'__version__ = "{current_version}"', f'__version__ = "{new_version}"')
        init_file.write_text(content)
    
    # Update setup.py
    setup_file = Path(__file__).parent / "setup.py"
    if setup_file.exists():
        content = setup_file.read_text()
        # Look for version= pattern
        import re
        content = re.sub(r'version="[^"]*"', f'version="{new_version}"', content)
        setup_file.write_text(content)

def build_windows_exe(version):
    """Build Windows executable"""
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
        
        # Build with PyInstaller - Fixed syntax
        dev_tool_dir = base_dir / "dev_tool"
        
        # Use proper separator for current OS
        separator = ";" if platform.system().lower() == "windows" else ":"
        
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--name=dev_tool",
            "--onefile",
            "--console",
            f"--add-data={dev_tool_dir}{separator}dev_tool",
            "--hidden-import=google.generativeai",
            "--hidden-import=colorama",
            "--collect-all=google.generativeai",
            "--collect-all=colorama",
            str(dev_tool_dir / "cli.py")
        ]
        
        print("🔨 Building executable...")
        subprocess.check_call(cmd, cwd=base_dir)
        
        # Rename with version
        exe_name = "dev_tool.exe" if platform.system().lower() == "windows" else "dev_tool"
        original_exe = dist_dir / exe_name
        
        platform_name = platform.system().lower()
        arch = platform.machine().lower()
        if arch == "x86_64":
            arch = "amd64"
        elif arch in ["aarch64", "arm64"]:
            arch = "arm64"
        
        new_name = f"dev_tool_v{version}_{platform_name}_{arch}"
        if platform.system().lower() == "windows":
            new_name += ".exe"
        
        versioned_exe = dist_dir / new_name
        
        if original_exe.exists():
            shutil.move(str(original_exe), str(versioned_exe))
            print(f"✅ Executable built: {versioned_exe}")
            return versioned_exe
        return None
        
    except Exception as e:
        print(f"❌ Build failed: {e}")
        return None

def build_windows_msi(version, exe_path):
    """Build Windows MSI installer"""
    try:
        # Check if WiX Toolset is available
        if not shutil.which("candle") or not shutil.which("light"):
            print("⚠️  WiX Toolset not found. Skipping MSI build.")
            print("   Install from: https://wixtoolset.org/")
            return None
            
        base_dir = Path(__file__).parent
        wix_dir = base_dir / "wix"
        wix_dir.mkdir(exist_ok=True)
        
        # Create WXS file
        wxs_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
    <Product Id="*" Name="Dev Tool" Language="1033" Version="{version}" 
             Manufacturer="Dev Tool Team" UpgradeCode="a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8">
        <Package InstallerVersion="200" Compressed="yes" Comments="Windows Installer Package"/>
        <Media Id="1" Cabinet="media1.cab" EmbedCab="yes"/>
        <Directory Id="TARGETDIR" Name="SourceDir">
            <Directory Id="ProgramFilesFolder">
                <Directory Id="INSTALLDIR" Name="Dev Tool">
                    <Component Id="MainExecutable" Guid="a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n9">
                        <File Id="dev_tool.exe" Source="{exe_path}" KeyPath="yes"/>
                        <Environment Id="PATH" Name="PATH" Value="[INSTALLDIR]" Permanent="no" Part="last" Action="set" System="yes"/>
                    </Component>
                </Directory>
            </Directory>
        </Directory>
        <Feature Id="Complete" Title="Dev Tool" Level="1">
            <ComponentRef Id="MainExecutable"/>
        </Feature>
    </Product>
</Wix>'''
        
        wxs_file = wix_dir / "dev_tool.wxs"
        with open(wxs_file, "w") as f:
            f.write(wxs_content)
        
        # Build MSI
        print("🔨 Building Windows MSI installer...")
        subprocess.check_call([
            "candle", str(wxs_file), "-o", str(wix_dir / "dev_tool.wixobj")
        ], cwd=wix_dir)
        
        subprocess.check_call([
            "light", str(wix_dir / "dev_tool.wixobj"), "-o", 
            str(base_dir / "dist" / f"dev_tool_v{version}_windows.msi")
        ], cwd=wix_dir)
        
        msi_path = base_dir / "dist" / f"dev_tool_v{version}_windows.msi"
        if msi_path.exists():
            print(f"✅ Windows MSI built: {msi_path}")
            return msi_path
        return None
        
    except Exception as e:
        print(f"❌ MSI build failed: {e}")
        return None

def build_linux_snap(version):
    """Build Linux Snap package with all dependencies included"""
    try:
        if not shutil.which("snapcraft"):
            print("⚠️  Snapcraft not found. Skipping Snap build.")
            print("   Install with: sudo snap install snapcraft --classic")
            return None
            
        base_dir = Path(__file__).parent
        
        # Create snapcraft.yaml in snap directory
        snap_dir = base_dir / "snap"
        snap_dir.mkdir(exist_ok=True)
        
        snapcraft_content = f'''name: dev-tool
version: '{version}'
summary: AI-powered Git commit message generator
description: |
  Dev Tool is an AI-powered assistant that generates meaningful
  commit messages based on your code changes using Google's Gemini AI.

grade: stable
confinement: classic
base: core20

apps:
  dev-tool:
    command: bin/dev_tool
    plugs: [home, network, network-bind]

parts:
  dev-tool:
    plugin: dump
    source: .
    organize:
      dev_tool: bin/dev_tool
    stage-packages:
      - python3
      - python3-pip
    override-build: |
      set -e
      mkdir -p $SNAPCRAFT_PART_INSTALL/bin
      mkdir -p $SNAPCRAFT_PART_INSTALL/lib/python3.8/site-packages
      
      # Install all Python dependencies
      pip3 install --target=$SNAPCRAFT_PART_INSTALL/lib/python3.8/site-packages \\
        google-generativeai>=0.3.0 \\
        colorama>=0.4.0
      
      # Copy the dev_tool package
      cp -r dev_tool $SNAPCRAFT_PART_INSTALL/lib/python3.8/site-packages/
      
      # Create the executable wrapper
      cat > $SNAPCRAFT_PART_INSTALL/bin/dev_tool << 'EOF'
#!/bin/bash
export PYTHONPATH=$SNAPCRAFT_PART_INSTALL/lib/python3.8/site-packages:$PYTHONPATH
python3 $SNAPCRAFT_PART_INSTALL/lib/python3.8/site-packages/dev_tool/cli.py "$@"
EOF
      chmod +x $SNAPCRAFT_PART_INSTALL/bin/dev_tool
'''
        
        with open(snap_dir / "snapcraft.yaml", "w") as f:
            f.write(snapcraft_content)
        
        # Build Snap
        print("🔨 Building Linux Snap package...")
        subprocess.check_call(["snapcraft"], cwd=base_dir)
        
        # Move to dist directory
        snap_files = list(base_dir.glob("*.snap"))
        if snap_files:
            snap_path = snap_files[0]
            dist_snap = base_dir / "dist" / f"dev-tool_{version}.snap"
            shutil.move(str(snap_path), str(dist_snap))
            print(f"✅ Linux Snap package built: {dist_snap}")
            return dist_snap
        return None
        
    except Exception as e:
        print(f"❌ Snap build failed: {e}")
        return None

def build_python_wheel(version):
    """Build Python wheel package"""
    try:
        base_dir = Path(__file__).parent
        
        print("🔨 Building Python wheel...")
        subprocess.check_call([sys.executable, "setup.py", "bdist_wheel"], cwd=base_dir)
        
        # Find the wheel file
        wheel_dir = base_dir / "dist"
        wheel_files = list(wheel_dir.glob("*.whl"))
        
        if wheel_files:
            wheel_path = wheel_files[-1]  # Get the most recent one
            print(f"✅ Python wheel built: {wheel_path}")
            return wheel_path
        return None
        
    except Exception as e:
        print(f"❌ Wheel build failed: {e}")
        return None

def create_release_info(version, artifacts):
    """Create release information file"""
    base_dir = Path(__file__).parent
    dist_dir = base_dir / "dist"
    
    release_info = f"""# Dev Tool v{version} Release

## Installation Instructions

### Binary Executables
"""
    
    for artifact in artifacts:
        if artifact and artifact.exists():
            name = artifact.name
            size = artifact.stat().st_size
            size_mb = size / (1024 * 1024)
            
            if name.endswith('.exe'):
                release_info += f"\n### Windows Executable\n- File: `{name}`\n- Size: {size_mb:.1f} MB\n- Install: Download and run\n"
            elif name.endswith('.deb'):
                release_info += f"\n### Ubuntu/Debian Package\n- File: `{name}`\n- Size: {size_mb:.1f} MB\n- Install: `sudo dpkg -i {name}`\n"
            elif name.endswith('.snap'):
                release_info += f"\n### Snap Package\n- File: `{name}`\n- Size: {size_mb:.1f} MB\n- Install: `sudo snap install {name} --dangerous`\n"
            elif name.endswith('.whl'):
                release_info += f"\n### Python Wheel\n- File: `{name}`\n- Size: {size_mb:.1f} MB\n- Install: `pip install {name}`\n"
            elif name.endswith('.msi'):
                release_info += f"\n### Windows Installer\n- File: `{name}`\n- Size: {size_mb:.1f} MB\n- Install: Double-click to install\n"
    
    release_info += """
### From Source
```bash
git clone https://github.com/your-repo/dev_tool
cd dev_tool
pip install -e .