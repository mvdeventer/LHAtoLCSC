"""
GitHub Release Script for LHAtoLCSC

Automates the release process including:
- Version detection and increment
- Git commit, tag, and push
- GitHub release creation with release notes
- Changelog generation
"""

import subprocess
import sys
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple, List
import argparse


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")


def print_success(text: str):
    """Print success message."""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_error(text: str):
    """Print error message."""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_warning(text: str):
    """Print warning message."""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


def print_info(text: str):
    """Print info message."""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")


def run_command(cmd: List[str], capture_output: bool = True, check: bool = True) -> subprocess.CompletedProcess:
    """
    Run a shell command and return the result.
    
    Args:
        cmd: Command and arguments as list
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        
    Returns:
        CompletedProcess object
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture_output,
            text=True,
            check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {' '.join(cmd)}")
        print_error(f"Error: {e.stderr}")
        raise
    except FileNotFoundError:
        print_error(f"Command not found: {cmd[0]}")
        print_error("Make sure Git and GitHub CLI (gh) are installed and in PATH")
        raise


def check_git_installed() -> bool:
    """Check if git is installed."""
    try:
        run_command(["git", "--version"], capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_gh_installed() -> bool:
    """Check if GitHub CLI is installed."""
    try:
        run_command(["gh", "--version"], capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_gh_authenticated() -> bool:
    """Check if GitHub CLI is authenticated."""
    try:
        result = run_command(["gh", "auth", "status"], capture_output=True, check=False)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def get_current_branch() -> str:
    """Get the current git branch."""
    result = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    return result.stdout.strip()


def check_clean_working_directory() -> bool:
    """Check if the working directory is clean."""
    result = run_command(["git", "status", "--porcelain"])
    return len(result.stdout.strip()) == 0


def get_latest_tag() -> Optional[str]:
    """Get the latest git tag following semantic versioning."""
    try:
        result = run_command(["git", "tag", "--sort=-v:refname"], check=False)
        tags = result.stdout.strip().split('\n')
        
        # Filter tags that match semantic versioning pattern
        version_pattern = re.compile(r'^v?\d+\.\d+\.\d+$')
        for tag in tags:
            if tag and version_pattern.match(tag):
                return tag
        
        return None
    except subprocess.CalledProcessError:
        return None


def parse_version(version_string: str) -> Tuple[int, int, int]:
    """
    Parse a version string into major, minor, patch numbers.
    
    Args:
        version_string: Version string (e.g., "v1.2.3" or "1.2.3")
        
    Returns:
        Tuple of (major, minor, patch)
    """
    # Remove 'v' prefix if present
    version_string = version_string.lstrip('v')
    
    # Parse version numbers
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)$', version_string)
    if not match:
        raise ValueError(f"Invalid version format: {version_string}")
    
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def increment_version(version: str, bump_type: str) -> str:
    """
    Increment version based on bump type.
    
    Args:
        version: Current version string
        bump_type: One of 'major', 'minor', 'patch'
        
    Returns:
        New version string
    """
    major, minor, patch = parse_version(version)
    
    if bump_type == 'major':
        return f"{major + 1}.0.0"
    elif bump_type == 'minor':
        return f"{major}.{minor + 1}.0"
    elif bump_type == 'patch':
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")


def get_next_version(bump_type: str) -> str:
    """
    Determine the next version based on the latest tag and bump type.
    
    Args:
        bump_type: One of 'major', 'minor', 'patch'
        
    Returns:
        Next version string
    """
    latest_tag = get_latest_tag()
    
    if latest_tag is None:
        print_info("No existing tags found. Starting with version 0.1.0")
        return "0.1.0"
    
    print_info(f"Latest tag: {latest_tag}")
    return increment_version(latest_tag, bump_type)


def get_commits_since_tag(tag: Optional[str]) -> List[str]:
    """
    Get commit messages since the specified tag.
    
    Args:
        tag: Git tag to compare from (None for all commits)
        
    Returns:
        List of commit messages
    """
    if tag:
        cmd = ["git", "log", f"{tag}..HEAD", "--pretty=format:%s"]
    else:
        cmd = ["git", "log", "--pretty=format:%s"]
    
    result = run_command(cmd, check=False)
    
    if result.returncode != 0 or not result.stdout.strip():
        return []
    
    return result.stdout.strip().split('\n')


def categorize_commits(commits: List[str]) -> dict:
    """
    Categorize commits into features, fixes, and other changes.
    
    Args:
        commits: List of commit messages
        
    Returns:
        Dictionary with categorized commits
    """
    categories = {
        'features': [],
        'fixes': [],
        'improvements': [],
        'docs': [],
        'other': []
    }
    
    for commit in commits:
        commit_lower = commit.lower()
        
        if any(keyword in commit_lower for keyword in ['feat:', 'feature:', 'add:', 'added']):
            categories['features'].append(commit)
        elif any(keyword in commit_lower for keyword in ['fix:', 'fixed', 'bug:', 'bugfix']):
            categories['fixes'].append(commit)
        elif any(keyword in commit_lower for keyword in ['improve:', 'improved', 'enhancement:', 'update:', 'updated']):
            categories['improvements'].append(commit)
        elif any(keyword in commit_lower for keyword in ['doc:', 'docs:', 'documentation']):
            categories['docs'].append(commit)
        else:
            categories['other'].append(commit)
    
    return categories


def generate_release_notes(version: str, commits: List[str]) -> str:
    """
    Generate release notes from commit messages.
    
    Args:
        version: Version being released
        commits: List of commit messages
        
    Returns:
        Formatted release notes
    """
    release_date = datetime.now().strftime("%Y-%m-%d")
    
    notes = f"# Release v{version}\n\n"
    notes += f"**Release Date:** {release_date}\n\n"
    
    if not commits:
        notes += "Initial release of LHAtoLCSC - LCSC API Integration Tool\n\n"
        notes += "## Features\n\n"
        notes += "- 🔧 Professional Tkinter-based GUI for component management\n"
        notes += "- 🔌 Full LCSC API integration with authentication\n"
        notes += "- 🧪 Mock API server with 104,000+ components for testing\n"
        notes += "- ⚙️ Settings wizard with mock server credentials button\n"
        notes += "- 📦 Component search and management functionality\n"
        notes += "- 🔐 Secure API credential storage\n"
        return notes
    
    categories = categorize_commits(commits)
    
    # Features
    if categories['features']:
        notes += "## ✨ New Features\n\n"
        for commit in categories['features']:
            notes += f"- {commit}\n"
        notes += "\n"
    
    # Bug Fixes
    if categories['fixes']:
        notes += "## 🐛 Bug Fixes\n\n"
        for commit in categories['fixes']:
            notes += f"- {commit}\n"
        notes += "\n"
    
    # Improvements
    if categories['improvements']:
        notes += "## 🚀 Improvements\n\n"
        for commit in categories['improvements']:
            notes += f"- {commit}\n"
        notes += "\n"
    
    # Documentation
    if categories['docs']:
        notes += "## 📚 Documentation\n\n"
        for commit in categories['docs']:
            notes += f"- {commit}\n"
        notes += "\n"
    
    # Other changes
    if categories['other']:
        notes += "## 🔧 Other Changes\n\n"
        for commit in categories['other']:
            notes += f"- {commit}\n"
        notes += "\n"
    
    # Footer
    notes += "---\n\n"
    notes += "## 📋 Requirements\n\n"
    notes += "- Python 3.8 or higher\n"
    notes += "- tkinter (usually included with Python)\n"
    notes += "- Flask 3.1.2 (for mock server)\n\n"
    notes += "## 🚀 Installation\n\n"
    notes += "```bash\n"
    notes += "pip install -r requirements.txt\n"
    notes += "python main.py\n"
    notes += "```\n\n"
    notes += "## 🧪 Testing with Mock Server\n\n"
    notes += "```bash\n"
    notes += "python tests/mock_lcsc_server.py\n"
    notes += "```\n\n"
    notes += "Then use the **🧪 Use Mock Server Credentials** button in the settings dialog.\n"
    
    return notes


def update_version_in_files(version: str):
    """
    Update version number in relevant files.
    
    Args:
        version: New version string
    """
    # Update in config.py or __init__.py
    config_files = [
        Path("src/lhatolcsc/__init__.py"),
        Path("src/lhatolcsc/core/config.py"),
    ]
    
    for config_file in config_files:
        if config_file.exists():
            content = config_file.read_text()
            
            # Try different version patterns
            patterns = [
                (r'__version__\s*=\s*["\'][\d.]+["\']', f'__version__ = "{version}"'),
                (r'VERSION\s*=\s*["\'][\d.]+["\']', f'VERSION = "{version}"'),
                (r'version\s*=\s*["\'][\d.]+["\']', f'version = "{version}"'),
            ]
            
            updated = False
            for pattern, replacement in patterns:
                if re.search(pattern, content):
                    content = re.sub(pattern, replacement, content)
                    updated = True
            
            if updated:
                config_file.write_text(content)
                print_success(f"Updated version in {config_file}")


def create_changelog_entry(version: str, release_notes: str):
    """
    Add entry to CHANGELOG.md file.
    
    Args:
        version: Version being released
        release_notes: Generated release notes
    """
    changelog_path = Path("CHANGELOG.md")
    
    # Read existing changelog or create new one
    if changelog_path.exists():
        existing_content = changelog_path.read_text()
    else:
        existing_content = "# Changelog\n\nAll notable changes to this project will be documented in this file.\n\n"
    
    # Insert new version at the top (after the header)
    lines = existing_content.split('\n')
    header_end = 0
    for i, line in enumerate(lines):
        if line.startswith('## '):
            header_end = i
            break
    
    if header_end == 0:
        header_end = len(lines)
    
    # Prepare new entry
    new_entry = release_notes.replace('# Release', '##')
    
    # Insert new entry
    updated_content = '\n'.join(lines[:header_end]) + '\n\n' + new_entry + '\n\n' + '\n'.join(lines[header_end:])
    
    changelog_path.write_text(updated_content)
    print_success(f"Updated CHANGELOG.md")


def commit_and_tag(version: str, release_notes: str):
    """
    Commit changes and create a git tag.
    
    Args:
        version: Version to tag
        release_notes: Release notes for the tag message
    """
    # Stage all changes
    run_command(["git", "add", "."])
    
    # Commit
    commit_message = f"Release v{version}"
    run_command(["git", "commit", "-m", commit_message])
    print_success(f"Created commit: {commit_message}")
    
    # Create annotated tag
    tag_name = f"v{version}"
    tag_message = f"Release {tag_name}\n\n{release_notes[:500]}"  # Limit tag message length
    
    run_command(["git", "tag", "-a", tag_name, "-m", tag_message])
    print_success(f"Created tag: {tag_name}")


def push_to_remote(version: str):
    """
    Push commits and tags to remote repository.
    
    Args:
        version: Version being released
    """
    branch = get_current_branch()
    
    # Push commits
    run_command(["git", "push", "origin", branch])
    print_success(f"Pushed commits to origin/{branch}")
    
    # Push tags
    run_command(["git", "push", "origin", f"v{version}"])
    print_success(f"Pushed tag v{version}")


def create_github_release(version: str, release_notes: str, prerelease: bool = False):
    """
    Create a GitHub release using GitHub CLI.
    
    Args:
        version: Version being released
        release_notes: Release notes content
        prerelease: Whether this is a prerelease
    """
    tag_name = f"v{version}"
    
    # Save release notes to temporary file
    notes_file = Path("release_notes_temp.md")
    notes_file.write_text(release_notes)
    
    try:
        # Create release
        cmd = [
            "gh", "release", "create", tag_name,
            "--title", f"Release v{version}",
            "--notes-file", str(notes_file)
        ]
        
        if prerelease:
            cmd.append("--prerelease")
        
        run_command(cmd, capture_output=False)
        print_success(f"Created GitHub release: {tag_name}")
    finally:
        # Clean up temp file
        if notes_file.exists():
            notes_file.unlink()


def main():
    """Main release script execution."""
    parser = argparse.ArgumentParser(
        description="Release script for LHAtoLCSC",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python release.py patch           # Create a patch release (0.1.0 -> 0.1.1)
  python release.py minor           # Create a minor release (0.1.0 -> 0.2.0)
  python release.py major           # Create a major release (0.1.0 -> 1.0.0)
  python release.py patch --dry-run # Preview changes without executing
  python release.py minor --prerelease # Create a prerelease version
        """
    )
    
    parser.add_argument(
        'bump_type',
        choices=['major', 'minor', 'patch'],
        help='Type of version bump'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
    parser.add_argument(
        '--prerelease',
        action='store_true',
        help='Mark the release as a prerelease'
    )
    parser.add_argument(
        '--skip-push',
        action='store_true',
        help='Skip pushing to remote (for local testing)'
    )
    
    args = parser.parse_args()
    
    print_header("LHAtoLCSC Release Script")
    
    # Check prerequisites
    print_info("Checking prerequisites...")
    
    if not check_git_installed():
        print_error("Git is not installed or not in PATH")
        sys.exit(1)
    print_success("Git is installed")
    
    if not check_gh_installed():
        print_error("GitHub CLI (gh) is not installed or not in PATH")
        print_info("Install from: https://cli.github.com/")
        sys.exit(1)
    print_success("GitHub CLI is installed")
    
    if not check_gh_authenticated():
        print_error("GitHub CLI is not authenticated")
        print_info("Run: gh auth login")
        sys.exit(1)
    print_success("GitHub CLI is authenticated")
    
    # Check working directory
    print_info("\nChecking working directory...")
    branch = get_current_branch()
    print_info(f"Current branch: {branch}")
    
    if not check_clean_working_directory():
        print_error("Working directory is not clean. Please commit or stash changes first.")
        sys.exit(1)
    print_success("Working directory is clean")
    
    # Determine next version
    print_info("\nDetermining next version...")
    next_version = get_next_version(args.bump_type)
    print_success(f"Next version: v{next_version} ({args.bump_type} bump)")
    
    # Get commits since last tag
    latest_tag = get_latest_tag()
    commits = get_commits_since_tag(latest_tag)
    print_info(f"Found {len(commits)} commits since {latest_tag or 'beginning'}")
    
    # Generate release notes
    print_info("\nGenerating release notes...")
    release_notes = generate_release_notes(next_version, commits)
    
    # Show preview
    print_header("Release Preview")
    print(release_notes)
    print()
    
    # Dry run exit
    if args.dry_run:
        print_warning("Dry run complete. No changes were made.")
        sys.exit(0)
    
    # Confirmation
    print_warning(f"About to release version v{next_version}")
    response = input(f"{Colors.BOLD}Do you want to continue? (yes/no): {Colors.ENDC}").strip().lower()
    
    if response not in ['yes', 'y']:
        print_info("Release cancelled.")
        sys.exit(0)
    
    # Execute release process
    try:
        print_header("Executing Release")
        
        # Update version in files
        print_info("Updating version in files...")
        update_version_in_files(next_version)
        
        # Update changelog
        print_info("Updating CHANGELOG.md...")
        create_changelog_entry(next_version, release_notes)
        
        # Commit and tag
        print_info("Creating commit and tag...")
        commit_and_tag(next_version, release_notes)
        
        # Push to remote
        if not args.skip_push:
            print_info("Pushing to remote...")
            push_to_remote(next_version)
            
            # Create GitHub release
            print_info("Creating GitHub release...")
            create_github_release(next_version, release_notes, args.prerelease)
        else:
            print_warning("Skipped pushing to remote (--skip-push)")
        
        print_header("Release Complete!")
        print_success(f"Successfully released v{next_version}")
        
        if not args.skip_push:
            # Get repository URL
            result = run_command(["git", "remote", "get-url", "origin"])
            repo_url = result.stdout.strip()
            
            # Convert SSH to HTTPS URL for display
            if repo_url.startswith("git@github.com:"):
                repo_url = repo_url.replace("git@github.com:", "https://github.com/")
                repo_url = repo_url.replace(".git", "")
            
            print_info(f"View release: {repo_url}/releases/tag/v{next_version}")
        
    except Exception as e:
        print_error(f"Release failed: {str(e)}")
        print_warning("You may need to manually undo changes:")
        print_warning(f"  git tag -d v{next_version}")
        print_warning(f"  git reset --hard HEAD~1")
        sys.exit(1)


if __name__ == "__main__":
    main()
