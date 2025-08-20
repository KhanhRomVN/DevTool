# PowerShell script to install dev_tool on Windows
# Run this in PowerShell: iex (Invoke-WebRequest -Uri "https://raw.githubusercontent.com/KhanhRomVN/dev_tool/main/install.ps1" -UseBasicParsing).Content

$ErrorActionPreference = "Stop"

# Tool information
$TOOL_NAME = "dev_tool"
$VERSION = "2.0.2"
$REPO_URL = "https://github.com/KhanhRomVN/dev_tool"

function Write-ColorOutput($ForegroundColor) {
    if ($args) {
        Write-Host $args -ForegroundColor $ForegroundColor
    } else {
        $input | Write-Host -ForegroundColor $ForegroundColor
    }
}

function Print-Header {
    Write-ColorOutput Cyan @"
==================================================
           🛠️  DEV TOOL 2.0 INSTALLER           
        AI-Powered Git Assistant Setup          
==================================================
"@
}

function Print-Success($message) {
    Write-ColorOutput Green "✅ $message"
}

function Print-Info($message) {
    Write-ColorOutput Blue "ℹ️  $message"
}

function Print-Warning($message) {
    Write-ColorOutput Yellow "⚠️  $message"
}

function Print-Error($message) {
    Write-ColorOutput Red "❌ $message"
}

function Test-GoInstalled {
    try {
        $goVersion = go version 2>$null
        if ($goVersion) {
            Print-Success "Go found: $goVersion"
            return $true
        }
    } catch {
        Print-Warning "Go is not installed or not in PATH"
        return $false
    }
    return $false
}

function Install-GoFromWeb {
    Print-Info "Downloading and installing Go..."
    
    $goVersion = "1.21.5"
    $goInstaller = "go$goVersion.windows-amd64.msi"
    $downloadUrl = "https://golang.org/dl/$goInstaller"
    $tempPath = Join-Path $env:TEMP $goInstaller
    
    try {
        Print-Info "Downloading Go installer..."
        Invoke-WebRequest -Uri $downloadUrl -OutFile $tempPath -UseBasicParsing
        
        Print-Info "Running Go installer..."
        Start-Process -FilePath $tempPath -Wait -ArgumentList "/quiet"
        
        # Refresh environment variables
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
        
        # Clean up
        Remove-Item $tempPath -Force
        
        # Verify installation
        if (Test-GoInstalled) {
            Print-Success "Go installed successfully"
            return $true
        } else {
            Print-Warning "Go installation may require restarting PowerShell"
            return $false
        }
    } catch {
        Print-Error "Failed to install Go: $_"
        return $false
    }
}

function Install-DevTool {
    Print-Info "Installing $TOOL_NAME..."
    
    # Check if Go is available
    if (-not (Test-GoInstalled)) {
        Print-Info "Go is required to install $TOOL_NAME"
        $installGo = Read-Host "Install Go automatically? (y/N)"
        
        if ($installGo -eq "y" -or $installGo -eq "Y") {
            if (-not (Install-GoFromWeb)) {
                Print-Error "Failed to install Go"
                Print-Info "Please install Go manually from https://golang.org/dl/ and try again"
                exit 1
            }
        } else {
            Print-Info "Please install Go manually from https://golang.org/dl/ and try again"
            exit 1
        }
    }
    
    try {
        Print-Info "Installing $TOOL_NAME from source..."
        & go install github.com/KhanhRomVN/dev_tool@latest
        
        # Check if installation was successful
        $goPath = & go env GOPATH 2>$null
        $devToolPath = Join-Path $goPath "bin\dev_tool.exe"
        
        if (Test-Path $devToolPath) {
            Print-Success "$TOOL_NAME installed successfully!"
            
            # Add GOPATH/bin to PATH if not already there
            $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
            $goBinPath = Join-Path $goPath "bin"
            
            if ($currentPath -notlike "*$goBinPath*") {
                Print-Info "Adding Go bin directory to PATH..."
                $newPath = "$currentPath;$goBinPath"
                [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
                $env:PATH += ";$goBinPath"
                Print-Success "Added $goBinPath to PATH"
            }
            
            Print-Info "Installation location: $devToolPath"
            return $true
        } else {
            Print-Error "Installation failed - binary not found"
            return $false
        }
    } catch {
        Print-Error "Failed to install $TOOL_NAME: $_"
        return $false
    }
}

function Test-Installation {
    try {
        $version = & dev_tool --version 2>$null
        if ($version) {
            Print-Success "✅ $TOOL_NAME is working correctly!"
            Print-Info "Version: $version"
            return $true
        }
    } catch {
        Print-Warning "Tool installed but not accessible. You may need to restart PowerShell."
        return $false
    }
    return $false
}

# Main execution
Print-Header

# Check if already installed
try {
    $currentVersion = & dev_tool --version 2>$null
    if ($currentVersion) {
        Print-Info "dev_tool is already installed: $currentVersion"
        $reinstall = Read-Host "Reinstall? (y/N)"
        if ($reinstall -ne "y" -and $reinstall -ne "Y") {
            Print-Info "Installation cancelled"
            exit 0
        }
    }
} catch {
    Print-Info "dev_tool is not currently installed"
}

# Install the tool
if (Install-DevTool) {
    Print-Success "🎉 Installation completed successfully!"
    
    if (Test-Installation) {
        Print-Info "You can now use 'dev_tool' command"
        Print-Info "Run 'dev_tool --help' for usage information"
        Print-Info "Run 'dev_tool settings' to configure your preferences"
    } else {
        Print-Warning "Please restart PowerShell or your terminal to use dev_tool"
    }
} else {
    Print-Error "Installation failed"
    exit 1
}