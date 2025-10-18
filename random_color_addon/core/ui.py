"""
UI components for Random Color add-on
"""
import bpy


class VIEW3D_PT_random_color(bpy.types.Panel):
    """Main UI Panel for Random Color add-on"""
    bl_label = "Random Color"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Random Color'
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        
        # Main operators
        col.operator("mesh.random_color_selected_faces", icon='COLOR')
        col.operator("mesh.clear_random_color_selected_faces", icon='TRASH')
        layout.separator()
        col.operator("object.faceset_sculpt", icon='SCULPTMODE_HLT')
        layout.separator()
        
        # Update section
        update_box = layout.box()
        update_box.label(text="Add-on Updates")
        update_col = update_box.column(align=True)
        update_col.operator("object.check_for_updates", icon='FILE_REFRESH')
        update_col.operator("object.auto_reload_addon", icon='RECOVER_LAST')
        update_box.label(text=f"Version: {bpy.context.preferences.addons[__package__].module.bl_info['version']}")
        
        layout.separator()
        
        # Material management
        box = layout.box()
        box.label(text="Unused RandomSel Materials")
        obj = context.active_object
        if obj and obj.type == 'MESH' and obj.data:
            mesh = obj.data
            unused_materials = []
            for mat in bpy.data.materials:
                if mat.name.startswith("RandomSel_") and mat not in mesh.materials:
                    unused_materials.append(mat)
            
            if unused_materials:
                for mat in unused_materials[:5]:  # Show max 5
                    row = box.row()
                    row.label(text=mat.name, icon='MATERIAL')
                    row.operator("object.delete_random_material_slot", text="", icon='TRASH').material_name = mat.name
                
                if len(unused_materials) > 5:
                    box.label(text=f"... and {len(unused_materials) - 5} more")
                
                box.operator("object.delete_all_unused_random_materials", icon='CANCEL')
            else:
                box.label(text="No unused materials", icon='CHECKMARK')
        
        # Copy command section
        layout.separator()
        box = layout.box()
        box.label(text="Copy Command")
        box.operator("wm.copy_random_color_command", icon='COPYDOWN')
