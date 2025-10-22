# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


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

## [Unreleased]

### Added
- 

### Changed
- 

### Fixed
- 

---

## v0.2.1

**Release Date:** 2025-10-22



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
