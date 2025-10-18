"""
Core operators for Random Color add-on
"""
import bpy
import bmesh
import random
import traceback
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
        bm = bmesh.new()
        bm.from_mesh(obj.data)
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
        bm = bmesh.new()
        bm.from_mesh(obj.data)
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
        
        # Store original mode
        original_mode = obj.mode
        
        try:
            # Step 1: Switch to Edit mode
            if original_mode != 'EDIT':
                bpy.ops.object.mode_set(mode='EDIT')
            
            # Step 2: Get selected faces
            bm = bmesh.from_edit_mesh(obj.data)
            bm.faces.ensure_lookup_table()
            selected_face_indices = [f.index for f in bm.faces if f.select]
            
            if not selected_face_indices:
                self.report({'ERROR'}, "No faces selected")
                return {'CANCELLED'}
            
            # Step 3: Switch to Object mode to access mesh data
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Step 4: Get or create face set attribute
            mesh = obj.data
            if ".sculpt_face_set" not in mesh.attributes:
                face_set_attr = mesh.attributes.new(name=".sculpt_face_set", type='INT', domain='FACE')
            else:
                face_set_attr = mesh.attributes[".sculpt_face_set"]
            
            # Step 5: Find the maximum face set ID
            max_id = 0
            for poly in mesh.polygons:
                face_set_id = face_set_attr.data[poly.index].value
                if face_set_id > max_id:
                    max_id = face_set_id
            
            # Step 6: Assign new face set ID to selected faces
            new_face_set_id = max_id + 1
            for face_idx in selected_face_indices:
                face_set_attr.data[face_idx].value = new_face_set_id
            
            # Step 7: Return to Edit mode
            bpy.ops.object.mode_set(mode='EDIT')
            
            # Step 8: Unhide all faces (Alt+H equivalent)
            bpy.ops.mesh.reveal()
            
            self.report({'INFO'}, f"FaceSet created successfully from {len(selected_face_indices)} selected faces. All faces unhidden. Switch to Sculpt mode to see FaceSet.")
            return {'FINISHED'}
            
        except Exception as e:
            # Restore original mode on error
            try:
                bpy.ops.object.mode_set(mode=original_mode)
            except:
                pass
            self.report({'ERROR'}, f"FaceSet creation failed: {str(e)}")
            return {'CANCELLED'}


# Removed OBJECT_OT_block_unused_materials - not needed
