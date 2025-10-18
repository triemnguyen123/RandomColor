"""
Random Color Add-on for Blender
Assigns random colors to selected faces
"""

import bpy

bl_info = {
    "name": "Random Color",
    "author": "Triem Nguyen",
    "version": (1, 0, 9),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Random Color",
    "description": "Assign a random material to selected faces",
    "category": "Mesh",
    "doc_url": "https://github.com/triemnguyen123/RandomColor",
    "tracker_url": "https://github.com/triemnguyen12/RandomColor/issues",
}

# Build timestamp for debugging
import datetime
BUILD_TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Import all operators and UI components
from .core.operators import (
    MESH_OT_random_color_selected_faces,
    MESH_OT_clear_random_color_selected_faces,
    OBJECT_OT_faceset_sculpt,
)

from .core.ui import VIEW3D_PT_random_color

# Removed unused material management operators

from .core.updater import (
    OBJECT_OT_check_for_updates,
    OBJECT_OT_auto_reload_addon,
    updater,
)

# Update version in updater
updater.current_version = bl_info["version"]

# All classes to register
classes = (
    MESH_OT_random_color_selected_faces,
    MESH_OT_clear_random_color_selected_faces,
    VIEW3D_PT_random_color,
    OBJECT_OT_faceset_sculpt,
    OBJECT_OT_check_for_updates,
    OBJECT_OT_auto_reload_addon,
)


def register():
    """Register all classes"""
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Auto-check for updates on startup (optional)
    # Uncomment the line below if you want automatic update checking
    # bpy.app.timers.register(lambda: updater.check_for_updates(), first_interval=5.0)


def unregister():
    """Unregister all classes"""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    # Clear module cache to ensure fresh reload
    import sys
    module_name = __name__
    if module_name in sys.modules:
        del sys.modules[module_name]


if __name__ == "__main__":
    register()