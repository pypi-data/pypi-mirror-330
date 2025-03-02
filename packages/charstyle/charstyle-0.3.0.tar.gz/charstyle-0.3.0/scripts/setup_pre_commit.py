#!/usr/bin/env python3
"""
Setup script for pre-commit hooks.
This script installs pre-commit hooks for the charstyle project.
"""

import subprocess
import sys


def main() -> int:
    """Install pre-commit hooks."""
    print("Setting up pre-commit hooks for charstyle...")

    # Check if pre-commit is installed
    try:
        subprocess.run(["pre-commit", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("pre-commit not found. Installing...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pre-commit"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error installing pre-commit: {e}")
            return 1

    # Install the pre-commit hooks
    try:
        subprocess.run(["pre-commit", "install"], check=True)
        print("Pre-commit hooks installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing pre-commit hooks: {e}")
        return 1

    # Run pre-commit hooks on all files
    print("Running pre-commit hooks on all files...")
    try:
        subprocess.run(["pre-commit", "run", "--all-files"], check=False)
    except subprocess.CalledProcessError:
        print("Some pre-commit hooks failed. Please fix the issues and try again.")

    print("\nSetup complete! Pre-commit hooks will now run automatically on git commit.")
    print("You can also run them manually with: pre-commit run --all-files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
