import bpy
import bmesh
from mathutils import Vector

def createRoofs(obj, amount):
    # Get the active object (ensure it is a mesh object)
    if obj is None or obj.type != 'MESH':
        raise ValueError("Please select a mesh object.")
    pass
    
    bpy.context.view_layer.objects.active = obj;
    obj.select_set(True);
    
    # Enter edit mode and access the mesh data
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(obj.data);
    
    # Iterate through all faces in the mesh
    dbg_length = len(bm.faces);
    change = [];
    for (i, face) in enumerate(bm.faces):
        if len(face.verts) != 4: continue; # Check if the face is a quad
        print(i, "/", dbg_length);
        # Get the edges and calculate their lengths
        edges = list(face.edges)
        edge_lengths = [edge.calc_length() for edge in edges]
        min_index = min((l, i) for (i, l) in enumerate(edge_lengths))[1];
        
        N = edges[min_index];
        S = edges[(min_index + 2) % len(edges)];
        
        # NW   N   NE      NW   NN   NE
        #                              
        #                              
        # W         E  ->  W          E
        #                              
        #                              
        # SW   S   SE      SW   SS   SE
        
        (NE, NW) = N.verts;
        (SW, SE) = S.verts;
        # we assume counter-clokwise, actual direction not important
        
        NN = bm.verts.new((NE.co + NW.co) / 2);
        SS = bm.verts.new((SE.co + SW.co) / 2);
        
        NN.co.z += amount;
        SS.co.z += amount;
        
        change.append((
            [face],
            [
                [NN, NW, SW, SS],
                [NE, NN, SS, SE],
                [NE, NW, NN],
                [SW, SE, SS],
            ]
        ));
    pass
    for (to_remove, to_add) in change:
        for face in to_remove: bm.faces.remove(face);
        for vertices in to_add: bm.faces.new(vertices);
    pass
    
    # Update the mesh and exit edit mode
    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')
pass

createRoofs(bpy.data.objects["Areas:building_roof"], 10.0);
