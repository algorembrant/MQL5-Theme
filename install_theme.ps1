$ErrorActionPreference = "Stop"

$extensionName = "mql5-support-dev"
$extensionsDir = "$env:USERPROFILE\.vscode\extensions"
$targetPath = "$extensionsDir\$extensionName"
$sourcePath = $PSScriptRoot

Write-Host "Installing MQL5 Theme (Dev Mode)..."

# Ensure extensions directory exists
if (-not (Test-Path -Path $extensionsDir)) {
    New-Item -ItemType Directory -Path $extensionsDir | Out-Null
}

# Remove existing link if it exists
if (Test-Path -Path $targetPath) {
    Write-Host "Removing existing link..."
    Remove-Item -Path $targetPath -Recurse -Force
}

# Create Junction
Write-Host "Linking $sourcePath to $targetPath"
New-Item -ItemType Junction -Path $targetPath -Target $sourcePath | Out-Null

Write-Host "--------------------------------------------------"
Write-Host "Success! The theme has been installed."
Write-Host "Please RESTART VS Code (or Reload Window) to see changes."
Write-Host "--------------------------------------------------"
