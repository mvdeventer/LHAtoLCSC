# Start Mock LCSC API Server
# Run this in a separate terminal window

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Starting Mock LCSC API Server" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Mock Credentials:" -ForegroundColor Yellow
Write-Host "  API Key:    test_api_key_12345" -ForegroundColor Green
Write-Host "  API Secret: test_api_secret_67890" -ForegroundColor Green
Write-Host "  API URL:    http://localhost:5000" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment and run server
& .\venv\Scripts\Activate.ps1
python tests\mock_lcsc_server.py
