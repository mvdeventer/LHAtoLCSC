# Quick activation script for LHAtoLCSC virtual environment

if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "Error: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run '.\setup_venv.ps1' first to create the environment." -ForegroundColor Yellow
    exit 1
}

Write-Host "Activating LHAtoLCSC virtual environment..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "Virtual environment is now active!" -ForegroundColor Green
Write-Host "Run 'python main.py' to start the application" -ForegroundColor Cyan