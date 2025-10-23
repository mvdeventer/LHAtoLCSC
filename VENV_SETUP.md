# Virtual Environment Setup Guide

This guide explains how to set up and use the LHAtoLCSC application in a Python virtual environment.

## Quick Start

### 1. Setup Virtual Environment (One-time setup)
```powershell
.\setup_venv.ps1
```
This script will:
- Create a new virtual environment in the `venv` folder
- Activate the virtual environment
- Install all required dependencies
- Install Flask for the mock server

### 2. Daily Usage
```powershell
# Activate the virtual environment
.\activate_venv.ps1

# Then run any of these commands:
python main.py                    # Start the main application
.\start_mock_server.ps1          # Start the mock LCSC server  
python test_search_history.py     # Test search history functionality
python test_bulk_price_sorting.py # Test bulk price sorting
```

## Manual Setup (Alternative)

If you prefer to set up manually:

```powershell
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
python main.py
```

## Features Available in Virtual Environment

### ✅ Search History
- **Location**: Stock Browser → Search → History dropdown
- **Features**: 
  - Remembers up to 100 search terms
  - Persistent between app restarts
  - Click history item to automatically search
  - Clear history button available
- **Storage**: `~/.lhatolcsc/search_history.json`

### ✅ Bulk Price Sorting
- **Feature**: Search results sorted by cheapest bulk price first
- **Logic**: Finds lowest price at highest quantity break for each component
- **Benefit**: Prioritizes components with best value for large orders

### ✅ Currency Conversion
- **Location**: Stock Browser → Currency dropdown
- **Features**:
  - 20+ supported currencies
  - Real-time exchange rates
  - Live price conversion
  - Currency symbols in column headers

### ✅ Mock Server
- **URL**: http://localhost:5000
- **Database**: 104,042+ components
- **Performance**: Optimized SQL queries with smart sorting

## Virtual Environment Benefits

- **Isolation**: Dependencies don't conflict with system Python
- **Reproducibility**: Same environment across different machines
- **Clean**: Easy to delete and recreate if needed
- **Version Control**: Specific dependency versions ensure compatibility

## Troubleshooting

### Permission Issues
If you get execution policy errors:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Missing Dependencies
If imports fail, reinstall dependencies:
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Virtual Environment Issues
If venv is corrupted, recreate it:
```powershell
Remove-Item -Recurse -Force venv
.\setup_venv.ps1
```

## Development

### Testing
All tests work in the virtual environment:
```powershell
python test_search_history.py     # Test search history
python test_bulk_price_sorting.py # Test sorting algorithm
python test_smart_sorting.py      # Test smart search results
```

### Adding New Dependencies
1. Install in virtual environment: `pip install package_name`
2. Update requirements: `pip freeze > requirements.txt`
3. Commit the updated requirements.txt

## File Structure
```
venv/                          # Virtual environment (auto-created)
├── Scripts/
│   ├── Activate.ps1          # Activation script
│   └── python.exe            # Python interpreter
└── Lib/site-packages/        # Installed packages

setup_venv.ps1                # One-time setup script
activate_venv.ps1             # Daily activation script
start_mock_server.ps1         # Mock server (venv-compatible)
requirements.txt              # Dependencies list
```

The virtual environment keeps everything isolated and ensures consistent behavior across different systems.