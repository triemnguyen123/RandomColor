"""
Auto-update system for Random Color add-on
"""
import bpy
import urllib.request
import json
import zipfile
import shutil
from pathlib import Path


class AddonUpdater:
    """Auto-update system for the add-on"""
    
    def __init__(self):
        self.github_repo = "triemnguyen123/RandomColor"
        self.current_version = (1, 0, 1)  # Will be updated from bl_info
        self.addon_name = "Random Color"
        
    def get_latest_version(self):
        """Lấy version mới nhất từ GitHub"""
        try:
            url = f"https://api.github.com/repos/{self.github_repo}/releases/latest"
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read())
                version_str = data["tag_name"].lstrip("v")
                return tuple(map(int, version_str.split(".")))
        except:
            return None
    
    def download_latest(self):
        """Download và cài đặt version mới nhất"""
        try:
            # Lấy download URL
            url = f"https://api.github.com/repos/{self.github_repo}/releases/latest"
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read())
                download_url = data["zipball_url"]
            
            # Download file
            temp_dir = Path(bpy.app.tempdir) / "addon_update"
            temp_dir.mkdir(exist_ok=True)
            
            zip_path = temp_dir / "latest.zip"
            urllib.request.urlretrieve(download_url, zip_path)
            
            # Extract và copy files
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Tìm folder extracted
            extracted_folder = None
            for item in temp_dir.iterdir():
                if item.is_dir() and item.name.startswith(self.github_repo.split("/")[0]):
                    extracted_folder = item
                    break
            
            if extracted_folder:
                # Copy files vào addon directory
                addon_dir = Path(__file__).parent.parent
                for file_path in extracted_folder.rglob("*"):
                    if file_path.is_file() and file_path.suffix == ".py":
                        relative_path = file_path.relative_to(extracted_folder)
                        target_path = addon_dir / relative_path
                        target_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(file_path, target_path)
            
            # Cleanup
            shutil.rmtree(temp_dir)
            return True
            
        except Exception as e:
            print(f"Update failed: {e}")
            return False
    
    def check_for_updates(self):
        """Kiểm tra có update không"""
        latest = self.get_latest_version()
        if latest and latest > self.current_version:
            return latest
        return None


# Global updater instance
updater = AddonUpdater()


class OBJECT_OT_check_for_updates(bpy.types.Operator):
    """Check for add-on updates"""
    bl_idname = "object.check_for_updates"
    bl_label = "Check for Updates"
    bl_options = {"INTERNAL"}
    
    def execute(self, context):
        latest_version = updater.check_for_updates()
        if latest_version:
            self.report({'INFO'}, f"Update available: {latest_version}")
            # Tự động download và cài đặt
            if updater.download_latest():
                self.report({'INFO'}, "Update installed! Please restart Blender.")
            else:
                self.report({'ERROR'}, "Update failed!")
        else:
            self.report({'INFO'}, "Add-on is up to date!")
        return {'FINISHED'}


class OBJECT_OT_auto_reload_addon(bpy.types.Operator):
    """Reload add-on (useful during development)"""
    bl_idname = "object.auto_reload_addon"
    bl_label = "Reload Add-on"
    bl_options = {"INTERNAL"}
    
    def execute(self, context):
        # Unregister và register lại add-on
        from .. import classes
        for cls in classes:
            bpy.utils.unregister_class(cls)
        
        # Import lại module
        import importlib
        import sys
        current_module = sys.modules[__package__]
        importlib.reload(current_module)
        
        # Register lại
        for cls in classes:
            bpy.utils.register_class(cls)
        
        self.report({'INFO'}, "Add-on reloaded!")
        return {'FINISHED'}
