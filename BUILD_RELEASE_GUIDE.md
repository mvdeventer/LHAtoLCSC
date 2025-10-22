# Build and Release Guide

This guide explains how to build installers and create releases for LHAtoLCSC.

## Prerequisites

### Required
- **Python 3.8+** with pip
- **Git** with GitHub account
- **GitHub CLI** (`gh`) - Install from https://cli.github.com/

### Optional (for installers)
- **PyInstaller** - Install with: `pip install pyinstaller`
- **InnoSetup 6** - Download from https://jrsoftware.org/isdl.php

## Quick Start

### Simple Release (Recommended)

The easiest way to create a release with everything automated:

```bash
# Patch release (0.2.0 -> 0.2.1)
release.bat patch

# Minor release (0.2.0 -> 0.3.0)
release.bat minor

# Major release (0.2.0 -> 1.0.0)
release.bat major
```

This will:
1. ✅ Run tests
2. 🔨 Build Windows installer (if tools available)
3. 📝 Update version in all files
4. 📋 Update CHANGELOG.md
5. 💾 Commit changes to git
6. 🏷️ Create git tag
7. 🚀 Push to GitHub
8. 📦 Create GitHub release with installer

### Dry Run

Test what would happen without making changes:

```bash
python release_workflow.py patch --dry-run
```

### Skip Options

```bash
# Skip tests
python release_workflow.py patch --skip-tests

# Skip building installer
python release_workflow.py patch --skip-installer

# Both
python release_workflow.py patch --skip-tests --skip-installer
```

## Manual Steps

### Build Installer Only

To build just the Windows installer without releasing:

```bash
python build_installer.py
```

This creates:
- `dist/LHAtoLCSC.exe` - Standalone executable
- `installer/LHAtoLCSC-X.X.X-Setup.exe` - Windows installer (if InnoSetup installed)
- `installer/LHAtoLCSC-X.X.X-Portable.zip` - Portable ZIP package

### Manual Release Steps

If you prefer to do it manually:

1. **Update version** in:
   - `src/lhatolcsc/core/config.py`
   - `setup.py`

2. **Update CHANGELOG.md**:
   ```markdown
   ## v0.2.1
   
   **Release Date:** 2025-10-22
   
   ### Added
   - New feature...
   ```

3. **Build installer**:
   ```bash
   python build_installer.py
   ```

4. **Commit and tag**:
   ```bash
   git add -A
   git commit -m "chore: Release v0.2.1"
   git tag -a v0.2.1 -m "Release v0.2.1"
   ```

5. **Push to GitHub**:
   ```bash
   git push origin master
   git push origin v0.2.1
   ```

6. **Create GitHub release**:
   ```bash
   gh release create v0.2.1 ^
       --title "v0.2.1" ^
       --notes "See CHANGELOG.md for details" ^
       installer/LHAtoLCSC-0.2.1-Setup.exe ^
       installer/LHAtoLCSC-0.2.1-Portable.zip
   ```

## Installer Details

### PyInstaller Configuration

The `LHAtoLCSC.spec` file is auto-generated and includes:
- All Python dependencies
- Tkinter GUI libraries
- Documentation files (README, LICENSE)
- Application resources

### InnoSetup Configuration

The `installer.iss` file creates a professional Windows installer with:
- Start menu shortcuts
- Desktop icon (optional)
- Uninstaller
- License agreement
- Custom icon (if `icon.ico` exists)

### Build Artifacts

After building, you'll find:

```
dist/
  └── LHAtoLCSC.exe              # Standalone executable (~50 MB)

installer/
  ├── LHAtoLCSC-X.X.X-Setup.exe  # Windows installer (~50 MB)
  └── LHAtoLCSC-X.X.X-Portable.zip  # Portable package (~50 MB)
```

## Troubleshooting

### PyInstaller Not Found

```bash
pip install pyinstaller
```

### InnoSetup Not Found

1. Download from https://jrsoftware.org/isdl.php
2. Install to default location (`C:\Program Files (x86)\Inno Setup 6`)
3. Or add custom location to PATH

### GitHub CLI Not Authenticated

```bash
gh auth login
```

### Build Fails on Tkinter

Make sure you have the full Python installation with Tkinter:
```bash
python -m tkinter  # Should open a test window
```

### Executable Too Large

The executable includes Python runtime and all dependencies. This is normal for PyInstaller builds. Typical size: 40-60 MB.

To reduce size:
- Remove unused dependencies from `requirements.txt`
- Use `--exclude` option in PyInstaller spec
- Enable UPX compression (already enabled)

### Release Already Exists

If a tag/release already exists:

```bash
# Delete tag locally
git tag -d v0.2.1

# Delete tag remotely
git push origin :refs/tags/v0.2.1

# Delete release on GitHub
gh release delete v0.2.1

# Try again
release.bat patch
```

## CI/CD Integration

To automate releases on GitHub Actions, create `.github/workflows/release.yml`:

```yaml
name: Build and Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pyinstaller
      
      - name: Build installer
        run: python build_installer.py
      
      - name: Upload to release
        uses: softprops/action-gh-release@v1
        with:
          files: installer/*
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Version Numbering

We use [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0): Breaking changes, incompatible API changes
- **MINOR** (0.2.0): New features, backwards compatible
- **PATCH** (0.2.1): Bug fixes, backwards compatible

Examples:
- `0.1.0` → `0.2.0`: Added new features
- `0.2.0` → `0.2.1`: Fixed bugs
- `0.2.1` → `1.0.0`: First stable release

## Best Practices

1. **Always test before release**: Run `pytest` or manual tests
2. **Update CHANGELOG**: Document all changes
3. **Tag consistently**: Use `vX.Y.Z` format
4. **Test installer**: Install and run before pushing
5. **Write release notes**: Help users understand what changed
6. **Keep builds reproducible**: Document all dependencies

## Support

For issues with the build/release process:
1. Check this guide
2. Review error messages
3. Open an issue on GitHub
4. Check GitHub Actions logs (if using CI/CD)

---

**Last Updated:** 2025-10-22
