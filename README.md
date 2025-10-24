# 🔌 LHAtoLCSC - BOM to LCSC Part Matcher

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A professional desktop application to automatically match Bill of Materials (BOM) components with LCSC electronic parts using intelligent fuzzy search and LCSC API integration.

## ✨ Features

- 📊 **Excel BOM Import** - Load your existing BOM files effortlessly
- 🔍 **Fuzzy Search** - Intelligent component matching with confidence scoring
- 🎯 **LCSC API Integration** - Real-time access to 600,000+ components
- 📈 **Batch Processing** - Process entire BOMs automatically
- 💰 **Price & Stock Info** - Get current pricing and availability
- 📤 **Enhanced Export** - Export BOM with LCSC part numbers and pricing
- 🎨 **Modern GUI** - Clean, intuitive Tkinter interface
- ⚡ **Performance Optimized** - Local caching for speed

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- LCSC API credentials ([Apply here](https://www.lcsc.com/agent))

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/LHAtoLCSC.git
   cd LHAtoLCSC
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API credentials:**
   ```bash
   cp .env.example .env
   # Edit .env and add your LCSC API credentials
   ```

5. **Run the application:**
   ```bash
   python -m src.lhatolcsc
   ```

## 📖 Usage

1. **Launch Application** - Start LHAtoLCSC
2. **Load BOM** - Click "Load BOM" and select your Excel file
3. **Map Columns** - Verify "Stock Part Name" column detection
4. **Start Matching** - Click "Start Matching" to process BOM
5. **Review Results** - Check matches and approve/modify as needed
6. **Export** - Save enhanced BOM with LCSC part numbers

### Sample BOM Format

Your Excel BOM should have at minimum:

| Stock Part Name | Quantity | Reference Designator |
|----------------|----------|----------------------|
| STM32F103C8T6 | 1 | U1 |
| 10K Resistor 0603 | 10 | R1-R10 |
| 100nF Capacitor 0603 | 15 | C1-C15 |

## 🏗️ Project Structure

```
LHAtoLCSC/
├── src/lhatolcsc/          # Main application code
│   ├── api/                # LCSC API integration
│   ├── core/               # Core business logic
│   ├── gui/                # Tkinter GUI components
│   └── utils/              # Utility functions
├── tests/                  # Test suite
├── docs/                   # Documentation
├── resources/              # Icons, config, templates
└── scripts/                # Build and release scripts
```

## 🛠️ Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run tests with coverage
pytest --cov=src/lhatolcsc --cov-report=html

# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api/test_client.py

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov-report=term-missing
```

### Test Organization

All test files are organized in the `tests/` directory:

- `tests/test_*.py` - Unit and integration tests
- `tests/debug_*.py` - Debug utilities and test scripts
- `tests/verify_*.py` - Verification and validation scripts
- `tests/inspect_*.py` - Database and data inspection tools
- `tests/mock_*.py` - Mock server and test data utilities

**Note:** All new test files should be created in the `tests/` directory to maintain organization.

## 📋 LCSC API Overview

LHAtoLCSC uses the following LCSC API endpoints:

- **Keyword Search API** - Fuzzy search for components
- **Product Details API** - Get detailed part information
- **Category API** - Browse component categories
- **Manufacturer API** - Filter by brand

For detailed API documentation, see [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

## � Release Process

This project uses automated releases with semantic versioning. To create a new release:

```bash
# Preview the release (dry-run mode)
python ultimate_release.py patch --dry-run

# Create a patch release (bug fixes: 0.2.6 -> 0.2.7)
python ultimate_release.py patch

# Create a minor release (new features: 0.2.6 -> 0.3.0)
python ultimate_release.py minor

# Create a major release (breaking changes: 0.2.6 -> 1.0.0)
python ultimate_release.py major
```

The ultimate release script automatically:
- ✅ **GitHub API Integration** - Detects latest releases intelligently
- ✅ **Smart Version Calculation** - Calculates next version based on GitHub releases
- ✅ **Multi-File Updates** - Updates version in config.py, pyproject.toml, setup.py
- ✅ **Auto Release Notes** - Generates professional release notes from git commits
- ✅ **GitHub Actions** - Triggers workflows and waits for installer builds
- ✅ **Asset Verification** - Confirms Windows installer and portable ZIP uploads
- ✅ **Safety Features** - Rollback on failure, working directory validation
- ✅ **Professional Logging** - Beautiful colored output with detailed logging

For complete documentation, see [ULTIMATE_RELEASE_GUIDE.md](ULTIMATE_RELEASE_GUIDE.md).

**Prerequisites:**
- Install dependencies: `pip install pygithub gitpython`
- Set GitHub token: `export GITHUB_TOKEN="your_token"` or `gh auth login`

## �📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LCSC Electronics](https://www.lcsc.com/) for providing the API
- [Python](https://www.python.org/) and the open-source community
- All contributors to this project

## 📞 Support

- 📧 Email: support@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/LHAtoLCSC/issues)
- 📖 Documentation: [User Guide](docs/USER_GUIDE.md)

## 🗺️ Roadmap

- [x] Phase 1: Foundation and API Integration
- [x] Phase 2: Core Functionality
- [ ] Phase 3: GUI Development (In Progress)
- [ ] Phase 4: Advanced Features
- [ ] Phase 5: Testing & Documentation
- [ ] Phase 6: v1.0.0 Release

See [PROJECT_PLAN.md](PROJECT_PLAN.md) for detailed roadmap.

---

**Made with ❤️ for the electronics community**
