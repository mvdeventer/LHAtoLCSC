# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## v0.2.11
**Release Date:** 2025-10-24

### ✨ Features
â€¢ feat: ensure only latest version installers are released

### 🐛 Bug Fixes
â€¢ fix: handle Unicode encoding in build_installer.py for GitHub Actions
â€¢ fix: install InnoSetup in GitHub Actions workflow
â€¢ fix: restore build_installer.py needed for GitHub Actions

### 📝 Other Changes
â€¢ Release v0.2.10
â€¢ Release v0.2.9
â€¢ Release v0.2.8
â€¢ Release v0.2.7
â€¢ chore: remove old release scripts and update to ultimate_release.py
â€¢ changes
â€¢ chore: Release v0.2.6
â€¢ chore: Release v0.2.5
â€¢ Fix security vulnerabilities and code quality issues
â€¢ Fix code quality issues: remove unused imports, variables, and security warnings
â€¢ Update version to 0.2.5 for release
â€¢ v0.2.5: Improve horizontal scrolling speed, fix version consistency, organize tests
â€¢ Fix PyInstaller imports for logging and tkinter modules
â€¢ Update pyproject.toml version to 0.2.4
â€¢ Update version to 0.2.4 and improve PyInstaller module support
â€¢ Release 0.2.4: Enhanced pagination, currency persistence, and release automation


## v0.2.10
**Release Date:** 2025-10-24

### ✨ Features
â€¢ feat: ensure only latest version installers are released

### 🐛 Bug Fixes
â€¢ fix: install InnoSetup in GitHub Actions workflow
â€¢ fix: restore build_installer.py needed for GitHub Actions

### 📝 Other Changes
â€¢ Release v0.2.9
â€¢ Release v0.2.8
â€¢ Release v0.2.7
â€¢ chore: remove old release scripts and update to ultimate_release.py
â€¢ changes
â€¢ chore: Release v0.2.6
â€¢ chore: Release v0.2.5
â€¢ Fix security vulnerabilities and code quality issues
â€¢ Fix code quality issues: remove unused imports, variables, and security warnings
â€¢ Update version to 0.2.5 for release
â€¢ v0.2.5: Improve horizontal scrolling speed, fix version consistency, organize tests
â€¢ Fix PyInstaller imports for logging and tkinter modules
â€¢ Update pyproject.toml version to 0.2.4
â€¢ Update version to 0.2.4 and improve PyInstaller module support
â€¢ Release 0.2.4: Enhanced pagination, currency persistence, and release automation


## v0.2.9
**Release Date:** 2025-10-24

### ✨ Features
â€¢ feat: ensure only latest version installers are released

### 🐛 Bug Fixes
â€¢ fix: restore build_installer.py needed for GitHub Actions

### 📝 Other Changes
â€¢ Release v0.2.8
â€¢ Release v0.2.7
â€¢ chore: remove old release scripts and update to ultimate_release.py
â€¢ changes
â€¢ chore: Release v0.2.6
â€¢ chore: Release v0.2.5
â€¢ Fix security vulnerabilities and code quality issues
â€¢ Fix code quality issues: remove unused imports, variables, and security warnings
â€¢ Update version to 0.2.5 for release
â€¢ v0.2.5: Improve horizontal scrolling speed, fix version consistency, organize tests
â€¢ Fix PyInstaller imports for logging and tkinter modules
â€¢ Update pyproject.toml version to 0.2.4
â€¢ Update version to 0.2.4 and improve PyInstaller module support
â€¢ Release 0.2.4: Enhanced pagination, currency persistence, and release automation


## v0.2.8
**Release Date:** 2025-10-24

### ✨ Features
â€¢ feat: ensure only latest version installers are released

### 📝 Other Changes
â€¢ Release v0.2.7
â€¢ chore: remove old release scripts and update to ultimate_release.py
â€¢ changes
â€¢ chore: Release v0.2.6
â€¢ chore: Release v0.2.5
â€¢ Fix security vulnerabilities and code quality issues
â€¢ Fix code quality issues: remove unused imports, variables, and security warnings
â€¢ Update version to 0.2.5 for release
â€¢ v0.2.5: Improve horizontal scrolling speed, fix version consistency, organize tests
â€¢ Fix PyInstaller imports for logging and tkinter modules
â€¢ Update pyproject.toml version to 0.2.4
â€¢ Update version to 0.2.4 and improve PyInstaller module support
â€¢ Release 0.2.4: Enhanced pagination, currency persistence, and release automation


## v0.2.7
**Release Date:** 2025-10-24

### 📝 Other Changes
â€¢ chore: remove old release scripts and update to ultimate_release.py
â€¢ changes
â€¢ chore: Release v0.2.6
â€¢ chore: Release v0.2.5
â€¢ Fix security vulnerabilities and code quality issues
â€¢ Fix code quality issues: remove unused imports, variables, and security warnings
â€¢ Update version to 0.2.5 for release
â€¢ v0.2.5: Improve horizontal scrolling speed, fix version consistency, organize tests
â€¢ Fix PyInstaller imports for logging and tkinter modules
â€¢ Update pyproject.toml version to 0.2.4
â€¢ Update version to 0.2.4 and improve PyInstaller module support
â€¢ Release 0.2.4: Enhanced pagination, currency persistence, and release automation


## v0.1.0

**Release Date:** 2025-10-21

## ✨ New Features

- feat: Add version info to all windows and complete release automation
- feat: Initial project setup with complete structure

## 🐛 Bug Fixes

- fix: Add UTF-8 encoding support to release script for Windows compatibility

---

## 📋 Requirements

- Python 3.8 or higher
- tkinter (usually included with Python)
- Flask 3.1.2 (for mock server)

## 🚀 Installation

```bash
pip install -r requirements.txt
python main.py
```

## 🧪 Testing with Mock Server

```bash
python tests/mock_lcsc_server.py
```

Then use the **🧪 Use Mock Server Credentials** button in the settings dialog.


## v0.2.0

**Release Date:** 2025-10-22

## ✨ New Features

### Professional Corporate Theme
- **New Theme System**: Created comprehensive `CorporateTheme` class with modern navy blue/orange color scheme
- **Consistent UI**: Applied professional styling to all windows (main, stock browser, settings, popups)
- **Color Palette**:
  - Primary: Navy Blue (#2c5f8d) for professional corporate appearance
  - Accent: Warm Orange (#ff6b35) for important actions
  - Success: Green (#27ae60) for positive actions
  - Professional grays for backgrounds and text
- **Enhanced Components**:
  - Professional status bars with dark slate backgrounds
  - Styled action buttons (Accent, Success, Danger)
  - Modern data grids with professional headers
  - Segoe UI fonts throughout
  - Alternating row colors for better readability
- **Suitable for**: Company stock management and inventory applications

### Enhanced Search & Features
- **Comprehensive Fuzzy Search**: Advanced fuzzy matching with 75% similarity threshold
- **Multi-keyword Search**: All keywords must match for results
- **Typo Tolerance**: Handles common typos and character variations
- **Search Fields**: Product code, model, brand, package, description, category
- **Unicode Cleaning**: Proper handling of Ω, ±, µ, ° characters in displays and exports

### Stock Browser Improvements
- **Lazy Loading**: Instant window open, loads data on demand
- **10 Price Columns**: Displays all price breaks (1+, 10+, 25+, 50+, 100+, 200+, 500+, 1K+, 5K+, 10K+)
- **Sortable Columns**: Click headers to sort by stock or price
- **Description Column**: Shows product descriptions with search capability
- **Theme Integration**: Professional corporate styling throughout

### Mock Server Enhancements
- **Interactive CLI**: 10 commands (help, status, reload, info, search, random, stats, categories, brands, quit)
- **Fuzzy Search**: Server-side fuzzy matching for realistic testing
- **104K Components**: Complete database with resistors, capacitors, inductors, ICs, sensors, connectors
- **Product Descriptions**: All components have detailed LCSC-style descriptions
- **Datasheet URLs**: PDF links for all products
- **Random Pricing**: 1-10 price tiers per component (randomized from 10 possible quantities)

### Documentation
- Added `DESCRIPTION_FEATURE.md` - Product description implementation guide
- Added `README_PRICE_UPDATER.md` - Mock database pricing update tool
- Updated all documentation with theme details

## 🐛 Bug Fixes
- Fixed page size filter capping at 100 (now detects localhost for 1000 max)
- Fixed sticky parameter tuples in grid layouts (changed to strings)
- Fixed Unicode character handling in CSV exports
- Fixed search to include productIntroEn field

## 🎨 UI/UX Improvements
- Modern corporate color scheme suitable for business applications
- Professional fonts (Segoe UI) throughout
- Consistent button styling (primary, accent, success, danger)
- Enhanced status bars with better visibility
- Professional data grid headers
- Improved spacing and padding

---

## v0.2.3

**Release Date:** 2025-10-23

### 🐛 Bug Fixes
- **Enhanced API Client**: Improved API client resilience and error handling
- **Stock Browser Improvements**: Fixed display issues and enhanced functionality
- **Mock Server Updates**: Updated mock LCSC server with improved data handling

### 🧪 Testing
- **Comprehensive Test Suite**: Added complete test suite for API categories and endpoints
- **Database Integration Tests**: Added tests for category verification and database operations
- **Category Tree Testing**: Added category tree JSON file and related test scripts
- **Performance Testing**: Added search performance tests
- **Fuzz Testing**: Added fuzzy search test validation
- **Integration Scripts**: Added various verification and mock data generation scripts

## [Unreleased]

### Added
-

### Changed
-

### Fixed
-

---

## v0.2.2

**Release Date:** 2025-10-22

### ✨ New Features
- **Automatic Release Notes**: Release notes are now automatically extracted from CHANGELOG.md and included in GitHub releases
- **MANIFEST.in**: Added proper packaging manifest for source distributions

### 🐛 Bug Fixes
- **Fixed GitHub Actions Build**: Made setup.py resilient to missing requirements.txt in isolated build environments
- **Fixed Package Building**: Added fallback requirements list to ensure builds succeed in CI/CD pipelines
- **Fixed File Handling**: Proper pathlib usage for cross-platform compatibility

### 📚 Documentation
- Enhanced release workflow documentation
- Improved build process reliability

---

## v0.2.1

**Release Date:** 2025-10-22

### ✨ New Features
- **Release Automation**: Complete automated release workflow
  - `release.bat` - Simple Windows wrapper for releases
  - `release_workflow.py` - Complete automation (test → build → version → commit → push → release)
  - `build_installer.py` - Windows installer creation with PyInstaller + InnoSetup
- **Windows Installer**: Professional Windows installer (.exe) with InnoSetup
  - Standalone executable (64 MB)
  - Setup wizard with start menu integration
  - Portable ZIP distribution
  - Automatic dependency inclusion

### 🐛 Bug Fixes
- **Fixed PyInstaller Dependencies**: Use venv's PyInstaller to ensure all dependencies are included
- **Fixed Module Imports**: Properly include python-dotenv, pydantic, diskcache, and all required packages
- **Window Visibility**: Ensure main window appears in foreground on startup
- **InnoSetup Script**: Handle optional files (icon.ico, .env.example, docs) gracefully

### 🎨 UI/UX Improvements
- Main window now forces focus and appears on top on startup
- Better window positioning and visibility

### 📚 Documentation
- Added `BUILD_RELEASE_GUIDE.md` - Complete build and release documentation
- Added `RELEASE_QUICKSTART.md` - Quick reference for releases

---

### Added
- Release automation script (`release.py`) with version detection and GitHub CLI integration
- Automatic release notes generation from commit messages
- Mock server credentials auto-fill button (🧪) in settings wizard
- Mock API server with 104,042+ components:
  - 35,280 Resistors (10 manufacturers, 12 packages)
  - 49,329 Capacitors (10 manufacturers, various packages)
  - 8,652 Inductors (8 manufacturers)
  - 6,780 Crystals (7 manufacturers)
  - 1,305 ICs (MCUs, op-amps, regulators, interface ICs)
  - 516 Sensors (temperature, pressure, humidity, motion, magnetic, light)
  - 2,180 Connectors (USB, pin headers, card slots, wire-to-board, RF)
- Comprehensive release process documentation (RELEASE.md)

### Fixed
- Sticky parameter types in tkinter (converted tuples to strings)
- API endpoint paths to match LCSC structure (/rest/wmsc2agent/*)
- Authentication to use query parameters instead of headers

### Planned
- Full GUI implementation for BOM management
- Advanced fuzzy matching algorithms
- Batch processing optimization
- Export to multiple formats
- Local caching for improved performance

## [0.1.0] - 2025-10-21

### Added
- Initial project structure and setup
- LCSC API integration module
  - Authentication with SHA1 signature
  - Product search API (fuzzy and exact)
  - Product details API
  - Category and brand APIs
- Core business logic
  - Configuration management with .env support
  - Logging setup with file rotation
  - BOM processor for Excel files
  - Fuzzy matching engine with RapidFuzz
- Basic Tkinter GUI
  - Main application window
  - Menu bar structure
  - API connection testing
- Development infrastructure
  - Complete Python package structure
  - Testing setup with pytest
  - Code quality tools (Black, Flake8, MyPy)
  - GitHub Actions CI/CD pipeline
  - Automated release workflow
- Documentation
  - Comprehensive project plan
  - API documentation
  - README with quick start guide
  - Development setup guide

### Technical Details
- Python 3.10+ support
- Modular architecture (API, Core, GUI layers)
- Type hints throughout codebase
- Comprehensive error handling
- Rate limiting and retry logic
- Extensive logging

[Unreleased]: https://github.com/yourusername/LHAtoLCSC/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/LHAtoLCSC/releases/tag/v0.1.0
