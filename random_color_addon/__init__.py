bl_info = {
    "name": "Random Color Selected Faces",
    "author": "RIOO",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Edit Mode > Search or Pie Menu Editor",
    "description": "Assign a random material to selected faces",
    "category": "Mesh",
    "doc_url": "https://github.com/triemnguyen123/RandomColor",
    "tracker_url": "https://github.com/triemnguyen12/RandomColor/issues",
}

import bpy
import random
import os
import json
import urllib.request
import urllib.error
import zipfile
import shutil
from pathlib import Path


def _ensure_random_material() -> bpy.types.Material:
    r = random.random()
    g = random.random()
    b = random.random()

    mat = bpy.data.materials.new(name="RandomSel")
    mat.diffuse_color = (r, g, b, 1.0)
    mat.use_nodes = True
    principled = mat.node_tree.nodes.get("Principled BSDF")
    if principled and hasattr(principled.inputs[0], "default_value"):
        principled.inputs[0].default_value = (r, g, b, 1.0)
    return mat


class MESH_OT_random_color_selected_faces(bpy.types.Operator):
    bl_idname = "mesh.random_color_selected_faces"
    bl_label = "Random Color Selected Faces"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        obj = context.active_object
        return obj is not None and obj.type == "MESH" and obj.mode in {"EDIT", "VERTEX_PAINT", "WEIGHT_PAINT", "TEXTURE_PAINT", "OBJECT"}

    def execute(self, context: bpy.types.Context):
        obj = context.active_object
        if obj is None or obj.type != "MESH":
            self.report({'WARNING'}, "No mesh selected")
            return {'CANCELLED'}

        original_mode = obj.mode

        if original_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        mesh = obj.data
        selected_faces = [p for p in mesh.polygons if p.select]
        if not selected_faces:
            if original_mode != 'OBJECT':
                bpy.ops.object.mode_set(mode=original_mode)
            self.report({'INFO'}, "No faces selected")
            return {'CANCELLED'}

        mat = _ensure_random_material()
        obj.data.materials.append(mat)
        mat_index = len(obj.data.materials) - 1

        for poly in selected_faces:
            poly.material_index = mat_index

        if original_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode=original_mode)

        return {'FINISHED'}

class MESH_OT_clear_random_color_selected_faces(bpy.types.Operator):
    bl_idname = "mesh.clear_random_color_selected_faces"
    bl_label = "Clear Random Color on Selected Faces"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        obj = context.active_object
        return obj is not None and obj.type == "MESH" and obj.mode in {"EDIT", "VERTEX_PAINT", "WEIGHT_PAINT", "TEXTURE_PAINT", "OBJECT"}

    def execute(self, context: bpy.types.Context):
        obj = context.active_object
        if obj is None or obj.type != "MESH":
            self.report({'WARNING'}, "No mesh selected")
            return {'CANCELLED'}

        original_mode = obj.mode
        if original_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        mesh = obj.data
        selected_faces = [p for p in mesh.polygons if p.select]
        if not selected_faces:
            if original_mode != 'OBJECT':
                bpy.ops.object.mode_set(mode=original_mode)
            self.report({'INFO'}, "No faces selected")
            return {'CANCELLED'}

        # Reassign selected faces away from RandomSel to fallback (index 0)
        fallback_index = 0
        for poly in selected_faces:
            poly.material_index = fallback_index

        # Compute currently used material indices after reassignment
        used_indices = {p.material_index for p in mesh.polygons}

        # Remove any RandomSel material slots that are no longer used by any face
        # Do it from highest index to lowest to keep indices stable
        materials = obj.data.materials
        indices_to_remove = [i for i, m in enumerate(materials) if m and m.name.startswith("RandomSel") and i not in used_indices]
        indices_to_remove.sort(reverse=True)

        for i in indices_to_remove:
            mat = materials[i]
            # Remove the material slot safely via operator (updates polygon indices)
            obj.active_material_index = i
            bpy.ops.object.material_slot_remove()
            # If datablock has no users, remove it from bpy.data
            if mat and mat.users == 0:
                bpy.data.materials.remove(mat)

        if original_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode=original_mode)

        return {'FINISHED'}


# ---------- Auto Update System ----------

class AddonUpdater:
    """Auto-update system for the add-on"""
    
    def __init__(self):
        self.github_repo = "yourusername/RandomColor"  # Thay đổi thành repo thực tế của bạn
        self.current_version = bl_info["version"]
        self.addon_name = bl_info["name"]
        
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
                addon_dir = Path(__file__).parent
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
        for cls in classes:
            bpy.utils.unregister_class(cls)
        
        # Import lại module
        import importlib
        import sys
        current_module = sys.modules[__name__]
        importlib.reload(current_module)
        
        # Register lại
        for cls in classes:
            bpy.utils.register_class(cls)
        
        self.report({'INFO'}, "Add-on reloaded!")
        return {'FINISHED'}

# ---------- Simple UI Panel for discoverability ----------

class VIEW3D_PT_random_color(bpy.types.Panel):
    bl_label = "Random Color"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Random Color'

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator(MESH_OT_random_color_selected_faces.bl_idname, icon='COLOR')
        col.operator(MESH_OT_clear_random_color_selected_faces.bl_idname, icon='TRASH')
        layout.separator()
        col.operator(OBJECT_OT_faceset_sculpt.bl_idname, icon='SCULPTMODE_HLT')
        layout.separator()
        
        # Update section
        update_box = layout.box()
        update_box.label(text="Add-on Updates")
        update_col = update_box.column(align=True)
        update_col.operator(OBJECT_OT_check_for_updates.bl_idname, icon='FILE_REFRESH')
        update_col.operator(OBJECT_OT_auto_reload_addon.bl_idname, icon='RECOVER_LAST')
        update_box.label(text=f"Version: {bl_info['version']}")
        
        layout.separator()
        box = layout.box()
        box.label(text="Unused RandomSel Materials")
        # Unused RandomSel materials management (object mode removal)
        obj = context.active_object
        if obj and obj.type == 'MESH' and obj.data:
            mesh = obj.data
            used_indices = {p.material_index for p in mesh.polygons}
            random_unused = [(i, m) for i, m in enumerate(mesh.materials) if m and m.name.startswith("RandomSel") and i not in used_indices]
            if random_unused:
                for i, m in random_unused:
                    row = box.row(align=True)
                    row.label(text=f"Slot {i}: {m.name}")
                    op = row.operator('object.delete_random_material_slot', text='Delete', icon='X')
                    op.slot_index = i
                box.operator('object.delete_all_unused_random_materials', text='Delete All Unused', icon='TRASH')
            else:
                box.label(text="No unused RandomSel materials")
        else:
            box.label(text="Select a Mesh to manage materials")
        layout.separator()
        row = layout.row(align=True)
        row.label(text=f"Command: {MESH_OT_random_color_selected_faces.bl_idname}")
        row.operator('wm.copy_random_color_command', text='', icon='COPYDOWN')


class WM_OT_copy_random_color_command(bpy.types.Operator):
    bl_idname = "wm.copy_random_color_command"
    bl_label = "Copy Random Color Command"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        context.window_manager.clipboard = MESH_OT_random_color_selected_faces.bl_idname
        self.report({'INFO'}, "Copied: mesh.random_color_selected_faces")
        return {'FINISHED'}


class OBJECT_OT_delete_random_material_slot(bpy.types.Operator):
    bl_idname = "object.delete_random_material_slot"
    bl_label = "Delete Random Material Slot"
    bl_options = {"REGISTER", "UNDO"}

    slot_index: bpy.props.IntProperty(name="Slot Index", min=0)

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        obj = context.active_object
        return obj is not None and obj.type == "MESH"

    def execute(self, context: bpy.types.Context):
        obj = context.active_object
        mesh = obj.data
        if self.slot_index < 0 or self.slot_index >= len(mesh.materials):
            self.report({'WARNING'}, "Invalid slot index")
            return {'CANCELLED'}

        mat = mesh.materials[self.slot_index]
        if mat is None or mat.name != "RandomSel":
            self.report({'INFO'}, "Slot is not RandomSel or already empty")
            return {'CANCELLED'}

        # Only allow deletion if no faces use this slot
        used_indices = {p.material_index for p in mesh.polygons}
        if self.slot_index in used_indices:
            self.report({'WARNING'}, "Slot is used by some faces")
            return {'CANCELLED'}

        original_mode = obj.mode
        if original_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        obj.active_material_index = self.slot_index
        bpy.ops.object.material_slot_remove()
        if mat and mat.users == 0:
            bpy.data.materials.remove(mat)

        if original_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode=original_mode)

        return {'FINISHED'}


class OBJECT_OT_delete_all_unused_random_materials(bpy.types.Operator):
    bl_idname = "object.delete_all_unused_random_materials"
    bl_label = "Delete All Unused RandomSel Materials"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        obj = context.active_object
        return obj is not None and obj.type == "MESH"

    def execute(self, context: bpy.types.Context):
        obj = context.active_object
        mesh = obj.data

        # Determine unused RandomSel slots
        used_indices = {p.material_index for p in mesh.polygons}
        indices_to_remove = [i for i, m in enumerate(mesh.materials) if m and m.name.startswith("RandomSel") and i not in used_indices]
        if not indices_to_remove:
            self.report({'INFO'}, "No unused RandomSel materials")
            return {'CANCELLED'}

        original_mode = obj.mode
        if original_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        indices_to_remove.sort(reverse=True)
        for i in indices_to_remove:
            mat = mesh.materials[i]
            obj.active_material_index = i
            bpy.ops.object.material_slot_remove()
            if mat and mat.users == 0:
                bpy.data.materials.remove(mat)

        if original_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode=original_mode)

        return {'FINISHED'}


class OBJECT_OT_faceset_sculpt(bpy.types.Operator):
    bl_idname = "object.faceset_sculpt"
    bl_label = "FaceSet Sculpt"
    bl_description = "Create face set from visible faces in sculpt mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'WARNING'}, "No mesh selected")
            return {'CANCELLED'}

        # Check if we're in edit mode
        if context.mode != 'EDIT_MESH':
            self.report({'WARNING'}, "Please enter Edit Mode first and select faces to hide")
            return {'CANCELLED'}

        # Store current mode
        original_mode = context.mode
        
        # Hide selected faces (Shift+H)
        bpy.ops.mesh.hide(unselected=False)
        
        # Switch to Object Mode first, then Sculpt Mode
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='SCULPT')
        
        # Create face set from visible faces
        bpy.ops.paint.face_set_change_visibility(mode='HIDE')
        bpy.ops.paint.face_set_create()
        
        # Return to Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Unhide all faces (Alt+H)
        bpy.ops.mesh.reveal()
        
        self.report({'INFO'}, "FaceSet created successfully")
        return {'FINISHED'}


# Ensure operator classes tuple is defined after all classes are declared
classes = (
    MESH_OT_random_color_selected_faces,
    MESH_OT_clear_random_color_selected_faces,
    VIEW3D_PT_random_color,
    WM_OT_copy_random_color_command,
    OBJECT_OT_delete_random_material_slot,
    OBJECT_OT_delete_all_unused_random_materials,
    OBJECT_OT_faceset_sculpt,
    OBJECT_OT_check_for_updates,
    OBJECT_OT_auto_reload_addon,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Auto-check for updates on startup (optional)
    # Uncomment the line below if you want automatic update checking
    # bpy.app.timers.register(lambda: updater.check_for_updates(), first_interval=5.0)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()


