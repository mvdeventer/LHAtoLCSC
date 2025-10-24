"""
Ultimate GitHub Release Script for LHAtoLCSC

This comprehensive script automates the entire release process with:
- GitHub API integration for version detection
- Automatic version incrementation (patch, minor, major)
- Multi-file version synchronization
- Git operations with proper tagging
- GitHub Actions trigger for installer building
- Release notes generation from git commits
- Changelog updating
- Asset verification and upload
- Rollback capabilities
- Comprehensive error handling and logging

Usage:
    python ultimate_release.py [patch|minor|major] [--dry-run] [--force]

Requirements:
    pip install requests pygithub gitpython
"""

import argparse
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from git import Repo
from github import Github


class Colors:
    """ANSI color codes for beautiful terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class ReleaseLogger:
    """Enhanced logging with timestamps and colors."""

    def __init__(self, log_file: str = "release.log"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(exist_ok=True)

    def _log(self, level: str, message: str, color: str = ""):
        """Internal logging method."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"

        # Print to console with color
        print(f"{color}{log_entry}{Colors.ENDC}")

        # Write to file without color codes
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"{log_entry}\n")

    def header(self, text: str):
        """Print formatted header."""
        border = "=" * 80
        self._log("HEADER", f"\n{border}\n{text.center(80)}\n{border}", Colors.HEADER + Colors.BOLD)

    def success(self, text: str):
        """Log success message."""
        self._log("SUCCESS", f"✓ {text}", Colors.OKGREEN)

    def info(self, text: str):
        """Log info message."""
        self._log("INFO", f"ℹ {text}", Colors.OKCYAN)

    def warning(self, text: str):
        """Log warning message."""
        self._log("WARNING", f"⚠ {text}", Colors.WARNING)

    def error(self, text: str):
        """Log error message."""
        self._log("ERROR", f"✗ {text}", Colors.FAIL)

    def step(self, text: str):
        """Log step message."""
        self._log("STEP", f"→ {text}", Colors.OKBLUE)


class Version:
    """Semantic version handling."""

    def __init__(self, version_string: str):
        """Initialize from version string (e.g., '1.2.3' or 'v1.2.3')."""
        clean_version = version_string.lstrip('v')
        parts = clean_version.split('.')

        if len(parts) != 3:
            raise ValueError(f"Invalid version format: {version_string}")

        self.major = int(parts[0])
        self.minor = int(parts[1])
        self.patch = int(parts[2])

    def increment(self, bump_type: str) -> 'Version':
        """Return new version with incremented component."""
        if bump_type == "major":
            return Version(f"{self.major + 1}.0.0")
        elif bump_type == "minor":
            return Version(f"{self.major}.{self.minor + 1}.0")
        elif bump_type == "patch":
            return Version(f"{self.major}.{self.minor}.{self.patch + 1}")
        else:
            raise ValueError(f"Invalid bump type: {bump_type}")

    def __str__(self):
        """Return version string."""
        return f"{self.major}.{self.minor}.{self.patch}"

    def __lt__(self, other):
        """Compare versions."""
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)

    def __le__(self, other):
        """Compare versions."""
        return (self.major, self.minor, self.patch) <= (other.major, other.minor, other.patch)

    def __gt__(self, other):
        """Compare versions."""
        return (self.major, self.minor, self.patch) > (other.major, other.minor, other.patch)

    def __ge__(self, other):
        """Compare versions."""
        return (self.major, self.minor, self.patch) >= (other.major, other.minor, other.patch)

    def __eq__(self, other):
        """Check version equality."""
        return (self.major, self.minor, self.patch) == (other.major, other.minor, other.patch)


class GitHubReleaseMaster:
    """Master class for comprehensive GitHub release management."""

    def __init__(self, repo_path: str = ".", github_token: Optional[str] = None):
        """Initialize the release master."""
        self.logger = ReleaseLogger()
        self.repo_path = Path(repo_path).resolve()
        self.git_repo = Repo(self.repo_path)

        # GitHub setup
        self.github_token = github_token or self._get_github_token()
        self.github = Github(self.github_token)
        self.repo_name = self._get_repo_name()
        self.gh_repo = self.github.get_repo(self.repo_name)

        # File paths for version management
        self.version_files = {
            "config.py": self.repo_path / "src" / "lhatolcsc" / "core" / "config.py",
            "pyproject.toml": self.repo_path / "pyproject.toml",
            "setup.py": self.repo_path / "setup.py",
        }

        # State tracking
        self.rollback_info = {}

    def _get_github_token(self) -> str:
        """Get GitHub token from environment or git config."""
        import os

        # Try environment variable first
        token = os.getenv("GITHUB_TOKEN")
        if token:
            return token

        # Try git config
        try:
            result = subprocess.run(
                ["git", "config", "--get", "github.token"],
                capture_output=True,
                text=True,
                cwd=self.repo_path
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except Exception:
            pass

        # Try gh CLI
        try:
            result = subprocess.run(
                ["gh", "auth", "token"],
                capture_output=True,
                text=True,
                cwd=self.repo_path
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except Exception:
            pass

        raise ValueError(
            "GitHub token not found. Set GITHUB_TOKEN environment variable, "
            "configure with 'git config github.token <token>', "
            "or authenticate with 'gh auth login'"
        )

    def _get_repo_name(self) -> str:
        """Extract repository name from git remote."""
        try:
            origin_url = self.git_repo.remote('origin').url

            # Handle both SSH and HTTPS URLs
            if origin_url.startswith('git@github.com:'):
                repo_path = origin_url[15:].rstrip('.git')
            elif 'github.com/' in origin_url:
                repo_path = origin_url.split('github.com/')[-1].rstrip('.git')
            else:
                raise ValueError(f"Cannot parse GitHub repo from URL: {origin_url}")

            return repo_path
        except Exception as e:
            raise ValueError(f"Failed to determine repository name: {e}")

    def get_latest_release_version(self) -> Optional[Version]:
        """Get the latest release version from GitHub."""
        try:
            releases = list(self.gh_repo.get_releases())
            if not releases:
                self.logger.info("No existing releases found")
                return None

            latest_release = releases[0]
            version_str = latest_release.tag_name.lstrip('v')
            self.logger.info(f"Latest release: {latest_release.tag_name}")
            return Version(version_str)

        except Exception as e:
            self.logger.warning(f"Failed to get latest release: {e}")
            return None

    def get_current_version(self) -> Version:
        """Get current version from config.py."""
        config_file = self.version_files["config.py"]

        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_file}")

        content = config_file.read_text(encoding='utf-8')
        match = re.search(r'self\.version\s*=\s*["\']([^"\']+)["\']', content)

        if not match:
            raise ValueError("Version not found in config.py")

        return Version(match.group(1))

    def calculate_next_version(self, bump_type: str) -> Version:
        """Calculate the next version based on bump type."""
        current_version = self.get_current_version()
        latest_release = self.get_latest_release_version()

        if latest_release and latest_release >= current_version:
            # Base next version on latest release
            next_version = latest_release.increment(bump_type)
            self.logger.info(f"Basing next version on latest release: {latest_release} → {next_version}")
        else:
            # Base next version on current code version
            next_version = current_version.increment(bump_type)
            self.logger.info(f"Basing next version on current code: {current_version} → {next_version}")

        return next_version

    def update_version_files(self, new_version: Version, dry_run: bool = False) -> Dict[str, str]:
        """Update version in all relevant files."""
        self.logger.step(f"Updating version to {new_version}")
        changes = {}

        for file_key, file_path in self.version_files.items():
            if not file_path.exists():
                self.logger.warning(f"File not found: {file_path}")
                continue

            try:
                original_content = file_path.read_text(encoding='utf-8')
                updated_content = original_content

                if file_key == "config.py":
                    # Update config.py version
                    updated_content = re.sub(
                        r'(self\.version\s*=\s*["\'])([^"\']+)(["\'])',
                        f'\\g<1>{new_version}\\g<3>',
                        updated_content
                    )

                elif file_key == "pyproject.toml":
                    # Update pyproject.toml version
                    updated_content = re.sub(
                        r'(version\s*=\s*["\'])([^"\']+)(["\'])',
                        f'\\g<1>{new_version}\\g<3>',
                        updated_content
                    )

                elif file_key == "setup.py":
                    # Update setup.py version
                    updated_content = re.sub(
                        r'(version\s*=\s*["\'])([^"\']+)(["\'])',
                        f'\\g<1>{new_version}\\g<3>',
                        updated_content
                    )

                if updated_content != original_content:
                    changes[str(file_path)] = original_content
                    if not dry_run:
                        file_path.write_text(updated_content, encoding='utf-8')
                    self.logger.success(f"Updated {file_path.name}")
                else:
                    self.logger.warning(f"No version pattern found in {file_path.name}")

            except Exception as e:
                self.logger.error(f"Failed to update {file_path}: {e}")

        return changes

    def generate_release_notes(self, since_tag: Optional[str] = None) -> str:
        """Generate release notes from git commits."""
        self.logger.step("Generating release notes from git history")

        try:
            # Get commits since last tag
            if since_tag:
                commit_range = f"{since_tag}..HEAD"
            else:
                # Get all commits if no previous tag
                commit_range = "HEAD"

            # Get git log
            result = subprocess.run([
                "git", "log", commit_range,
                "--pretty=format:• %s",
                "--no-merges"
            ], capture_output=True, text=True, cwd=self.repo_path)

            if result.returncode != 0:
                raise subprocess.CalledProcessError(result.returncode, result.args, result.stderr)

            commits = result.stdout.strip()

            if not commits:
                return "• Initial release"

            # Process commits into categories
            features = []
            fixes = []
            other = []

            for line in commits.split('\n'):
                line = line.strip()
                if not line:
                    continue

                lower_line = line.lower()
                if any(keyword in lower_line for keyword in ['feat:', 'feature:', 'add:', 'new:']):
                    features.append(line)
                elif any(keyword in lower_line for keyword in ['fix:', 'bug:', 'hotfix:', 'patch:']):
                    fixes.append(line)
                else:
                    other.append(line)

            # Build release notes
            notes = []

            if features:
                notes.append("### ✨ Features")
                notes.extend(features)
                notes.append("")

            if fixes:
                notes.append("### 🐛 Bug Fixes")
                notes.extend(fixes)
                notes.append("")

            if other:
                notes.append("### 📝 Other Changes")
                notes.extend(other)
                notes.append("")

            release_notes = '\n'.join(notes).strip()
            self.logger.success(f"Generated release notes ({len(commits.split())} commits)")

            return release_notes

        except Exception as e:
            self.logger.warning(f"Failed to generate release notes: {e}")
            return "• See git history for changes"

    def update_changelog(self, version: Version, release_notes: str, dry_run: bool = False) -> bool:
        """Update CHANGELOG.md with new version."""
        self.logger.step("Updating CHANGELOG.md")

        changelog_path = self.repo_path / "CHANGELOG.md"

        try:
            if changelog_path.exists():
                content = changelog_path.read_text(encoding='utf-8')
            else:
                content = "# Changelog\n\nAll notable changes to this project will be documented in this file.\n\n"

            # Create new entry
            release_date = datetime.now().strftime("%Y-%m-%d")
            new_entry = f"""## v{version}
**Release Date:** {release_date}

{release_notes}

"""

            # Insert after the header
            lines = content.split('\n')
            insert_index = 3  # After title and description

            # Find the right place to insert (after any existing header)
            for i, line in enumerate(lines):
                if line.startswith('## '):
                    insert_index = i
                    break

            lines.insert(insert_index, new_entry)
            updated_content = '\n'.join(lines)

            if not dry_run:
                changelog_path.write_text(updated_content, encoding='utf-8')

            self.logger.success("Updated CHANGELOG.md")
            return True

        except Exception as e:
            self.logger.error(f"Failed to update CHANGELOG.md: {e}")
            return False

    def commit_and_tag(self, version: Version, dry_run: bool = False) -> bool:
        """Commit changes and create git tag."""
        self.logger.step(f"Committing changes and creating tag v{version}")

        if dry_run:
            self.logger.info("DRY RUN: Would commit and tag")
            return True

        try:
            # Stage all changes
            self.git_repo.git.add('--all')

            # Check if there are changes to commit
            if not self.git_repo.is_dirty(untracked_files=True):
                self.logger.warning("No changes to commit")
                return False

            # Commit
            commit_message = f"Release v{version}"
            self.git_repo.index.commit(commit_message)
            self.logger.success(f"Committed: {commit_message}")

            # Create tag
            tag_name = f"v{version}"
            self.git_repo.create_tag(tag_name, message=f"Release {tag_name}")
            self.logger.success(f"Created tag: {tag_name}")

            # Push to origin
            origin = self.git_repo.remote('origin')
            origin.push()
            origin.push(tags=True)
            self.logger.success("Pushed to origin with tags")

            return True

        except Exception as e:
            self.logger.error(f"Failed to commit and tag: {e}")
            return False

    def wait_for_workflow_completion(self, version: Version, timeout: int = 1800) -> bool:
        """Wait for GitHub Actions workflow to complete."""
        self.logger.step("Waiting for GitHub Actions workflow to complete")

        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                # Get workflow runs triggered by our tag
                workflows = self.gh_repo.get_workflow_runs()

                for run in workflows:
                    if run.head_sha == self.git_repo.head.commit.hexsha:
                        self.logger.info(f"Found workflow run: {run.html_url}")

                        if run.status == "completed":
                            if run.conclusion == "success":
                                self.logger.success("Workflow completed successfully!")
                                return True
                            else:
                                self.logger.error(f"Workflow failed with conclusion: {run.conclusion}")
                                return False
                        else:
                            self.logger.info(f"Workflow status: {run.status}")

                time.sleep(30)  # Wait 30 seconds before checking again

            except Exception as e:
                self.logger.warning(f"Error checking workflow status: {e}")
                time.sleep(30)

        self.logger.error("Timeout waiting for workflow completion")
        return False

    def create_github_release(self, version: Version, release_notes: str,
                              wait_for_assets: bool = True, dry_run: bool = False) -> bool:
        """Create GitHub release."""
        self.logger.step(f"Creating GitHub release v{version}")

        if dry_run:
            self.logger.info("DRY RUN: Would create GitHub release")
            return True

        try:
            tag_name = f"v{version}"

            # Wait for workflow to complete if requested
            if wait_for_assets:
                if not self.wait_for_workflow_completion(version):
                    self.logger.warning("Workflow didn't complete successfully, creating release anyway")

            # Create release
            release = self.gh_repo.create_git_release(
                tag=tag_name,
                name=f"Release v{version}",
                message=f"""# Release v{version}

{release_notes}

## Installation

### Windows Installer
Download and run `LHAtoLCSC-{version}-Setup.exe` for a complete installation with start menu integration.

### Portable Version
Download `LHAtoLCSC-{version}-Portable.zip`, extract, and run `LHAtoLCSC.exe` (no installation required).

### From Python Package
```bash
pip install lhatolcsc=={version}
```

## Requirements
- Python 3.10 or higher (for Python package only)
- LCSC API credentials

See [README.md](https://github.com/{self.repo_name}/blob/main/README.md) for full documentation.
""",
                draft=False,
                prerelease=False
            )

            self.logger.success(f"Created release: {release.html_url}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to create GitHub release: {e}")
            return False

    def rollback_changes(self, changes: Dict[str, str]):
        """Rollback file changes in case of failure."""
        self.logger.warning("Rolling back changes...")

        for file_path, original_content in changes.items():
            try:
                Path(file_path).write_text(original_content, encoding='utf-8')
                self.logger.info(f"Rolled back {file_path}")
            except Exception as e:
                self.logger.error(f"Failed to rollback {file_path}: {e}")

    def verify_release_assets(self, version: Version, max_wait: int = 300) -> bool:
        """Verify that release assets are available."""
        self.logger.step("Verifying release assets...")

        tag_name = f"v{version}"
        start_time = time.time()

        while time.time() - start_time < max_wait:
            try:
                release = self.gh_repo.get_release(tag_name)
                assets = list(release.get_assets())

                if assets:
                    self.logger.success(f"Found {len(assets)} release assets:")
                    for asset in assets:
                        self.logger.info(f"  • {asset.name} ({asset.size} bytes)")
                    return True
                else:
                    self.logger.info("No assets found yet, waiting...")
                    time.sleep(10)

            except Exception as e:
                self.logger.warning(f"Error checking assets: {e}")
                time.sleep(10)

        self.logger.warning("Assets not found within timeout period")
        return False

    def _clean_old_installers(self, next_version: Version, dry_run: bool = False):
        """Clean old installer files to ensure only the latest version is released."""
        self.logger.step("Cleaning old installer files from local directory")

        installer_dir = self.repo_path / "installer"
        if not installer_dir.exists():
            self.logger.info("No installer directory found")
            return

        # Pattern for current version files
        current_version_patterns = [
            f"LHAtoLCSC-{next_version}-Setup.exe",
            f"LHAtoLCSC-{next_version}-Portable.zip"
        ]

        try:
            removed_count = 0
            for file in installer_dir.glob("*"):
                if file.is_file() and file.name not in current_version_patterns:
                    if dry_run:
                        self.logger.info(f"Would remove: {file.name}")
                    else:
                        file.unlink()
                        self.logger.success(f"Removed old installer: {file.name}")
                    removed_count += 1

            if removed_count == 0:
                self.logger.info("No old installer files to remove")
            elif not dry_run:
                self.logger.success(f"Cleaned {removed_count} old installer file(s)")

        except Exception as e:
            self.logger.warning(f"Failed to clean local installers: {e}")

    def _clean_old_release_assets(self, dry_run: bool = False):
        """Remove old installer files from previous GitHub releases."""
        self.logger.step("Cleaning old installer assets from previous GitHub releases")

        if dry_run:
            self.logger.info("DRY RUN: Would clean old release assets")
            return

        try:
            releases = list(self.gh_repo.get_releases())
            cleaned_releases = 0

            for release in releases:
                # Skip the latest 3 releases
                if cleaned_releases >= len(releases) - 3:
                    continue

                assets_to_remove = []
                for asset in release.get_assets():
                    # Remove old installer files but keep wheel and tar.gz
                    if asset.name.endswith(('-Setup.exe', '-Portable.zip')):
                        # Check if it's from a different version than the release
                        if not asset.name.startswith(f"LHAtoLCSC-{release.tag_name.lstrip('v')}-"):
                            assets_to_remove.append(asset)

                for asset in assets_to_remove:
                    try:
                        asset.delete_asset()
                        self.logger.success(f"Removed {asset.name} from {release.tag_name}")
                    except Exception as e:
                        self.logger.warning(f"Failed to remove {asset.name}: {e}")

                if assets_to_remove:
                    cleaned_releases += 1

            if cleaned_releases == 0:
                self.logger.info("No old installer assets found in previous releases")
            else:
                self.logger.success(f"Cleaned assets from {cleaned_releases} previous release(s)")

        except Exception as e:
            self.logger.warning(f"Failed to clean old release assets: {e}")

    def perform_release(self, bump_type: str = "patch", dry_run: bool = False,
                        force: bool = False, wait_for_assets: bool = True) -> bool:
        """Perform the complete release process."""
        self.logger.header(f"Starting {bump_type.upper()} Release Process")

        if dry_run:
            self.logger.warning("DRY RUN MODE - No changes will be made")

        try:
            # 1. Calculate next version
            next_version = self.calculate_next_version(bump_type)
            self.logger.info(f"Target version: {next_version}")

            # 2. Check for existing tag
            existing_tags = [tag.name for tag in self.git_repo.tags]
            if f"v{next_version}" in existing_tags and not force:
                self.logger.error(f"Tag v{next_version} already exists! Use --force to override")
                return False

            # 3. Check working directory
            if self.git_repo.is_dirty() and not force:
                self.logger.error("Working directory is dirty! Commit changes first or use --force")
                return False

            # 4. Clean old installers from local installer directory
            self._clean_old_installers(next_version, dry_run)

            # 5. Update version files
            changes = self.update_version_files(next_version, dry_run)

            # 6. Generate release notes
            latest_release = self.get_latest_release_version()
            since_tag = f"v{latest_release}" if latest_release else None
            release_notes = self.generate_release_notes(since_tag)

            # 7. Update changelog
            self.update_changelog(next_version, release_notes, dry_run)

            # 8. Commit and tag
            if not self.commit_and_tag(next_version, dry_run):
                self.logger.error("Failed to commit and tag")
                if not dry_run:
                    self.rollback_changes(changes)
                return False

            # 9. Create GitHub release
            if not self.create_github_release(next_version, release_notes, wait_for_assets, dry_run):
                self.logger.error("Failed to create GitHub release")
                return False

            # 10. Verify assets if requested
            if wait_for_assets and not dry_run:
                self.verify_release_assets(next_version)

            # 11. Clean old installer assets from previous releases
            self._clean_old_release_assets(dry_run)

            self.logger.header("🎉 Release Complete!")
            self.logger.success(f"Successfully released v{next_version}")
            self.logger.info(f"Release URL: https://github.com/{self.repo_name}/releases/tag/v{next_version}")

            return True

        except Exception as e:
            self.logger.error(f"Release failed: {e}")
            if 'changes' in locals():
                self.rollback_changes(changes)
            return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Ultimate GitHub Release Script for LHAtoLCSC",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ultimate_release.py patch              # Create patch release (0.1.0 → 0.1.1)
  python ultimate_release.py minor              # Create minor release (0.1.0 → 0.2.0)
  python ultimate_release.py major              # Create major release (0.1.0 → 1.0.0)
  python ultimate_release.py patch --dry-run    # Preview changes without making them
  python ultimate_release.py minor --force      # Force release even with dirty working dir
  python ultimate_release.py patch --no-wait    # Don't wait for GitHub Actions
        """
    )

    parser.add_argument(
        "bump_type",
        choices=["patch", "minor", "major"],
        help="Type of version bump to perform"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without making them"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Force release even with dirty working directory or existing tag"
    )

    parser.add_argument(
        "--no-wait",
        action="store_true",
        help="Don't wait for GitHub Actions to complete"
    )

    parser.add_argument(
        "--github-token",
        help="GitHub token (defaults to GITHUB_TOKEN env var or git config)"
    )

    args = parser.parse_args()

    try:
        # Create release master
        release_master = GitHubReleaseMaster(github_token=args.github_token)

        # Perform release
        success = release_master.perform_release(
            bump_type=args.bump_type,
            dry_run=args.dry_run,
            force=args.force,
            wait_for_assets=not args.no_wait
        )

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Release interrupted by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.FAIL}Fatal error: {e}{Colors.ENDC}")
        sys.exit(1)


if __name__ == "__main__":
    main()
