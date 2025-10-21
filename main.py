#!/usr/bin/env python3
"""
Main entry point for LHAtoLCSC application.

This script ensures the application runs with the correct Python environment
and module path configuration.
"""

import os
import sys
from pathlib import Path


def main():
    """Run the LHAtoLCSC application."""
    # Get the project root directory
    project_root = Path(__file__).parent.resolve()
    
    # Add src directory to Python path
    src_path = project_root / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    
    # Change to project root directory
    os.chdir(project_root)
    
    try:
        # Import and run the application
        from lhatolcsc.__main__ import main as app_main
        app_main()
    except ImportError as e:
        print(f"Error: Failed to import application: {e}")
        print(f"Python path: {sys.path}")
        print(f"Current directory: {os.getcwd()}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Application failed to start: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
