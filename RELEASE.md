# Release Process Documentation

This document describes how to create releases for the LHAtoLCSC project.

## Prerequisites

Before creating a release, ensure you have:

1. **Git** installed and configured
2. **GitHub CLI (gh)** installed and authenticated
   ```bash
   # Install GitHub CLI
   # Windows (using winget)
   winget install --id GitHub.cli
   
   # Or download from: https://cli.github.com/
   
   # Authenticate
   gh auth login
   ```
3. **Clean working directory** (all changes committed)
4. **Main/master branch** checked out (or your release branch)

## Release Script Usage

The `release.py` script automates the entire release process:

### Basic Usage

```bash
# Patch release (0.1.0 -> 0.1.1) - Bug fixes
python release.py patch

# Minor release (0.1.0 -> 0.2.0) - New features
python release.py minor

# Major release (0.1.0 -> 1.0.0) - Breaking changes
python release.py major
```

### Options

```bash
# Dry run - preview without making changes
python release.py patch --dry-run

# Create a prerelease
python release.py minor --prerelease

# Skip pushing to remote (local testing)
python release.py patch --skip-push
```

## What the Script Does

The release script performs the following steps automatically:

1. **Prerequisites Check**
   - Verifies Git is installed
   - Verifies GitHub CLI is installed and authenticated
   - Checks working directory is clean
   - Shows current branch

2. **Version Detection**
   - Finds the latest semantic version tag
   - Calculates the next version based on bump type
   - Shows version progression

3. **Release Notes Generation**
   - Collects commits since last tag
   - Categorizes commits (features, fixes, improvements, docs)
   - Generates formatted release notes
   - Shows preview before proceeding

4. **Version Update**
   - Updates `__version__` in Python files
   - Updates `CHANGELOG.md` with new entry

5. **Git Operations**
   - Commits all changes with release message
   - Creates annotated git tag
   - Pushes commits to remote
   - Pushes tag to remote

6. **GitHub Release**
   - Creates GitHub release with release notes
   - Links to the git tag
   - Marks as prerelease if specified

## Semantic Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version (X.0.0): Incompatible API changes
- **MINOR** version (0.X.0): New features (backwards compatible)
- **PATCH** version (0.0.X): Bug fixes (backwards compatible)

### When to Use Each

**Patch Release (0.1.0 → 0.1.1)**
- Bug fixes
- Security patches
- Documentation updates
- Minor improvements without new features

**Minor Release (0.1.0 → 0.2.0)**
- New features
- Enhancements to existing features
- Non-breaking API changes
- Deprecations (with backward compatibility)

**Major Release (0.1.0 → 1.0.0)**
- Breaking changes
- Major redesign
- Removed deprecated features
- Incompatible API changes

## Commit Message Conventions

For better release notes, use conventional commit messages:

```bash
# Features
git commit -m "feat: Add mock server credentials button"
git commit -m "feature: Implement component search"

# Bug Fixes
git commit -m "fix: Correct sticky parameter types in tkinter"
git commit -m "bugfix: Handle missing API credentials gracefully"

# Improvements
git commit -m "improve: Optimize database loading performance"
git commit -m "update: Enhance error messages"

# Documentation
git commit -m "docs: Add release process documentation"
git commit -m "doc: Update README with new features"
```

The script will automatically categorize these into sections in the release notes.

## Example Workflow

### Making a Patch Release

```bash
# 1. Ensure you're on the main branch
git checkout main
git pull origin main

# 2. Preview the release
python release.py patch --dry-run

# 3. Review the generated release notes
# 4. If everything looks good, create the release
python release.py patch

# 5. Confirm when prompted
Do you want to continue? (yes/no): yes

# 6. Script will:
#    - Update version files
#    - Update CHANGELOG.md
#    - Create commit and tag
#    - Push to GitHub
#    - Create GitHub release

# 7. View the release on GitHub
# The script will show you the URL
```

### Making a Minor Release

```bash
# Same process but with 'minor' instead of 'patch'
python release.py minor
```

## Manual Release Process (Fallback)

If you need to create a release manually:

### 1. Update Version

Edit version in relevant files:
- `src/lhatolcsc/__init__.py`
- `src/lhatolcsc/core/config.py`

### 2. Update CHANGELOG.md

Add a new section at the top:

```markdown
## v0.2.0 - 2025-10-21

### Features
- New feature description

### Bug Fixes
- Bug fix description
```

### 3. Commit Changes

```bash
git add .
git commit -m "Release v0.2.0"
```

### 4. Create Tag

```bash
git tag -a v0.2.0 -m "Release v0.2.0"
```

### 5. Push to GitHub

```bash
git push origin main
git push origin v0.2.0
```

### 6. Create GitHub Release

```bash
gh release create v0.2.0 \
  --title "Release v0.2.0" \
  --notes-file CHANGELOG.md
```

Or create manually through GitHub web interface.

## Troubleshooting

### GitHub CLI Not Authenticated

```bash
gh auth login
# Follow the prompts to authenticate
```

### Working Directory Not Clean

```bash
# Check status
git status

# Commit or stash changes
git add .
git commit -m "Your commit message"

# Or stash for later
git stash
```

### Need to Undo a Failed Release

```bash
# Delete local tag
git tag -d v0.2.0

# Reset last commit (if not pushed)
git reset --hard HEAD~1

# If already pushed, delete remote tag
git push origin :refs/tags/v0.2.0

# Delete GitHub release
gh release delete v0.2.0
```

### Version Already Exists

```bash
# List all tags
git tag -l

# If you need to replace a tag (not recommended)
git tag -d v0.2.0
git push origin :refs/tags/v0.2.0
# Then create new release
```

## Best Practices

1. **Always run dry-run first** to preview changes
2. **Review generated release notes** before confirming
3. **Test the application** before releasing
4. **Keep CHANGELOG.md updated** throughout development
5. **Use meaningful commit messages** for better release notes
6. **Release from main branch** (or your designated release branch)
7. **Ensure CI/CD passes** before releasing (if configured)
8. **Announce releases** to users/stakeholders

## Version History

Track versions in CHANGELOG.md and Git tags:

```bash
# View all releases
git tag -l

# View specific release notes
git show v0.2.0

# View GitHub releases
gh release list
```

## Additional Resources

- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [Git Tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging)
