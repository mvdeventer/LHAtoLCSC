# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
