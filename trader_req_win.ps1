# PowerShell script to install Python and required modules for automation

# Check if Python is already installed
$pythonInstalled = $False
try {
    $pythonInstalled = python --version
}
catch {
    Write-Host "Python is not installed."
}

# Install Python if not already installed
if (-not $pythonInstalled) {
    # Download Python installer
    $pythonInstallerUrl = "https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe"
    $pythonInstallerPath = "$env:TEMP\python_installer.exe"
    Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $pythonInstallerPath

    # Run Python installer
    Start-Process $pythonInstallerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
    Write-Host "Python installed successfully."
}

# Check if pip is installed
try {
    pip --version
}
catch {
    Write-Host "pip is not installed. Installing pip."
    # Install pip
    Invoke-Expression "python -m ensurepip"
}

# Install required Python packages
$requiredModules = @("requests", "Pillow", "pyautogui", "keyboard")
foreach ($module in $requiredModules) {
    pip install $module
    Write-Host "$module installed successfully."
}

Write-Host "Setup complete. Python and required modules are installed."
