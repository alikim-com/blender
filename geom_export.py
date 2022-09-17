import bpy

def fmtNum(n, p = 8):
     return f'{n:.{p}f}'

# export UVs
uvexp = True

out = "{ "

for coll in bpy.data.collections:
    print(coll.name)
    out += "{:s}: {{".format(coll.name)

    for obj in coll.objects:
        # only export objects which name starts with underscore    
        #if obj.name[0] == '_':
            mesh = obj.data
            out += "{:s}: {{".format(obj.name)

            out += "vert:[ "
            vert_local = [v.co for v in obj.data.vertices.values()]
            vert_world = [obj.matrix_world @ v_local for v_local in vert_local]
            for _,v in enumerate(vert_world):
                out += "{:.8f},{:.8f},{:.8f},".format(*v)
            out += " ], "
                  
            out += "poly:[ "
            for p in mesh.polygons:
                vert = p.vertices
                out += '[' + ','.join(map(str, vert)) + '],'
            out += " ], "
            
            if uvexp:
                uvl = mesh.uv_layers
                if uvl:
                    uvs = [None] * len(mesh.vertices) * 2
                    out += "uv:[ "
                    for p in mesh.polygons:
                        vert = p.vertices
                        rnge = p.loop_indices
                        for i,v in enumerate(vert):
                            off = v * 2
                            if uvs[off] == None:
                                uv = uvl.active.data[rnge[i]].uv
                                uvs[off] = uv[0]
                                uvs[off + 1] = uv[1]
                    out += ','.join(map(fmtNum, uvs)) + "],"

            out += " }, "

    out += "}, "

out += "}"

path = bpy.path.abspath("//")
fname = path + coll.name + '_export.txt'

print("writting to file '" + fname + "'...")

with open(fname,'w') as file_object:
    file_object.write(out)
    
print("done")

