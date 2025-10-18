#!/usr/bin/env python3
"""
Install addon to Blender addons directory
"""

import os
import sys
import shutil
from pathlib import Path

def install_addon():
    """Install addon to Blender"""
    print("🚀 Installing Random Color Addon to Blender")
    print("=" * 50)
    
    # Find addon directory
    addon_path = Path("random_color_addon")
    if not addon_path.exists():
        print("❌ Addon directory not found!")
        return False
    
    # Find Blender addons directory
    blender_addons_paths = [
        Path.home() / "AppData" / "Roaming" / "Blender Foundation" / "Blender" / "4.4" / "scripts" / "addons",
        Path.home() / "AppData" / "Roaming" / "Blender Foundation" / "Blender" / "4.3" / "scripts" / "addons",
        Path.home() / "AppData" / "Roaming" / "Blender Foundation" / "Blender" / "4.2" / "scripts" / "addons",
        Path("D:/UngDung/Blender/4.4/scripts/addons"),
        Path("D:/UngDung/Blender/4.3/scripts/addons"),
        Path("D:/UngDung/Blender/4.2/scripts/addons"),
    ]
    
    blender_addons_path = None
    for path in blender_addons_paths:
        if path.exists():
            blender_addons_path = path
            break
    
    if not blender_addons_path:
        print("❌ Blender addons directory not found!")
        print("   Please install Blender first")
        return False
    
    print(f"✅ Found Blender addons: {blender_addons_path}")
    
    # Copy addon
    target_path = blender_addons_path / "random_color_addon"
    
    # Remove existing addon
    if target_path.exists():
        print(f"🗑️  Removing existing addon...")
        shutil.rmtree(target_path)
    
    try:
        # Copy addon
        print(f"📦 Copying addon...")
        shutil.copytree(addon_path, target_path)
        print(f"✅ Addon installed: {target_path}")
        
        print("\n🎉 Installation complete!")
        print("\n📋 Next steps:")
        print("1. Open Blender")
        print("2. Go to Edit > Preferences > Add-ons")
        print("3. Search for 'Random Color' and enable it")
        print("4. The addon will appear in the 3D Viewport sidebar")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to install addon: {e}")
        return False

if __name__ == "__main__":
    install_addon()
