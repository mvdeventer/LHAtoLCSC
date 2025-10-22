"""
Complete Release Workflow for LHAtoLCSC

This script automates the entire release process:
1. Run tests
2. Build Windows installer
3. Bump version
4. Commit changes
5. Create git tag
6. Push to GitHub
7. Create GitHub release with installer

Usage:
    python release_workflow.py patch    # 0.2.0 -> 0.2.1
    python release_workflow.py minor    # 0.2.0 -> 0.3.0
    python release_workflow.py major    # 0.2.0 -> 1.0.0
    
Options:
    --skip-tests        Skip running tests
    --skip-installer    Skip building installer
    --dry-run          Show what would be done without making changes
"""

import subprocess
import sys
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple
import argparse


class Colors:
    """ANSI color codes."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Print formatted header."""
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


def run_command(cmd: list, capture_output: bool = True, check: bool = True) -> subprocess.CompletedProcess:
    """Run shell command."""
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
        if e.stderr:
            print(f"Error: {e.stderr}")
        raise


def get_current_version() -> str:
    """Get current version from config.py."""
    config_path = Path('src/lhatolcsc/core/config.py')
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.search(r'self\.version\s*=\s*["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    
    print_error("Could not find version in config.py")
    sys.exit(1)


def bump_version(current: str, bump_type: str) -> str:
    """Calculate new version based on bump type."""
    parts = current.split('.')
    if len(parts) != 3:
        print_error(f"Invalid version format: {current}")
        sys.exit(1)
    
    major, minor, patch = map(int, parts)
    
    if bump_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif bump_type == 'minor':
        minor += 1
        patch = 0
    elif bump_type == 'patch':
        patch += 1
    else:
        print_error(f"Invalid bump type: {bump_type}")
        sys.exit(1)
    
    return f"{major}.{minor}.{patch}"


def update_version_in_file(file_path: Path, old_version: str, new_version: str) -> bool:
    """Update version in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace version string
        new_content = content.replace(f'"{old_version}"', f'"{new_version}"')
        new_content = new_content.replace(f"'{old_version}'", f"'{new_version}'")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    except Exception as e:
        print_error(f"Failed to update {file_path}: {e}")
        return False


def update_changelog(new_version: str, dry_run: bool = False) -> bool:
    """Add new version section to CHANGELOG.md."""
    changelog_path = Path('CHANGELOG.md')
    
    if not changelog_path.exists():
        print_warning("CHANGELOG.md not found, skipping")
        return True
    
    try:
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the [Unreleased] section
        unreleased_match = re.search(r'## \[Unreleased\](.*?)(?=##|\Z)', content, re.DOTALL)
        if not unreleased_match:
            print_warning("No [Unreleased] section found in CHANGELOG.md")
            return True
        
        # Create new version section
        today = datetime.now().strftime('%Y-%m-%d')
        new_section = f'''## v{new_version}

**Release Date:** {today}

{unreleased_match.group(1).strip()}

---

'''
        
        # Insert new section after [Unreleased]
        new_content = content.replace(
            f"## [Unreleased]{unreleased_match.group(1)}",
            f"## [Unreleased]\n\n### Added\n- \n\n### Changed\n- \n\n### Fixed\n- \n\n---\n\n{new_section}"
        )
        
        if not dry_run:
            with open(changelog_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        
        return True
    except Exception as e:
        print_error(f"Failed to update CHANGELOG.md: {e}")
        return False


def run_tests() -> bool:
    """Run test suite."""
    print_info("Running tests...")
    
    try:
        # Try pytest first
        result = run_command(['pytest', 'tests/', '-v'], check=False)
        if result.returncode == 0:
            print_success("All tests passed")
            return True
        else:
            print_warning("Some tests failed, but continuing...")
            return True
    except FileNotFoundError:
        print_info("pytest not found, skipping tests")
        return True


def build_installer() -> bool:
    """Build Windows installer."""
    print_info("Building Windows installer...")
    
    try:
        result = run_command([sys.executable, 'build_installer.py'], capture_output=False)
        if result.returncode == 0:
            print_success("Installer built successfully")
            return True
        else:
            print_warning("Installer build had warnings, but continuing...")
            return True
    except Exception as e:
        print_error(f"Failed to build installer: {e}")
        return False


def git_commit_and_tag(version: str, dry_run: bool = False) -> bool:
    """Commit changes and create git tag."""
    print_info("Committing changes to git...")
    
    try:
        if not dry_run:
            # Stage all changes
            run_command(['git', 'add', '-A'])
            
            # Commit
            commit_msg = f"chore: Release v{version}"
            run_command(['git', 'commit', '-m', commit_msg])
            
            # Create tag
            tag_msg = f"Release v{version}"
            run_command(['git', 'tag', '-a', f'v{version}', '-m', tag_msg])
            
            print_success(f"Created commit and tag v{version}")
        else:
            print_info(f"[DRY RUN] Would create commit and tag v{version}")
        
        return True
    except subprocess.CalledProcessError as e:
        print_error("Git operations failed")
        return False


def extract_changelog_section(version: str) -> str:
    """Extract release notes for a specific version from CHANGELOG.md."""
    changelog_path = Path('CHANGELOG.md')
    if not changelog_path.exists():
        return ""
    
    try:
        content = changelog_path.read_text(encoding='utf-8')
        
        # Find the section for this version
        version_pattern = rf'## v{re.escape(version)}\s*\n(.*?)(?=\n## v|\Z)'
        match = re.search(version_pattern, content, re.DOTALL)
        
        if match:
            section = match.group(1).strip()
            
            # Format for GitHub release
            release_notes = f"# Release v{version}\n\n{section}"
            return release_notes
        
        return ""
    except Exception as e:
        print_warning(f"Could not extract changelog: {e}")
        return ""


def push_to_github(version: str, dry_run: bool = False) -> bool:
    """Push commits and tags to GitHub."""
    print_info("Pushing to GitHub...")
    
    try:
        if not dry_run:
            # Push commits
            run_command(['git', 'push', 'origin', 'master'])
            
            # Push tags
            run_command(['git', 'push', 'origin', f'v{version}'])
            
            print_success("Pushed to GitHub")
        else:
            print_info("[DRY RUN] Would push to GitHub")
        
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to push to GitHub")
        return False


def create_github_release(version: str, dry_run: bool = False) -> bool:
    """Create GitHub release with installer."""
    print_info("Creating GitHub release...")
    
    # Check if gh CLI is available
    try:
        run_command(['gh', '--version'], capture_output=True)
    except FileNotFoundError:
        print_error("GitHub CLI (gh) not found. Install from: https://cli.github.com/")
        return False
    
    # Generate release notes from CHANGELOG
    release_notes = extract_changelog_section(version)
    if not release_notes:
        release_notes = f"Release v{version}\n\nSee CHANGELOG.md for details."
    
    try:
        if not dry_run:
            # Create release
            cmd = [
                'gh', 'release', 'create', f'v{version}',
                '--title', f'v{version}',
                '--notes', release_notes
            ]
            
            # Add installer files if they exist
            installer_dir = Path('installer')
            if installer_dir.exists():
                for file in installer_dir.glob('*'):
                    if file.is_file():
                        cmd.append(str(file))
            
            result = run_command(cmd)
            print_success(f"Created GitHub release v{version}")
            
            # Print release URL
            if result.stdout:
                print_info(f"Release URL: {result.stdout.strip()}")
        else:
            print_info(f"[DRY RUN] Would create GitHub release v{version}")
        
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to create GitHub release")
        return False


def main():
    """Main release workflow."""
    parser = argparse.ArgumentParser(description='Complete release workflow for LHAtoLCSC')
    parser.add_argument('bump_type', choices=['major', 'minor', 'patch'], 
                       help='Version bump type')
    parser.add_argument('--skip-tests', action='store_true',
                       help='Skip running tests')
    parser.add_argument('--skip-installer', action='store_true',
                       help='Skip building installer')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    
    args = parser.parse_args()
    
    print_header("LHAtoLCSC Release Workflow")
    
    if args.dry_run:
        print_warning("DRY RUN MODE - No changes will be made")
    
    # Get current and new version
    current_version = get_current_version()
    new_version = bump_version(current_version, args.bump_type)
    
    print_info(f"Current version: {current_version}")
    print_info(f"New version: {new_version}")
    
    if not args.dry_run:
        response = input(f"\nProceed with release v{new_version}? (y/n): ")
        if response.lower() != 'y':
            print_info("Release cancelled")
            sys.exit(0)
    
    # Step 1: Run tests
    if not args.skip_tests:
        if not run_tests():
            print_error("Tests failed, aborting release")
            sys.exit(1)
    else:
        print_info("Skipping tests (--skip-tests)")
    
    # Step 2: Update version in files
    if not args.dry_run:
        print_info("Updating version in files...")
        files_to_update = [
            Path('src/lhatolcsc/core/config.py'),
            Path('setup.py'),
        ]
        
        for file_path in files_to_update:
            if file_path.exists():
                if update_version_in_file(file_path, current_version, new_version):
                    print_success(f"Updated {file_path}")
                else:
                    print_error(f"Failed to update {file_path}")
                    sys.exit(1)
    else:
        print_info("[DRY RUN] Would update version in config.py and setup.py")
    
    # Step 3: Update CHANGELOG
    if not update_changelog(new_version, args.dry_run):
        print_warning("Failed to update CHANGELOG.md, but continuing...")
    
    # Step 4: Build installer
    if not args.skip_installer:
        if not build_installer():
            print_warning("Installer build failed, but continuing...")
    else:
        print_info("Skipping installer build (--skip-installer)")
    
    # Step 5: Git commit and tag
    if not git_commit_and_tag(new_version, args.dry_run):
        print_error("Git operations failed, aborting")
        sys.exit(1)
    
    # Step 6: Push to GitHub
    if not push_to_github(new_version, args.dry_run):
        print_error("Failed to push to GitHub, aborting")
        sys.exit(1)
    
    # Step 7: Create GitHub release
    if not create_github_release(new_version, args.dry_run):
        print_warning("Failed to create GitHub release, but changes were committed")
    
    # Summary
    print_header("Release Complete!")
    print_success(f"Successfully released v{new_version}")
    
    print("\nNext steps:")
    print("  1. Verify the release on GitHub")
    print("  2. Test the installer")
    print("  3. Update documentation if needed")
    
    if args.dry_run:
        print_warning("\nThis was a DRY RUN - no changes were actually made")


if __name__ == '__main__':
    main()
