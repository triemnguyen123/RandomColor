"""
UI components for Random Color add-on
"""
import bpy
import traceback


class VIEW3D_PT_random_color(bpy.types.Panel):
    """Main UI Panel for Random Color add-on"""
    bl_label = "Random Color"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Random Color'
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        
        # Debug info - show version and build time
        from .. import BUILD_TIMESTAMP, bl_info
        debug_box = layout.box()
        debug_box.label(text=f"Version: {'.'.join(map(str, bl_info['version']))}", icon='INFO')
        debug_box.label(text=f"Build: {BUILD_TIMESTAMP}", icon='TIME')
        layout.separator()
        
        # Main operators - simplified UI
        col.operator("mesh.random_color_selected_faces", icon='COLOR')
        col.operator("mesh.clear_random_color_selected_faces", icon='TRASH')
        layout.separator()
        col.operator("object.faceset_sculpt", icon='SCULPTMODE_HLT')
        layout.separator()
        
        # Update and reload buttons
        layout.separator()
        col.operator("object.check_for_updates", icon='FILE_REFRESH')
        col.operator("object.auto_reload_addon", icon='RECOVER_LAST')
