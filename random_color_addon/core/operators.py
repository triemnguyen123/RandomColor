"""
Core operators for Random Color add-on
"""
import bpy
import bmesh
import random
from mathutils import Vector


def get_random_color():
    """Generate a random RGB color"""
    return (random.random(), random.random(), random.random(), 1.0)


def create_random_material(name, color):
    """Create a new material with random color"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
    return mat


class MESH_OT_random_color_selected_faces(bpy.types.Operator):
    """Assign random colors to selected faces"""
    bl_idname = "mesh.random_color_selected_faces"
    bl_label = "Random Color Selected Faces"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "No active mesh object")
            return {'CANCELLED'}
        
        if obj.mode != 'EDIT':
            self.report({'ERROR'}, "Must be in Edit mode")
            return {'CANCELLED'}
        
        # Get bmesh
        bm = bmesh.from_mesh(obj.data)
        bm.faces.ensure_lookup_table()
        
        # Get selected faces
        selected_faces = [f for f in bm.faces if f.select]
        if not selected_faces:
            self.report({'ERROR'}, "No faces selected")
            return {'CANCELLED'}
        
        # Create materials for each selected face
        for i, face in enumerate(selected_faces):
            color = get_random_color()
            mat_name = f"RandomSel_{i+1:03d}"
            
            # Create material
            mat = create_random_material(mat_name, color)
            
            # Assign to face
            face.material_index = len(obj.data.materials)
            obj.data.materials.append(mat)
        
        # Update mesh
        bm.to_mesh(obj.data)
        obj.data.update()
        
        self.report({'INFO'}, f"Applied random colors to {len(selected_faces)} faces")
        return {'FINISHED'}


class MESH_OT_clear_random_color_selected_faces(bpy.types.Operator):
    """Clear random colors from selected faces"""
    bl_idname = "mesh.clear_random_color_selected_faces"
    bl_label = "Clear Random Color Selected Faces"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "No active mesh object")
            return {'CANCELLED'}
        
        if obj.mode != 'EDIT':
            self.report({'ERROR'}, "Must be in Edit mode")
            return {'CANCELLED'}
        
        # Get bmesh
        bm = bmesh.from_mesh(obj.data)
        bm.faces.ensure_lookup_table()
        
        # Get selected faces
        selected_faces = [f for f in bm.faces if f.select]
        if not selected_faces:
            self.report({'ERROR'}, "No faces selected")
            return {'CANCELLED'}
        
        # Clear material indices
        for face in selected_faces:
            face.material_index = 0
        
        # Update mesh
        bm.to_mesh(obj.data)
        obj.data.update()
        
        self.report({'INFO'}, f"Cleared colors from {len(selected_faces)} faces")
        return {'FINISHED'}


class OBJECT_OT_faceset_sculpt(bpy.types.Operator):
    """Create FaceSet for sculpting from selected faces"""
    bl_idname = "object.faceset_sculpt"
    bl_label = "Create FaceSet for Sculpting"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "No active mesh object")
            return {'CANCELLED'}
        
        # Switch to Sculpt mode
        original_mode = obj.mode
        bpy.ops.object.mode_set(mode='SCULPT')
        
        # Create FaceSet from selected faces
        bpy.ops.paint.face_set_create()
        
        # Return to original mode
        bpy.ops.object.mode_set(mode=original_mode)
        
        self.report({'INFO'}, "FaceSet created successfully")
        return {'FINISHED'}
