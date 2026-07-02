$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$appHome = Join-Path $env:LOCALAPPDATA "TabdealPythonSDK"
$venvPath = Join-Path $appHome "venv"
$venvPython = Join-Path $venvPath "Scripts\\python.exe"

function Resolve-Python {
    $candidates = @(
        @{ Cmd = "py"; Args = @("-3.11", "-c", "import sys; print(sys.executable)") },
        @{ Cmd = "py"; Args = @("-3", "-c", "import sys; print(sys.executable)") },
        @{ Cmd = "python"; Args = @("-c", "import sys; print(sys.executable)") }
    )

    foreach ($candidate in $candidates) {
        try {
            $resolved = & $candidate.Cmd @($candidate.Args) 2>$null
            if ($LASTEXITCODE -eq 0 -and $resolved) {
                return $resolved.Trim()
            }
        } catch {
        }
    }

    if (Get-Command winget -ErrorAction SilentlyContinue) {
        Write-Host "Python not found. Installing Python 3.11 with winget..."
        winget install -e --id Python.Python.3.11 --accept-package-agreements --accept-source-agreements
        return Resolve-Python
    }

    throw "Python 3 was not found and winget is unavailable. Please install Python 3.11+ and run this script again."
}

$python = Resolve-Python
New-Item -ItemType Directory -Force -Path $appHome | Out-Null

if (-not (Test-Path $venvPython)) {
    Write-Host "Creating virtual environment at $venvPath"
    & $python -m venv $venvPath
}

Write-Host "Upgrading pip..."
& $venvPython -m pip install --upgrade pip

Write-Host "Installing tabdeal-python from $projectRoot"
& $venvPython -m pip install --upgrade $projectRoot

Write-Host "Launching Tabdeal Quickstart Panel..."
& $venvPython -m tabdeal
