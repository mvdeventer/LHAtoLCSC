# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
