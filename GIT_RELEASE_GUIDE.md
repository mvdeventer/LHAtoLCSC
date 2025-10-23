# Git Release Management Scripts

This directory contains comprehensive Git release management tools for the LHAtoLCSC project.

## 📁 **Available Scripts**

### 1. **`git_release.py`** - Python Release Manager
Full-featured Python script with comprehensive Git operations and GitHub integration.

### 2. **`git_release.ps1`** - PowerShell Release Manager  
Windows-optimized PowerShell script with colored output and robust error handling.

### 3. **`git_release.bat`** - Batch Wrapper
Simple batch file for easy command-line access to PowerShell script.

## 🚀 **Quick Start Examples**

### **Basic Usage (Recommended)**
```bash
# Patch release (0.2.3 → 0.2.4)
.\git_release.bat patch "Fixed pagination duplicate pages" --commit-all --push

# Minor release (0.2.4 → 0.3.0)  
.\git_release.bat minor "Added currency persistence feature" --create-release

# Major release (0.3.0 → 1.0.0)
.\git_release.bat major "Complete UI redesign" --commit-all --push --create-release

# Specific version
.\git_release.bat version 0.2.5 "Hotfix for critical bug" --push
```

### **PowerShell Direct Usage**
```powershell
# Patch release with all features
.\git_release.ps1 -Bump patch -Message "Bug fixes" -CommitAll -Push -CreateRelease

# Dry run to preview changes
.\git_release.ps1 -Bump minor -Message "New features" -DryRun

# Force overwrite existing tag
.\git_release.ps1 -Version "0.2.4" -Message "Re-release" -Force
```

### **Python Script Usage**
```bash
# Full release with GitHub integration
python git_release.py --bump patch --message "Enhanced pagination" --commit-all --push --create-release

# Dry run preview
python git_release.py --version 0.3.0 --message "Major update" --dry-run
```

## 📖 **Detailed Command Reference**

### **Version Parameters**
- **`--bump patch`** / **`patch`**: Increment patch version (0.2.3 → 0.2.4)
- **`--bump minor`** / **`minor`**: Increment minor version (0.2.3 → 0.3.0)  
- **`--bump major`** / **`major`**: Increment major version (0.2.3 → 1.0.0)
- **`--version X.Y.Z`** / **`version X.Y.Z`**: Set specific version

### **Required Parameters**
- **`--message "text"`** / **`"message"`**: Release description/message

### **Optional Flags**
- **`--commit-all`** / **`--CommitAll`**: Commit all changed files (not just version)
- **`--push`** / **`-Push`**: Push commits and tags to remote repository
- **`--create-release`** / **`-CreateRelease`**: Create GitHub release (requires `gh` CLI)
- **`--dry-run`** / **`-DryRun`**: Preview operations without making changes
- **`--force`** / **`-Force`**: Force operations (overwrite existing tags)
- **`--tag-prefix`** / **`-TagPrefix`**: Custom tag prefix (default: "v")

## 🔄 **Release Workflow**

### **Standard Release Process**
1. **Prepare Code**: Ensure all changes are ready
2. **Run Tests**: Verify functionality works
3. **Choose Version**: Decide on patch/minor/major bump
4. **Execute Release**: Run release script with appropriate options
5. **Verify Results**: Check Git tags and GitHub release

### **What the Scripts Do**
1. ✅ **Validate Git Status**: Check repository state and uncommitted changes
2. ✅ **Update Version**: Modify `pyproject.toml` with new version number
3. ✅ **Create Commit**: Commit version changes and optionally other files
4. ✅ **Create Git Tag**: Tag the release with version and message
5. ✅ **Push Changes**: Push commits and tags to remote repository
6. ✅ **GitHub Release**: Create GitHub release with installer (if available)

## 📋 **Examples for Different Scenarios**

### **Bug Fix Release (Patch)**
```bash
# Fix critical pagination bug
.\git_release.bat patch "Fixed pagination duplicate page numbers" --commit-all --push

# Result: 0.2.3 → 0.2.4
```

### **Feature Release (Minor)**
```bash
# Add currency persistence
.\git_release.bat minor "Added persistent currency selection" --create-release

# Result: 0.2.4 → 0.3.0
```

### **Breaking Changes (Major)**
```bash
# Major UI overhaul
.\git_release.bat major "Complete interface redesign" --commit-all --push --create-release

# Result: 0.3.0 → 1.0.0
```

### **Hotfix Release**
```bash
# Emergency fix
.\git_release.bat version 0.2.3.1 "Critical security hotfix" --push

# Result: 0.2.3 → 0.2.3.1
```

### **Preview Changes (Dry Run)**
```bash
# See what would happen without making changes
.\git_release.bat minor "Planned feature release" --dry-run --commit-all --push
```

## 🛡️ **Safety Features**

### **Built-in Protections**
- ✅ **Git Repository Check**: Ensures you're in a valid Git repository
- ✅ **Uncommitted Changes Warning**: Alerts about pending changes
- ✅ **Tag Conflict Prevention**: Prevents overwriting existing tags (unless forced)
- ✅ **Dry Run Mode**: Preview operations without making changes
- ✅ **Error Handling**: Comprehensive error messages and rollback

### **Pre-Release Checklist**
- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No uncommitted critical changes
- [ ] Ready for production

## 🔧 **Configuration**

### **Version File Location**
The scripts automatically read/write version from:
- **`pyproject.toml`** - Primary version source

### **Release Notes Template**
Auto-generated release notes include:
- Release version and date
- User-provided message
- Recent enhancements summary
- Technical improvements list
- Bug fixes overview

### **GitHub Integration Requirements**
For `--create-release` functionality:
- **GitHub CLI** (`gh`) must be installed
- **Authentication** set up with GitHub
- **Repository** must be on GitHub

## 🐛 **Troubleshooting**

### **Common Issues**

**"Tag already exists"**
```bash
# Use --force to overwrite
.\git_release.bat patch "Fixed bug" --force
```

**"Uncommitted changes found"**
```bash
# Include all changes in release commit
.\git_release.bat patch "Bug fixes" --commit-all
```

**"GitHub CLI not available"**
```bash
# Install GitHub CLI or skip GitHub release creation
# Script will continue with Git operations only
```

**"Not in a Git repository"**
```bash
# Ensure you're in the project root directory
cd C:\Projects\LCSC_API
.\git_release.bat patch "Release"
```

### **Recovery from Failed Release**
```bash
# Delete local tag if needed
git tag -d v0.2.4

# Reset version file manually if needed
# Edit pyproject.toml to correct version

# Re-run release script
.\git_release.bat patch "Fixed release" --force
```

## 📊 **Release History Tracking**

### **Git Tags Created**
Each release creates a Git tag with format: `v{version}`
- Example: `v0.2.4`, `v0.3.0`, `v1.0.0`

### **Commit Messages**
Standardized commit message format:
- **Format**: `Release {version}: {message}`
- **Example**: `Release 0.2.4: Fixed pagination duplicate pages`

### **GitHub Releases**
Automated GitHub releases include:
- **Title**: `LHAtoLCSC {version}`
- **Description**: Generated release notes with enhancements
- **Assets**: Windows installer (if available)

## 🎯 **Best Practices**

### **Version Numbering**
- **Patch** (0.2.3 → 0.2.4): Bug fixes, small improvements
- **Minor** (0.2.4 → 0.3.0): New features, backward compatible
- **Major** (0.3.0 → 1.0.0): Breaking changes, major milestones

### **Release Messages**
- ✅ **Good**: "Fixed pagination duplicate page numbers"
- ✅ **Good**: "Added persistent currency selection feature"
- ❌ **Avoid**: "Updates", "Changes", "Fixes"

### **Testing Before Release**
```bash
# Always test with dry run first
.\git_release.bat minor "New feature" --dry-run

# Then execute actual release
.\git_release.bat minor "New feature" --commit-all --push
```

---

## 📝 **Summary**

These Git release scripts provide a complete, automated solution for:
- ✅ **Version Management**: Automatic semantic versioning
- ✅ **Git Operations**: Commits, tags, and pushing
- ✅ **GitHub Integration**: Automated release creation
- ✅ **Safety Checks**: Validation and error prevention
- ✅ **Flexibility**: Multiple interfaces (Python, PowerShell, Batch)

**Ready to create your next release!** 🚀

```bash
# Start with a simple patch release
.\git_release.bat patch "Your release message here" --commit-all --push
```