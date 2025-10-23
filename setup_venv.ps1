# Setup and Run Script for LHAtoLCSC in Virtual Environment
# This script sets up the virtual environment and runs the application

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "LHAtoLCSC Virtual Environment Setup" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

# Install/Update dependencies
Write-Host "Installing/Updating dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: Some dependencies may have failed to install" -ForegroundColor Yellow
}

# Install additional mock server dependencies
Write-Host "Installing Flask for mock server..." -ForegroundColor Yellow
pip install flask

# Install the application in development mode
Write-Host "Installing LHAtoLCSC package..." -ForegroundColor Yellow
pip install -e .

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "Virtual Environment Setup Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Available commands:" -ForegroundColor Cyan
Write-Host "  python main.py                    - Start the main application" -ForegroundColor White
Write-Host "  .\start_mock_server.ps1          - Start the mock LCSC server" -ForegroundColor White
Write-Host "  python test_search_history.py     - Test search history functionality" -ForegroundColor White
Write-Host "  python test_bulk_price_sorting.py - Test bulk price sorting" -ForegroundColor White
Write-Host ""
Write-Host "Your virtual environment is now active (venv)" -ForegroundColor Green
Write-Host "To deactivate, run: deactivate" -ForegroundColor Cyan