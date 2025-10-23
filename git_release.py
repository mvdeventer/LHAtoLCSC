#!/usr/bin/env python3
"""
Git Release Script for LHAtoLCSC

This script automates Git operations for creating releases:
1. Validates current Git status
2. Commits pending changes
3. Creates and pushes Git tags
4. Handles version bumping
5. Manages release notes
6. Optional GitHub release creation

Usage:
    python git_release.py --version 0.2.4 --message "Enhanced pagination and currency persistence"
    python git_release.py --bump patch --message "Bug fixes"
    python git_release.py --bump minor --message "New features"
    python git_release.py --bump major --message "Breaking changes"

Options:
    --version VERSION       Specific version to tag (e.g., 0.2.4)
    --bump TYPE            Bump version: patch/minor/major
    --message MESSAGE      Release message/description
    --tag-prefix PREFIX    Tag prefix (default: 'v')
    --commit-all          Commit all changed files
    --push               Push to remote after tagging
    --create-release     Create GitHub release (requires gh CLI)
    --dry-run           Show what would be done without making changes
    --force             Force operations (use with caution)
"""

import subprocess
import sys
import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple, List
import os


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


class GitReleaseManager:
    """Manages Git release operations."""
    
    def __init__(self, dry_run: bool = False, force: bool = False):
        self.dry_run = dry_run
        self.force = force
        self.project_root = Path(__file__).parent
        
    def print_status(self, message: str, status: str = "INFO"):
        """Print formatted status message."""
        color = {
            "INFO": Colors.OKBLUE,
            "SUCCESS": Colors.OKGREEN,
            "WARNING": Colors.WARNING,
            "ERROR": Colors.FAIL,
            "HEADER": Colors.HEADER
        }.get(status, Colors.ENDC)
        
        prefix = "DRY RUN: " if self.dry_run else ""
        print(f"{color}[{status}] {prefix}{message}{Colors.ENDC}")
    
    def run_command(self, command: List[str], check: bool = True, capture: bool = False) -> subprocess.CompletedProcess:
        """Run a command with optional dry-run support."""
        cmd_str = " ".join(command)
        
        if self.dry_run:
            self.print_status(f"Would run: {cmd_str}", "INFO")
            # Return a mock result for dry run
            return subprocess.CompletedProcess(command, 0, stdout="", stderr="")
        
        try:
            self.print_status(f"Running: {cmd_str}", "INFO")
            result = subprocess.run(
                command,
                cwd=self.project_root,
                check=check,
                capture_output=capture,
                text=True
            )
            return result
        except subprocess.CalledProcessError as e:
            self.print_status(f"Command failed: {cmd_str}", "ERROR")
            self.print_status(f"Error: {e}", "ERROR")
            if e.stdout:
                self.print_status(f"Stdout: {e.stdout}", "ERROR")
            if e.stderr:
                self.print_status(f"Stderr: {e.stderr}", "ERROR")
            raise
    
    def get_current_version(self) -> str:
        """Get current version from pyproject.toml."""
        pyproject_path = self.project_root / "pyproject.toml"
        
        if not pyproject_path.exists():
            raise FileNotFoundError("pyproject.toml not found")
        
        content = pyproject_path.read_text(encoding='utf-8')
        
        # Extract version using regex
        pattern = r'version\s*=\s*["\']([^"\']+)["\']'
        version_match = re.search(pattern, content)
        if not version_match:
            raise ValueError("Version not found in pyproject.toml")
        
        return version_match.group(1)
    
    def bump_version(self, current_version: str, bump_type: str) -> str:
        """Bump version according to semantic versioning."""
        version_parts = current_version.split('.')
        
        if len(version_parts) != 3:
            raise ValueError(f"Invalid version format: {current_version}")
        
        major, minor, patch = map(int, version_parts)
        
        if bump_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif bump_type == "minor":
            minor += 1
            patch = 0
        elif bump_type == "patch":
            patch += 1
        else:
            raise ValueError(f"Invalid bump type: {bump_type}")
        
        return f"{major}.{minor}.{patch}"
    
    def update_version_file(self, new_version: str):
        """Update version in pyproject.toml."""
        pyproject_path = self.project_root / "pyproject.toml"
        
        if self.dry_run:
            self.print_status(f"Would update pyproject.toml version to {new_version}", "INFO")
            return
        
        content = pyproject_path.read_text(encoding='utf-8')
        
        # Replace version
        new_content = re.sub(
            r'(version\\s*=\\s*["\'])[^"\']+(["\'])',
            f'\\g<1>{new_version}\\g<2>',
            content
        )
        
        pyproject_path.write_text(new_content, encoding='utf-8')
        self.print_status(f"Updated pyproject.toml version to {new_version}", "SUCCESS")
    
    def check_git_status(self) -> Tuple[bool, List[str]]:
        """Check Git repository status."""
        try:
            # Check if we're in a git repository
            result = self.run_command(["git", "rev-parse", "--git-dir"], capture=True)
            
            # Check for uncommitted changes
            result = self.run_command(["git", "status", "--porcelain"], capture=True)
            changed_files = [line.strip() for line in result.stdout.split('\\n') if line.strip()]
            
            has_changes = len(changed_files) > 0
            return has_changes, changed_files
            
        except subprocess.CalledProcessError:
            raise RuntimeError("Not in a Git repository or Git not available")
    
    def get_current_branch(self) -> str:
        """Get current Git branch."""
        result = self.run_command(["git", "branch", "--show-current"], capture=True)
        return result.stdout.strip()
    
    def tag_exists(self, tag: str) -> bool:
        """Check if a Git tag already exists."""
        if self.dry_run:
            # In dry-run mode, assume tag doesn't exist unless it's a known tag
            # This prevents false positives during testing
            return False
        
        try:
            result = self.run_command(
                ["git", "rev-parse", f"refs/tags/{tag}"], 
                capture=True, 
                check=False
            )
            return result.returncode == 0
        except subprocess.CalledProcessError:
            return False
    
    def create_commit(self, message: str, files: List[str] = None):
        """Create a Git commit."""
        if files:
            # Add specific files
            for file in files:
                self.run_command(["git", "add", file])
        else:
            # Add all changes
            self.run_command(["git", "add", "."])
        
        # Check if there's anything to commit
        try:
            result = self.run_command(["git", "diff", "--cached", "--quiet"], check=False)
            if result.returncode == 0:
                self.print_status("No changes to commit", "WARNING")
                return False
        except:
            pass
        
        # Create commit
        self.run_command(["git", "commit", "-m", message])
        self.print_status(f"Created commit: {message}", "SUCCESS")
        return True
    
    def create_tag(self, tag: str, message: str):
        """Create a Git tag."""
        if self.tag_exists(tag) and not self.force:
            raise ValueError(f"Tag {tag} already exists. Use --force to overwrite.")
        
        if self.tag_exists(tag) and self.force:
            self.print_status(f"Deleting existing tag: {tag}", "WARNING")
            self.run_command(["git", "tag", "-d", tag])
        
        self.run_command(["git", "tag", "-a", tag, "-m", message])
        self.print_status(f"Created tag: {tag}", "SUCCESS")
    
    def push_changes(self, tag: str = None):
        """Push changes and tags to remote."""
        # Push commits
        self.run_command(["git", "push"])
        self.print_status("Pushed commits to remote", "SUCCESS")
        
        # Push tag if specified
        if tag:
            self.run_command(["git", "push", "origin", tag])
            self.print_status(f"Pushed tag {tag} to remote", "SUCCESS")
    
    def create_github_release(self, tag: str, title: str, message: str):
        """Create GitHub release using gh CLI."""
        # Check if gh CLI is available
        try:
            self.run_command(["gh", "--version"], capture=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.print_status("GitHub CLI (gh) not available. Skipping GitHub release creation.", "WARNING")
            return
        
        # Create release
        cmd = [
            "gh", "release", "create", tag,
            "--title", title,
            "--notes", message
        ]
        
        # Check for installer file
        installer_path = self.project_root / "dist" / "LHAtoLCSC-Setup.exe"
        if installer_path.exists():
            cmd.extend([str(installer_path)])
            self.print_status("Adding installer to GitHub release", "INFO")
        
        self.run_command(cmd)
        self.print_status(f"Created GitHub release: {tag}", "SUCCESS")
    
    def generate_release_notes(self, version: str, message: str) -> str:
        """Generate release notes."""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        
        notes = f"""# Release {version} - {timestamp}

## {message}

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
"""
        return notes


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Git Release Management for LHAtoLCSC",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    # Version arguments (mutually exclusive)
    version_group = parser.add_mutually_exclusive_group(required=True)
    version_group.add_argument("--version", help="Specific version to tag (e.g., 0.2.4)")
    version_group.add_argument("--bump", choices=["patch", "minor", "major"], 
                              help="Bump version type")
    
    # Required arguments
    parser.add_argument("--message", required=True, 
                       help="Release message/description")
    
    # Optional arguments
    parser.add_argument("--tag-prefix", default="v", 
                       help="Tag prefix (default: 'v')")
    parser.add_argument("--commit-all", action="store_true",
                       help="Commit all changed files")
    parser.add_argument("--push", action="store_true",
                       help="Push to remote after tagging")
    parser.add_argument("--create-release", action="store_true",
                       help="Create GitHub release (requires gh CLI)")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be done without making changes")
    parser.add_argument("--force", action="store_true",
                       help="Force operations (use with caution)")
    
    args = parser.parse_args()
    
    # Initialize release manager
    release_manager = GitReleaseManager(dry_run=args.dry_run, force=args.force)
    
    try:
        release_manager.print_status("Starting Git release process", "HEADER")
        
        # Check Git status
        has_changes, changed_files = release_manager.check_git_status()
        current_branch = release_manager.get_current_branch()
        
        release_manager.print_status(f"Current branch: {current_branch}", "INFO")
        
        if has_changes:
            release_manager.print_status(f"Found {len(changed_files)} changed files:", "WARNING")
            for file in changed_files[:10]:  # Show first 10 files
                release_manager.print_status(f"  {file}", "INFO")
            if len(changed_files) > 10:
                release_manager.print_status(f"  ... and {len(changed_files) - 10} more", "INFO")
        
        # Determine version
        current_version = release_manager.get_current_version()
        release_manager.print_status(f"Current version: {current_version}", "INFO")
        
        if args.version:
            new_version = args.version
        else:
            new_version = release_manager.bump_version(current_version, args.bump)
        
        release_manager.print_status(f"Target version: {new_version}", "INFO")
        
        # Update version file if needed
        if new_version != current_version:
            release_manager.update_version_file(new_version)
            has_changes = True  # Now we have version file changes
        
        # Commit changes if requested
        if has_changes and (args.commit_all or new_version != current_version):
            commit_message = f"Release {new_version}: {args.message}"
            files_to_commit = ["pyproject.toml"] if not args.commit_all else None
            release_manager.create_commit(commit_message, files_to_commit)
        elif has_changes and not args.commit_all:
            release_manager.print_status("Uncommitted changes found. Use --commit-all to include them.", "WARNING")
        
        # Create tag
        tag = f"{args.tag_prefix}{new_version}"
        tag_message = f"Release {new_version}: {args.message}"
        release_manager.create_tag(tag, tag_message)
        
        # Push if requested
        if args.push:
            release_manager.push_changes(tag)
        
        # Create GitHub release if requested
        if args.create_release:
            release_title = f"LHAtoLCSC {new_version}"
            release_notes = release_manager.generate_release_notes(new_version, args.message)
            release_manager.create_github_release(tag, release_title, release_notes)
        
        release_manager.print_status("Release process completed successfully!", "SUCCESS")
        release_manager.print_status(f"Created release: {tag}", "SUCCESS")
        
        if not args.push:
            release_manager.print_status("Remember to push your changes: git push && git push origin " + tag, "INFO")
        
        if not args.create_release:
            release_manager.print_status("To create GitHub release: python git_release.py --create-release", "INFO")
        
    except Exception as e:
        release_manager.print_status(f"Release process failed: {e}", "ERROR")
        sys.exit(1)


if __name__ == "__main__":
    main()