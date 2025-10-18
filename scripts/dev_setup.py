#!/usr/bin/env python3
"""
Development setup script for Random Color add-on
This script helps with development workflow
"""

import os
import sys
import shutil
from pathlib import Path

def get_blender_addons_path():
    """Get Blender addons directory path"""
    if sys.platform == "win32":
        # Windows
        appdata = os.environ.get('APPDATA')
        return Path(appdata) / "Blender Foundation" / "Blender" / "addons"
    elif sys.platform == "darwin":
        # macOS
        home = Path.home()
        return home / "Library" / "Application Support" / "Blender Foundation" / "Blender" / "addons"
    else:
        # Linux
        home = Path.home()
        return home / ".config" / "blender" / "addons"

def install_addon():
    """Install addon to Blender addons directory"""
    addons_path = get_blender_addons_path()
    addon_name = "random_color_addon"
    source_path = Path("random_color_addon")
    target_path = addons_path / addon_name
    
    if not source_path.exists():
        print("Error: random_color_addon directory not found")
        return False
    
    # Create addons directory if it doesn't exist
    addons_path.mkdir(parents=True, exist_ok=True)
    
    # Remove existing installation
    if target_path.exists():
        shutil.rmtree(target_path)
        print(f"Removed existing installation at {target_path}")
    
    # Copy addon
    shutil.copytree(source_path, target_path)
    print(f"Installed addon to {target_path}")
    
    return True

def create_symlink():
    """Create symlink for development (Linux/macOS only)"""
    if sys.platform == "win32":
        print("Symlinks not supported on Windows, using copy instead")
        return install_addon()
    
    addons_path = get_blender_addons_path()
    addon_name = "random_color_addon"
    source_path = Path("random_color_addon").absolute()
    target_path = addons_path / addon_name
    
    # Create addons directory if it doesn't exist
    addons_path.mkdir(parents=True, exist_ok=True)
    
    # Remove existing installation
    if target_path.exists():
        if target_path.is_symlink():
            target_path.unlink()
        else:
            shutil.rmtree(target_path)
        print(f"Removed existing installation at {target_path}")
    
    # Create symlink
    target_path.symlink_to(source_path)
    print(f"Created symlink: {target_path} -> {source_path}")
    
    return True

def main():
    print("Random Color Add-on Development Setup")
    print("=" * 40)
    
    if len(sys.argv) > 1 and sys.argv[1] == "symlink":
        success = create_symlink()
    else:
        success = install_addon()
    
    if success:
        print("\nSetup complete!")
        print("\nNext steps:")
        print("1. Open Blender")
        print("2. Go to Edit > Preferences > Add-ons")
        print("3. Search for 'Random Color' and enable it")
        print("4. Use 'Reload Add-on' button in the panel for development")
        print("\nTo create a release:")
        print("python scripts/create_release.py 1.0.1")
    else:
        print("Setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
