# Git Release Script for LHAtoLCSC
# PowerShell version for Windows compatibility
#
# This script automates Git operations for creating releases:
# 1. Validates current Git status
# 2. Commits pending changes
# 3. Creates and pushes Git tags
# 4. Handles version bumping
# 5. Manages release notes
# 6. Optional GitHub release creation
#
# Usage:
#   .\git_release.ps1 -Version "0.2.4" -Message "Enhanced pagination and currency persistence"
#   .\git_release.ps1 -Bump "patch" -Message "Bug fixes"
#   .\git_release.ps1 -Bump "minor" -Message "New features"
#   .\git_release.ps1 -Bump "major" -Message "Breaking changes"
#
# Examples:
#   .\git_release.ps1 -Bump patch -Message "Fixed pagination duplicate pages" -CommitAll -Push
#   .\git_release.ps1 -Version "0.3.0" -Message "Currency persistence feature" -CreateRelease
#   .\git_release.ps1 -Bump minor -Message "Enhanced UI" -DryRun

param(
    [Parameter(ParameterSetName = "SpecificVersion")]
    [string]$Version,
    
    [Parameter(ParameterSetName = "BumpVersion")]
    [ValidateSet("patch", "minor", "major")]
    [string]$Bump,
    
    [Parameter(Mandatory = $true)]
    [string]$Message,
    
    [string]$TagPrefix = "v",
    [switch]$CommitAll,
    [switch]$Push,
    [switch]$CreateRelease,
    [switch]$DryRun,
    [switch]$Force
)

# Color functions for better output
function Write-ColorText {
    param(
        [string]$Text,
        [ValidateSet("Info", "Success", "Warning", "Error", "Header")]
        [string]$Type = "Info"
    )
    
    $colors = @{
        "Info"    = "Cyan"
        "Success" = "Green"
        "Warning" = "Yellow"
        "Error"   = "Red"
        "Header"  = "Magenta"
    }
    
    $prefix = if ($DryRun) { "DRY RUN: " } else { "" }
    Write-Host "[$Type] $prefix$Text" -ForegroundColor $colors[$Type]
}

# Function to run commands with dry-run support
function Invoke-GitCommand {
    param(
        [string[]]$Command,
        [switch]$Capture
    )
    
    $cmdString = $Command -join " "
    
    if ($DryRun) {
        Write-ColorText "Would run: $cmdString" "Info"
        return @{ Success = $true; Output = ""; Error = "" }
    }
    
    Write-ColorText "Running: $cmdString" "Info"
    
    try {
        if ($Capture) {
            $result = & $Command[0] $Command[1..($Command.Length-1)] 2>&1
            if ($LASTEXITCODE -eq 0) {
                return @{ Success = $true; Output = $result -join "`n"; Error = "" }
            } else {
                throw "Command failed with exit code $LASTEXITCODE"
            }
        } else {
            & $Command[0] $Command[1..($Command.Length-1)]
            if ($LASTEXITCODE -ne 0) {
                throw "Command failed with exit code $LASTEXITCODE"
            }
            return @{ Success = $true; Output = ""; Error = "" }
        }
    }
    catch {
        Write-ColorText "Command failed: $cmdString" "Error"
        Write-ColorText "Error: $($_.Exception.Message)" "Error"
        throw
    }
}

# Function to get current version from pyproject.toml
function Get-CurrentVersion {
    $pyprojectPath = Join-Path $PSScriptRoot "pyproject.toml"
    
    if (-not (Test-Path $pyprojectPath)) {
        throw "pyproject.toml not found"
    }
    
    $content = Get-Content $pyprojectPath -Raw
    
    if ($content -match 'version\s*=\s*["\''"]([^"\''""]+)["\''"]') {
        return $Matches[1]
    }
    
    throw "Version not found in pyproject.toml"
}

# Function to bump version according to semantic versioning
function Get-BumpedVersion {
    param(
        [string]$CurrentVersion,
        [string]$BumpType
    )
    
    $versionParts = $CurrentVersion.Split('.')
    
    if ($versionParts.Count -ne 3) {
        throw "Invalid version format: $CurrentVersion"
    }
    
    $major = [int]$versionParts[0]
    $minor = [int]$versionParts[1]
    $patch = [int]$versionParts[2]
    
    switch ($BumpType) {
        "major" {
            $major++
            $minor = 0
            $patch = 0
        }
        "minor" {
            $minor++
            $patch = 0
        }
        "patch" {
            $patch++
        }
        default {
            throw "Invalid bump type: $BumpType"
        }
    }
    
    return "$major.$minor.$patch"
}

# Function to update version in pyproject.toml
function Update-VersionFile {
    param([string]$NewVersion)
    
    $pyprojectPath = Join-Path $PSScriptRoot "pyproject.toml"
    
    if ($DryRun) {
        Write-ColorText "Would update pyproject.toml version to $NewVersion" "Info"
        return
    }
    
    $content = Get-Content $pyprojectPath -Raw
    $newContent = $content -replace '(version\s*=\s*["\''"])[^"\''""]+(["\''"])', "`$1$NewVersion`$2"
    
    Set-Content $pyprojectPath $newContent -Encoding UTF8
    Write-ColorText "Updated pyproject.toml version to $NewVersion" "Success"
}

# Function to check Git status
function Test-GitStatus {
    try {
        # Check if we're in a git repository
        Invoke-GitCommand @("git", "rev-parse", "--git-dir") -Capture | Out-Null
        
        # Check for uncommitted changes
        $result = Invoke-GitCommand @("git", "status", "--porcelain") -Capture
        $changedFiles = ($result.Output -split "`n") | Where-Object { $_.Trim() -ne "" }
        
        return @{
            HasChanges = $changedFiles.Count -gt 0
            ChangedFiles = $changedFiles
        }
    }
    catch {
        throw "Not in a Git repository or Git not available"
    }
}

# Function to get current Git branch
function Get-CurrentBranch {
    $result = Invoke-GitCommand @("git", "branch", "--show-current") -Capture
    return $result.Output.Trim()
}

# Function to check if a Git tag exists
function Test-TagExists {
    param([string]$Tag)
    
    try {
        Invoke-GitCommand @("git", "rev-parse", "refs/tags/$Tag") -Capture | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Function to create a Git commit
function New-GitCommit {
    param(
        [string]$CommitMessage,
        [string[]]$Files = @()
    )
    
    if ($Files.Count -gt 0) {
        # Add specific files
        foreach ($file in $Files) {
            Invoke-GitCommand @("git", "add", $file)
        }
    } else {
        # Add all changes
        Invoke-GitCommand @("git", "add", ".")
    }
    
    # Check if there's anything to commit
    try {
        $result = Invoke-GitCommand @("git", "diff", "--cached", "--quiet") -Capture
        if ($result.Success) {
            Write-ColorText "No changes to commit" "Warning"
            return $false
        }
    }
    catch {
        # Continue with commit - there are changes
    }
    
    # Create commit
    Invoke-GitCommand @("git", "commit", "-m", $CommitMessage)
    Write-ColorText "Created commit: $CommitMessage" "Success"
    return $true
}

# Function to create a Git tag
function New-GitTag {
    param(
        [string]$Tag,
        [string]$TagMessage
    )
    
    if ((Test-TagExists $Tag) -and -not $Force) {
        throw "Tag $Tag already exists. Use -Force to overwrite."
    }
    
    if ((Test-TagExists $Tag) -and $Force) {
        Write-ColorText "Deleting existing tag: $Tag" "Warning"
        Invoke-GitCommand @("git", "tag", "-d", $Tag)
    }
    
    Invoke-GitCommand @("git", "tag", "-a", $Tag, "-m", $TagMessage)
    Write-ColorText "Created tag: $Tag" "Success"
}

# Function to push changes and tags to remote
function Push-GitChanges {
    param([string]$Tag)
    
    # Push commits
    Invoke-GitCommand @("git", "push")
    Write-ColorText "Pushed commits to remote" "Success"
    
    # Push tag if specified
    if ($Tag) {
        Invoke-GitCommand @("git", "push", "origin", $Tag)
        Write-ColorText "Pushed tag $Tag to remote" "Success"
    }
}

# Function to create GitHub release using gh CLI
function New-GitHubRelease {
    param(
        [string]$Tag,
        [string]$Title,
        [string]$ReleaseMessage
    )
    
    # Check if gh CLI is available
    try {
        Invoke-GitCommand @("gh", "--version") -Capture | Out-Null
    }
    catch {
        Write-ColorText "GitHub CLI (gh) not available. Skipping GitHub release creation." "Warning"
        return
    }
    
    # Create release
    $cmd = @("gh", "release", "create", $Tag, "--title", $Title, "--notes", $ReleaseMessage)
    
    # Check for installer file
    $installerPath = Join-Path $PSScriptRoot "dist\LHAtoLCSC-Setup.exe"
    if (Test-Path $installerPath) {
        $cmd += $installerPath
        Write-ColorText "Adding installer to GitHub release" "Info"
    }
    
    Invoke-GitCommand $cmd
    Write-ColorText "Created GitHub release: $Tag" "Success"
}

# Function to generate release notes
function New-ReleaseNotes {
    param(
        [string]$ReleaseVersion,
        [string]$ReleaseMessage
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd"
    
    return @"
# Release $ReleaseVersion - $timestamp

## $ReleaseMessage

### Recent Enhancements
- Enhanced pagination with web-style page number buttons (1-5)
- Persistent currency selection between app restarts
- Dynamic button width for large page numbers (fixed truncation)
- Improved search history management
- Better error handling and logging

### Technical Improvements
- Fixed pagination duplicate page numbers issue
- Enhanced widget cleanup in UI components  
- Added comprehensive currency preferences system
- Improved virtual environment automation scripts

### Bug Fixes
- Resolved button width truncation for large datasets
- Fixed lambda closure issues in pagination
- Enhanced widget destruction and cleanup

---
**Full Changelog**: Compare with previous version for detailed changes
"@
}

# Main script execution
try {
    Write-ColorText "Starting Git release process for LHAtoLCSC" "Header"
    
    # Validate parameters
    if (-not $Version -and -not $Bump) {
        throw "Either -Version or -Bump parameter is required"
    }
    
    # Check Git status
    $gitStatus = Test-GitStatus
    $currentBranch = Get-CurrentBranch
    
    Write-ColorText "Current branch: $currentBranch" "Info"
    
    if ($gitStatus.HasChanges) {
        $fileCount = $gitStatus.ChangedFiles.Count
        Write-ColorText "Found $fileCount changed files:" "Warning"
        $gitStatus.ChangedFiles[0..9] | ForEach-Object { Write-ColorText "  $_" "Info" }
        if ($fileCount -gt 10) {
            Write-ColorText "  ... and $($fileCount - 10) more" "Info"
        }
    }
    
    # Determine version
    $currentVersion = Get-CurrentVersion
    Write-ColorText "Current version: $currentVersion" "Info"
    
    if ($Version) {
        $newVersion = $Version
    } else {
        $newVersion = Get-BumpedVersion $currentVersion $Bump
    }
    
    Write-ColorText "Target version: $newVersion" "Info"
    
    # Update version file if needed
    $hasChanges = $gitStatus.HasChanges
    if ($newVersion -ne $currentVersion) {
        Update-VersionFile $newVersion
        $hasChanges = $true  # Now we have version file changes
    }
    
    # Commit changes if requested
    if ($hasChanges -and ($CommitAll -or ($newVersion -ne $currentVersion))) {
        $commitMessage = "Release $newVersion`: $Message"
        $filesToCommit = if (-not $CommitAll) { @("pyproject.toml") } else { @() }
        New-GitCommit $commitMessage $filesToCommit | Out-Null
    } elseif ($hasChanges -and -not $CommitAll) {
        Write-ColorText "Uncommitted changes found. Use -CommitAll to include them." "Warning"
    }
    
    # Create tag
    $tag = "$TagPrefix$newVersion"
    $tagMessage = "Release $newVersion`: $Message"
    New-GitTag $tag $tagMessage
    
    # Push if requested
    if ($Push) {
        Push-GitChanges $tag
    }
    
    # Create GitHub release if requested
    if ($CreateRelease) {
        $releaseTitle = "LHAtoLCSC $newVersion"
        $releaseNotes = New-ReleaseNotes $newVersion $Message
        New-GitHubRelease $tag $releaseTitle $releaseNotes
    }
    
    Write-ColorText "Release process completed successfully!" "Success"
    Write-ColorText "Created release: $tag" "Success"
    
    if (-not $Push) {
        Write-ColorText "Remember to push your changes: git push && git push origin $tag" "Info"
    }
    
    if (-not $CreateRelease) {
        Write-ColorText "To create GitHub release: .\git_release.ps1 -CreateRelease" "Info"
    }
    
} catch {
    Write-ColorText "Release process failed: $($_.Exception.Message)" "Error"
    exit 1
}