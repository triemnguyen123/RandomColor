#!/usr/bin/env python3
"""
Script to create a new release for Random Color add-on
Usage: python scripts/create_release.py 1.0.1
"""

import sys
import subprocess
import os
from pathlib import Path

def update_version(version):
    """Update version in all relevant files"""
    version_tuple = f"({', '.join(version.split('.'))})"
    
    # Update __init__.py
    init_file = Path("random_color_addon/__init__.py")
    if init_file.exists():
        content = init_file.read_text()
        content = content.replace(
            '"version": (1, 0, 0)',
            f'"version": {version_tuple}'
        )
        init_file.write_text(content)
        print(f"Updated version in {init_file}")
    
    # Update updater.py
    updater_file = Path("random_color_addon/core/updater.py")
    if updater_file.exists():
        content = updater_file.read_text()
        content = content.replace(
            'self.current_version = (1, 0, 0)',
            f'self.current_version = {version_tuple}'
        )
        updater_file.write_text(content)
        print(f"Updated version in {updater_file}")

def create_release(version):
    """Create git tag and push"""
    tag = f"v{version}"
    
    # Add and commit changes
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", f"Release {tag}"], check=True)
    
    # Create and push tag
    subprocess.run(["git", "tag", tag], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    subprocess.run(["git", "push", "origin", tag], check=True)
    
    print(f"Created release {tag}")
    print("GitHub Actions will automatically build and publish the release")
    

def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/create_release.py <version>")
        print("Example: python scripts/create_release.py 1.0.1")
        sys.exit(1)
    
    version = sys.argv[1]
    
    # Validate version format
    try:
        parts = version.split('.')
        if len(parts) != 3:
            raise ValueError
        [int(x) for x in parts]
    except ValueError:
        print("Error: Version must be in format X.Y.Z (e.g., 1.0.1)")
        sys.exit(1)
    
    print(f"Creating release {version}...")
    
    # Update version in files
    update_version(version)
    
    create_release(version)
    
    print("Release created successfully!")
    print("Check GitHub Actions for build progress")

if __name__ == "__main__":
    main()
