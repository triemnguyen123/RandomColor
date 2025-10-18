"""
Material management utilities for Random Color add-on
"""
import bpy


class OBJECT_OT_delete_random_material_slot(bpy.types.Operator):
    """Delete a specific RandomSel material"""
    bl_idname = "object.delete_random_material_slot"
    bl_label = "Delete RandomSel Material"
    bl_options = {"REGISTER", "UNDO"}
    
    material_name: bpy.props.StringProperty(name="Material Name")
    
    def execute(self, context):
        if self.material_name in bpy.data.materials:
            bpy.data.materials.remove(bpy.data.materials[self.material_name])
            self.report({'INFO'}, f"Deleted material: {self.material_name}")
        else:
            self.report({'ERROR'}, f"Material not found: {self.material_name}")
        return {'FINISHED'}


class OBJECT_OT_delete_all_unused_random_materials(bpy.types.Operator):
    """Delete all unused RandomSel materials"""
    bl_idname = "object.delete_all_unused_random_materials"
    bl_label = "Delete All Unused RandomSel Materials"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "No active mesh object")
            return {'CANCELLED'}
        
        mesh = obj.data
        unused_materials = []
        
        for mat in bpy.data.materials:
            if mat.name.startswith("RandomSel_") and mat not in mesh.materials:
                unused_materials.append(mat)
        
        for mat in unused_materials:
            bpy.data.materials.remove(mat)
        
        self.report({'INFO'}, f"Deleted {len(unused_materials)} unused materials")
        return {'FINISHED'}


class WM_OT_copy_random_color_command(bpy.types.Operator):
    """Copy random color command to clipboard"""
    bl_idname = "wm.copy_random_color_command"
    bl_label = "Copy Random Color Command"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        command = "bpy.ops.mesh.random_color_selected_faces()"
        context.window_manager.clipboard = command
        self.report({'INFO'}, "Command copied to clipboard")
        return {'FINISHED'}
