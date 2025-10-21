# Quick Start: Creating a Release

## Prerequisites

Install GitHub CLI if not already installed:

```powershell
# Windows (PowerShell)
winget install --id GitHub.cli

# Or download from: https://cli.github.com/
```

Authenticate with GitHub:

```powershell
gh auth login
```

## Create a Release

### 1. Preview the Release (Dry Run)

```powershell
python release.py patch --dry-run
```

This shows you what will happen without making any changes.

### 2. Create the Release

For bug fixes and minor changes:
```powershell
python release.py patch
```

For new features:
```powershell
python release.py minor
```

For breaking changes:
```powershell
python release.py major
```

### 3. Confirm

When prompted, type `yes` to proceed with the release.

The script will:
- ✅ Update version numbers in files
- ✅ Update CHANGELOG.md
- ✅ Create a git commit
- ✅ Create a git tag
- ✅ Push to GitHub
- ✅ Create a GitHub release with auto-generated notes

## Version Bumping

- **patch**: 0.1.0 → 0.1.1 (bug fixes)
- **minor**: 0.1.0 → 0.2.0 (new features)
- **major**: 0.1.0 → 1.0.0 (breaking changes)

## Options

```powershell
# Create a prerelease
python release.py minor --prerelease

# Skip pushing (local testing)
python release.py patch --skip-push

# Preview without changes
python release.py patch --dry-run
```

## Troubleshooting

**"Working directory is not clean"**
```powershell
git status
git add .
git commit -m "Your message"
```

**"GitHub CLI not authenticated"**
```powershell
gh auth login
```

**Undo a release (before pushing)**
```powershell
git tag -d v0.2.0
git reset --hard HEAD~1
```

For more details, see [RELEASE.md](RELEASE.md)
