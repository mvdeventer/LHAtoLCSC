"""
Migration Script: Clean up old release scripts

This script helps migrate from the fragmented release scripts to the new
ultimate_release.py script by safely removing the old scripts after
confirming the new script works.

Usage:
    python migrate_release_scripts.py [--dry-run] [--force]
"""

import argparse
import shutil
from pathlib import Path
from typing import List


class Colors:
    """ANSI color codes."""
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    OKCYAN = '\033[96m'


def print_header(text: str):
    """Print formatted header."""
    print(f"\n{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")


def print_success(text: str):
    """Print success message."""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_warning(text: str):
    """Print warning message."""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


def print_info(text: str):
    """Print info message."""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")


def get_old_release_scripts() -> List[Path]:
    """Get list of old release scripts to remove."""
    scripts = [
        Path("release.py"),
        Path("release_workflow.py"),
        Path("release.bat"),
        Path("build_installer.py"),  # Functionality integrated into ultimate_release.py
    ]

    return [script for script in scripts if script.exists()]


def backup_scripts(scripts: List[Path], backup_dir: Path = Path("backup_scripts")) -> bool:
    """Create backup of scripts before removal."""
    try:
        backup_dir.mkdir(exist_ok=True)

        for script in scripts:
            backup_path = backup_dir / script.name
            shutil.copy2(script, backup_path)
            print_success(f"Backed up {script.name} to {backup_path}")

        return True
    except Exception as e:
        print(f"{Colors.FAIL}✗ Failed to create backup: {e}{Colors.ENDC}")
        return False


def remove_scripts(scripts: List[Path], dry_run: bool = False) -> bool:
    """Remove old scripts."""
    try:
        for script in scripts:
            if dry_run:
                print_info(f"Would remove: {script}")
            else:
                script.unlink()
                print_success(f"Removed: {script}")
        return True
    except Exception as e:
        print(f"{Colors.FAIL}✗ Failed to remove scripts: {e}{Colors.ENDC}")
        return False


def update_documentation():
    """Update relevant documentation files."""
    print_info("Documentation updates needed:")
    print("  • Update README.md to reference ultimate_release.py")
    print("  • Update build instructions to use new script")
    print("  • Review any CI/CD references to old scripts")


def main():
    """Main migration function."""
    parser = argparse.ArgumentParser(description="Migrate to ultimate release script")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes only")
    parser.add_argument("--force", action="store_true", help="Skip confirmation prompts")
    args = parser.parse_args()

    print_header("Release Script Migration")

    # Check for ultimate_release.py
    ultimate_script = Path("ultimate_release.py")
    if not ultimate_script.exists():
        print(f"{Colors.FAIL}✗ ultimate_release.py not found! Run this from the project root.{Colors.ENDC}")
        return False

    print_success("Found ultimate_release.py")

    # Find old scripts
    old_scripts = get_old_release_scripts()

    if not old_scripts:
        print_info("No old release scripts found to remove")
        return True

    print_info("Old scripts found:")
    for script in old_scripts:
        print(f"  • {script}")

    if not args.dry_run and not args.force:
        print_warning("\nThis will remove the old release scripts!")
        print("The ultimate_release.py provides all functionality and more.")
        response = input("Continue? (y/N): ")
        if response.lower() != 'y':
            print("Migration cancelled")
            return False

    # Create backup
    if not args.dry_run:
        print_info("Creating backup...")
        if not backup_scripts(old_scripts):
            return False

    # Remove old scripts
    print_info("Removing old scripts...")
    if not remove_scripts(old_scripts, dry_run=args.dry_run):
        return False

    if not args.dry_run:
        print_header("Migration Complete!")
        print_success("Old release scripts have been removed")
        print_success("Backups created in backup_scripts/ directory")
        print_info("\nNext steps:")
        print("  1. Test ultimate_release.py with: python ultimate_release.py patch --dry-run")
        print("  2. Review ULTIMATE_RELEASE_GUIDE.md for usage instructions")
        print("  3. Update team documentation to use new script")
        print("  4. Remove backup_scripts/ after confirming everything works")
    else:
        print_header("Dry Run Complete")
        print_info("Use --force to skip confirmation or run without --dry-run to proceed")

    update_documentation()
    return True


if __name__ == "__main__":
    main()
