# Developer Guide

## Development Setup

### Prerequisites

- Python 3.10+
- Git
- VS Code (recommended)

### Initial Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/LHAtoLCSC.git
   cd LHAtoLCSC
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

3. **Install development dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

## Development Workflow

### Branch Strategy

- `main`: Production-ready code
- `develop`: Integration branch
- `feature/*`: Feature development
- `bugfix/*`: Bug fixes
- `release/*`: Release preparation

### Making Changes

1. **Create feature branch:**
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make your changes**

3. **Run tests:**
   ```bash
   pytest
   ```

4. **Format code:**
   ```bash
   black src/ tests/
   isort src/ tests/
   ```

5. **Commit changes:**
   ```bash
   git commit -m "feat: Add new feature"
   ```

## Code Style

### Formatting

We use:
- **Black** for code formatting (line length: 100)
- **isort** for import sorting
- **Flake8** for linting
- **MyPy** for type checking

Run all checks:
```bash
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: Add fuzzy search widget
fix: Correct API signature generation
docs: Update user guide
test: Add unit tests for BOM processor
refactor: Simplify matcher logic
chore: Update dependencies
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/lhatolcsc --cov-report=html

# Run specific test file
pytest tests/test_api/test_auth.py

# Run tests matching pattern
pytest -k "test_auth"
```

### Writing Tests

Place tests in `tests/` directory, mirroring the source structure:

```python
# tests/test_api/test_client.py
def test_search_products():
    """Test product search."""
    # Arrange
    client = LCSCClient("key", "secret")
    
    # Act
    result = client.search_products("STM32")
    
    # Assert
    assert result.total > 0
```

## Project Structure

```
src/lhatolcsc/
├── __init__.py
├── __main__.py
├── api/              # API integration
│   ├── auth.py
│   ├── client.py
│   ├── endpoints.py
│   └── models.py
├── core/             # Business logic
│   ├── bom_processor.py
│   ├── config.py
│   ├── logger.py
│   └── matcher.py
├── gui/              # GUI components
│   └── main_window.py
└── utils/            # Utilities
```

## Adding New Features

### 1. API Endpoint

1. Add endpoint to `api/endpoints.py`
2. Add method to `api/client.py`
3. Add tests to `tests/test_api/test_client.py`

### 2. GUI Component

1. Create module in `gui/`
2. Import in `gui/main_window.py`
3. Add to main window layout

### 3. Core Logic

1. Add module to `core/`
2. Add tests to `tests/test_core/`
3. Update documentation

## Debugging

### VS Code Configuration

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        },
        {
            "name": "LHAtoLCSC",
            "type": "python",
            "request": "launch",
            "module": "lhatolcsc",
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/src"
            }
        }
    ]
}
```

### Logging

Enable debug logging in `.env`:
```
LOG_LEVEL=DEBUG
DEBUG=true
```

## Building and Distribution

### Build Package

```bash
python -m build
```

### Build Windows Executable

```bash
pip install pyinstaller
pyinstaller --name LHAtoLCSC --onefile --windowed src/lhatolcsc/__main__.py
```

## Release Process

1. Update version in `setup.py` and `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create release branch: `git checkout -b release/v1.0.0`
4. Run full test suite
5. Merge to `main`
6. Tag release: `git tag -a v1.0.0 -m "Release v1.0.0"`
7. Push: `git push origin v1.0.0`
8. GitHub Actions will create the release

## Troubleshooting

### Import Errors

Add project root to PYTHONPATH:
```bash
set PYTHONPATH=%CD%\src  # Windows
# export PYTHONPATH=$PWD/src  # macOS/Linux
```

### Test Failures

1. Check virtual environment is activated
2. Ensure all dependencies installed
3. Check Python version (3.10+)
4. Clear pytest cache: `pytest --cache-clear`

## Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Black Documentation](https://black.readthedocs.io/)
- [Type Hints (PEP 484)](https://peps.python.org/pep-0484/)

## Getting Help

- Open an issue on GitHub
- Check existing issues and discussions
- Read the User Guide and API documentation

---

**Happy coding!** 🚀
