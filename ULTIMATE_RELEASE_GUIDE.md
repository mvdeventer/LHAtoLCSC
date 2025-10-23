# Ultimate Release Script Documentation

The `ultimate_release.py` script provides comprehensive GitHub release automation with all the bells and whistles. This script replaces all existing release scripts (`release.py`, `release_workflow.py`, `release.bat`) with a single, powerful solution.

## Features

### 🚀 **Automatic Version Management**
- Queries GitHub API to detect existing releases
- Automatically calculates next version (patch, minor, major)
- Updates version in multiple files simultaneously:
  - `src/lhatolcsc/core/config.py`
  - `pyproject.toml`
  - `setup.py`

### 🔍 **GitHub Integration**
- GitHub API integration for release detection
- Automatic release notes generation from git commits
- GitHub Actions workflow triggering
- Release asset verification and monitoring

### 📝 **Documentation**
- Automatic CHANGELOG.md updates
- Categorized release notes (Features, Bug Fixes, Other Changes)
- Professional release descriptions with installation instructions

### 🛡️ **Safety Features**
- Dry-run mode for previewing changes
- Rollback capabilities on failure
- Working directory cleanliness checks
- Existing tag detection and protection

### 📊 **Enhanced Logging**
- Beautiful colored terminal output
- Comprehensive logging to `release.log`
- Step-by-step progress tracking
- Timestamp and category-based logging

## Installation

### Prerequisites

Install required Python packages:
```bash
pip install pygithub gitpython
```

### GitHub Authentication

Set up GitHub authentication using one of these methods:

1. **Environment Variable (Recommended)**:
   ```bash
   export GITHUB_TOKEN="your_github_token_here"
   ```

2. **Git Config**:
   ```bash
   git config --global github.token "your_github_token_here"
   ```

3. **GitHub CLI** (if installed):
   ```bash
   gh auth login
   ```

### GitHub Token Setup

1. Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select these scopes:
   - `repo` (Full control of private repositories)
   - `workflow` (Update GitHub Actions workflows)
4. Copy the token and set it using one of the methods above

## Usage

### Basic Usage

```bash
# Patch release (0.1.0 → 0.1.1)
python ultimate_release.py patch

# Minor release (0.1.0 → 0.2.0)
python ultimate_release.py minor

# Major release (0.1.0 → 1.0.0)
python ultimate_release.py major
```

### Advanced Options

```bash
# Preview changes without making them
python ultimate_release.py patch --dry-run

# Force release even with dirty working directory
python ultimate_release.py minor --force

# Don't wait for GitHub Actions to complete
python ultimate_release.py patch --no-wait

# Use custom GitHub token
python ultimate_release.py patch --github-token "your_token"
```

## Release Process

The script performs these steps automatically:

### 1. 🔍 **Version Detection**
- Queries GitHub API for latest release
- Reads current version from `config.py`
- Calculates next version based on bump type

### 2. 🛡️ **Safety Checks**
- Verifies working directory is clean
- Checks for existing tags
- Validates GitHub authentication

### 3. 📝 **Version Updates**
- Updates version in all relevant files
- Maintains backup for rollback if needed

### 4. 📰 **Release Notes**
- Generates release notes from git commits
- Categorizes changes (Features, Bug Fixes, Other)
- Updates CHANGELOG.md with new entry

### 5. 🏷️ **Git Operations**
- Commits all changes
- Creates git tag
- Pushes to origin with tags

### 6. 🚀 **GitHub Actions**
- Pushes tag triggers GitHub Actions workflow
- Monitors workflow completion
- Waits for installer builds to complete

### 7. 📦 **GitHub Release**
- Creates GitHub release with generated notes
- Includes professional installation instructions
- Links to documentation and requirements

### 8. ✅ **Verification**
- Verifies release assets are uploaded
- Confirms workflow completion
- Provides release URL

## Configuration

### GitHub Actions Integration

The script works with the existing `.github/workflows/release.yml` workflow:

- **Trigger**: Push to tags matching `v*.*.*`
- **Builds**: Windows installer and portable ZIP
- **Uploads**: All build artifacts to the GitHub release

### File Structure

The script manages versions in these files:
```
src/lhatolcsc/core/config.py     # self.version = "x.y.z"
pyproject.toml                   # version = "x.y.z"
setup.py                         # version="x.y.z"
```

### Release Notes Categories

Commits are automatically categorized:

- **Features**: `feat:`, `feature:`, `add:`, `new:`
- **Bug Fixes**: `fix:`, `bug:`, `hotfix:`, `patch:`
- **Other Changes**: Everything else

## Examples

### Example 1: Patch Release
```bash
$ python ultimate_release.py patch

================================================================================
                           Starting PATCH Release Process
================================================================================

[2024-01-15 10:30:00] INFO: ℹ Latest release: v0.2.6
[2024-01-15 10:30:01] INFO: ℹ Basing next version on latest release: 0.2.6 → 0.2.7
[2024-01-15 10:30:01] INFO: ℹ Target version: 0.2.7
[2024-01-15 10:30:01] STEP: → Updating version to 0.2.7
[2024-01-15 10:30:01] SUCCESS: ✓ Updated config.py
[2024-01-15 10:30:01] SUCCESS: ✓ Updated pyproject.toml
[2024-01-15 10:30:01] STEP: → Generating release notes from git history
[2024-01-15 10:30:02] SUCCESS: ✓ Generated release notes (3 commits)
[2024-01-15 10:30:02] STEP: → Updating CHANGELOG.md
[2024-01-15 10:30:02] SUCCESS: ✓ Updated CHANGELOG.md
[2024-01-15 10:30:02] STEP: → Committing changes and creating tag v0.2.7
[2024-01-15 10:30:03] SUCCESS: ✓ Committed: Release v0.2.7
[2024-01-15 10:30:03] SUCCESS: ✓ Created tag: v0.2.7
[2024-01-15 10:30:05] SUCCESS: ✓ Pushed to origin with tags
[2024-01-15 10:30:05] STEP: → Creating GitHub release v0.2.7
[2024-01-15 10:30:05] STEP: → Waiting for GitHub Actions workflow to complete
[2024-01-15 10:30:35] INFO: ℹ Found workflow run: https://github.com/mvdeventer/LHAtoLCSC/actions/runs/123456
[2024-01-15 10:32:15] SUCCESS: ✓ Workflow completed successfully!
[2024-01-15 10:32:16] SUCCESS: ✓ Created release: https://github.com/mvdeventer/LHAtoLCSC/releases/tag/v0.2.7
[2024-01-15 10:32:16] STEP: → Verifying release assets...
[2024-01-15 10:32:46] SUCCESS: ✓ Found 4 release assets:
[2024-01-15 10:32:46] INFO: ℹ   • LHAtoLCSC-0.2.7-Setup.exe (15234567 bytes)
[2024-01-15 10:32:46] INFO: ℹ   • LHAtoLCSC-0.2.7-Portable.zip (12345678 bytes)
[2024-01-15 10:32:46] INFO: ℹ   • lhatolcsc-0.2.7-py3-none-any.whl (123456 bytes)
[2024-01-15 10:32:46] INFO: ℹ   • lhatolcsc-0.2.7.tar.gz (234567 bytes)

================================================================================
                                🎉 Release Complete!
================================================================================

[2024-01-15 10:32:46] SUCCESS: ✓ Successfully released v0.2.7
[2024-01-15 10:32:46] INFO: ℹ Release URL: https://github.com/mvdeventer/LHAtoLCSC/releases/tag/v0.2.7
```

### Example 2: Dry Run
```bash
$ python ultimate_release.py minor --dry-run

[2024-01-15 10:35:00] WARNING: ⚠ DRY RUN MODE - No changes will be made
[2024-01-15 10:35:01] INFO: ℹ Target version: 0.3.0
[2024-01-15 10:35:01] INFO: ℹ DRY RUN: Would commit and tag
[2024-01-15 10:35:01] INFO: ℹ DRY RUN: Would create GitHub release
```

## Troubleshooting

### Common Issues

1. **"GitHub token not found"**
   - Solution: Set up GitHub authentication (see Installation section)

2. **"Working directory is dirty"**
   - Solution: Commit your changes first, or use `--force`

3. **"Tag already exists"**
   - Solution: Use `--force` to override, or choose different bump type

4. **"Workflow didn't complete successfully"**
   - Check GitHub Actions tab for build errors
   - The release will still be created, but without assets

### Debug Information

Check the `release.log` file for detailed logging information:
```bash
tail -f release.log
```

### GitHub Actions Issues

If the workflow fails:
1. Check the [Actions tab](https://github.com/mvdeventer/LHAtoLCSC/actions)
2. Review build logs for errors
3. The release will be created but may lack build artifacts
4. You can manually trigger the workflow or upload assets

## Migration from Old Scripts

### Removing Old Scripts

After verifying the ultimate release script works, you can remove:
- `release.py`
- `release_workflow.py`
- `release.bat`
- `build_installer.py` (functionality integrated)

### Key Differences

| Feature | Old Scripts | Ultimate Script |
|---------|-------------|-----------------|
| Version Detection | Manual/config only | GitHub API + config |
| Release Notes | Manual | Auto-generated from commits |
| Asset Handling | Manual upload | Automatic via Actions |
| Error Handling | Basic | Comprehensive with rollback |
| Logging | Minimal | Professional with colors |
| Dry Run | Not available | Full preview mode |

## Contributing

To improve the release script:

1. Test changes with `--dry-run` first
2. Update this documentation for new features
3. Follow the existing logging patterns
4. Add appropriate error handling

## Security

- Store GitHub tokens securely (use environment variables)
- Never commit tokens to the repository
- Use the minimum required token permissions
- Regularly rotate your GitHub tokens

## Support

For issues with the release script:
1. Check the troubleshooting section
2. Review `release.log` for details
3. Test with `--dry-run` to isolate issues
4. Check GitHub Actions workflow status
