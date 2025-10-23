# Start Mock LCSC API Server
Write-Host '============================================================' -ForegroundColor Cyan
Write-Host 'Starting Mock LCSC API Server' -ForegroundColor Cyan
Write-Host '============================================================' -ForegroundColor Cyan
Write-Host ''
Write-Host 'Mock Credentials:' -ForegroundColor Yellow
Write-Host '  API Key:    test_api_key_12345' -ForegroundColor Green
Write-Host '  API Secret: test_api_secret_67890' -ForegroundColor Green
Write-Host '  API URL:    http://localhost:5000' -ForegroundColor Green
Write-Host ''
Write-Host 'Press Ctrl+C to stop the server' -ForegroundColor Yellow
Write-Host '============================================================' -ForegroundColor Cyan
Write-Host ''

if (-not (Test-Path 'venv\Scripts\python.exe')) {
    Write-Host 'Error: Virtual environment not found. Run .\setup_venv.ps1 first.' -ForegroundColor Red
    exit 1
}

if (-not (Test-Path 'tests\mock_lcsc_server.py')) {
    Write-Host 'Error: Mock server file not found' -ForegroundColor Red
    exit 1
}

Write-Host 'Starting server...' -ForegroundColor Gray
& '.\venv\Scripts\python.exe' 'tests\mock_lcsc_server.py'
