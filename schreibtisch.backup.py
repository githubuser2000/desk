import copy
import math
import socket
import time

import bmesh
import bpy
from mathutils import Vector

mult_frames = 4


def reset_blend():
    # bpy.ops.wm.read_factory_settings()

    for scene in bpy.data.scenes:
        for obj in scene.objects:
            for val in obj.values():
                scene.objects.collection_unlink(val)

    # only worry about data in the startup scene
    for bpy_data_iter in (
        bpy.data.objects,
        bpy.data.meshes,
        bpy.data.materials,
        bpy.data.cameras,
    ):
        for id_data in bpy_data_iter:
            bpy_data_iter.remove(id_data)


# def joinmerge(obs):
#    ctx = bpy.context.copy()
#    # one of the objects to join
#    ctx['active_object'] = obs[0]
#    ctx['selected_objects'] = obs
##    ctx['selected_editable_bases'] = [bpy.types.Scene.view_layers[ob.name] for ob in obs]
#    bpy.ops.object.join(ctx)


def joinmerge(obs):
    c = {}
    c["object"] = c["active_object"] = obs[0]
    c["selected_objects"] = c["selected_editable_objects"] = obs
    bpy.ops.object.join(c)


def createCube(x, y, z, xx, yy, zz):
    bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
    # cube = bpy.context.scene.objects[-1]
    bpy.ops.transform.resize(value=(xx, yy, zz))


def differ(from_, to):
    mod_bool = from_.modifiers.new("my_bool_mod", "BOOLEAN")
    mod_bool.operation = "DIFFERENCE"
    mod_bool.object = to
    bpy.context.view_layer.objects.active = from_
    res = bpy.ops.object.modifier_apply(modifier="my_bool_mod")


def unioner(from_, to):
    mod_bool = from_.modifiers.new("my_bool_mod", "BOOLEAN")
    mod_bool.operation = "UNION"
    mod_bool.object = to
    bpy.context.view_layer.objects.active = from_
    res = bpy.ops.object.modifier_apply(modifier="my_bool_mod")


def curvyobj(coords, coords2):
    curveData = bpy.data.curves.new("myCurve", type="SURFACE")
    curveData2 = bpy.data.curves.new("myCurve", type="SURFACE")
    curveData.dimensions = "3D"
    curveData.resolution_u = len(coords)
    curveData.resolution_v = len(coords)
    curveData2.dimensions = "3D"
    curveData2.resolution_u = len(coords2)
    curveData2.resolution_v = len(coords2)
    polyline = curveData.splines.new("POLY")
    polyline.points.add(len(coords) - 1)
    polyline2 = curveData.splines.new("POLY")
    polyline2.points.add(len(coords) - 1)
    for i, coord in enumerate(coords):
        x, y, z = coord
        polyline.points[i].co = (x, y, z, 1)
    for i, coord in enumerate(coords2):
        x, y, z = coord
        polyline2.points[i].co = (x, y, z, 1)

    # create Object
    surface_object = bpy.data.objects.new("myCurve", curveData)
    surface_object2 = bpy.data.objects.new("myCurve", curveData2)
    # curveData.bevel_depth = 100

    # attach to scene and validate context
    scn = bpy.context.scene
    # for scene in bpy.data.scenes:
    bpy.context.collection.objects.link(surface_object)
    bpy.context.collection.objects.link(surface_object2)
    # bpy.context.view_layer.objects.active = curveOB
    splines = surface_object.data.splines
    for s in splines:
        for p in s.points:
            p.select = True
    splines = surface_object2.data.splines
    for s in splines:
        for p in s.points:
            p.select = True

    bpy.context.view_layer.objects.active = surface_object
    # bpy.ops.object.mode_set(mode = 'EDIT')
    # bpy.ops.curve.make_segment()
    # bpy.ops.object.mode_set(mode = 'OBJECT')

    # mesh arrays
    verts = []  # the vertex array
    faces = []  # the face array

    # mesh variables
    numX = len(coords)  # number of quadrants in the x direction
    numY = 2  # number of quadrants in the y direction

    # wave variables
    freq = 1  # the wave frequency
    amp = 1  # the wave amplitude
    scale = 1  # the scale of the mesh

    # fill verts array
    # coords3=coords[0],coords2[0]
    # coords4=coords[1],coords2[1]
    # coords5=coords[2],coords2[2]

    matrix = []
    for m, n in zip(coords, coords2):
        matrix.append([m, n])

    # for i in [coords3,coords4,coords5]:
    for i in matrix:
        for x, y, z in i:
            vert = (x, y, z)
            verts.append(vert)

    # create mesh and object
    mesh = bpy.data.meshes.new("wave")
    object = bpy.data.objects.new("wave", mesh)

    # set mesh location
    #    object.location = bpy.context.scene.cursor_location
    bpy.context.collection.objects.link(object)

    # create mesh from python data
    mesh.from_pydata(verts, [], faces)
    mesh.update(calc_edges=True)

    # fill faces array
    count = 0
    for i in range(0, numY * (numX - 1)):
        if count < numY - 1:
            A = i  # the first vertex
            B = i + 1  # the second vertex
            C = (i + numY) + 1  # the third vertex
            D = i + numY  # the fourth vertex

            face = (A, B, C, D)
            faces.append(face)
            count = count + 1
        else:
            count = 0

    # create mesh and object
    mesh = bpy.data.meshes.new("wave")
    object = bpy.data.objects.new("wave", mesh)

    # set mesh location
    #    object.location = bpy.context.scene.cursor_location
    bpy.context.collection.objects.link(object)

    # create mesh from python data
    mesh.from_pydata(verts, [], faces)
    mesh.update(calc_edges=True)

    object.select_set(state=False)


# bpy.ops.wm.
# bpy.ops.wm.open_mainfile(filepath="/home/alex/Downloads/Palm_Tree.blend")
reset_blend()
# import bpy
# def setState0():
#    for ob in bpy.data.objects.values():ob.selected=False
#    bpy.context.view_layer.objects.active = None
# setState0()
# original_type = bpy.context.area.type
# bpy.context.area.type = "VIEW_3D"
# bpy.context.mode='OBJECT'
# bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
# bpy.context.area.type = original_type
# bpy.ops.wm.read_homefile(use_empty=True)
# bpy.ops.wm.read_factory_settings(use_empty=True)
# original_type = bpy.context.area.type
# bpy.context.
# bpy.context.area.type = "VIEW_3D"
# bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
# bpy.context.area.type = original_type
breite = 1.5
tiefe = 1.5

bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
# bpy.ops.mesh.primitive_cube_add()
# cont = bpy.context.area.type
# print(str(cont))
# myobject = bpy.context.active_object
# bpy.context.view_layer.objects.active = myobject
# myobject.select = True
scn = bpy.context.scene
cube = scn.objects["Cube"]
bpy.context.scene.objects[0].select_set(state=True)
bpy.ops.transform.resize(value=(9 / 2 * tiefe, 16 / 2 * breite, 0.2))
bpy.ops.mesh.primitive_cylinder_add(
    vertices=128, radius=3 * (breite + tiefe) / math.pi, location=(5.5 * tiefe, 0, 0)
)
bpy.ops.transform.resize(value=(1 * tiefe, 2 * breite, 1))
cylinder = scn.objects["Cylinder"]
cube.name = "Tischplatte"
bpy.context.scene.objects[0].select_set(state=False)

mod_bool = cube.modifiers.new("my_bool_mod", "BOOLEAN")
mod_bool.operation = "DIFFERENCE"
mod_bool.object = cylinder
bpy.context.view_layer.objects.active = cube
# bpy.context.view_layer.objects.active = cube
res = bpy.ops.object.modifier_apply(modifier="my_bool_mod")
cube.select_set(state=False)
cylinder.select_set(state=True)
bpy.ops.object.delete()

bpy.ops.mesh.primitive_cube_add(location=(-(9 / 2 - 7 / 2) * tiefe, 0, -2))
cube2 = scn.objects["Cube"]
cube2.name = "Platte_2"
bpy.ops.transform.resize(value=(7 / 2 * tiefe, 16 / 2 * breite, 0.2))

bpy.ops.mesh.primitive_cylinder_add(
    vertices=128, radius=3 * (breite + tiefe) / math.pi, location=(2.5 * tiefe, 0, -2)
)
bpy.ops.transform.resize(value=(1 * tiefe, 2 * breite, 1))
cyl1 = scn.objects["Cylinder"]
cyl1.name = "cyl1"
bpy.ops.mesh.primitive_cylinder_add(
    vertices=128, radius=3 * (breite + tiefe) / math.pi, location=(2.5 * tiefe, 0, -2)
)
bpy.ops.transform.resize(value=(2 * tiefe, breite, 1))
cyl2 = scn.objects["Cylinder"]
cyl2.name = "cyl2"

cyl1.select_set(state=False)
cyl2.select_set(state=False)

for cyli in [cyl1, cyl2]:
    mod_bool = cube2.modifiers.new("my_bool_mod", "BOOLEAN")
    mod_bool.operation = "DIFFERENCE"
    mod_bool.object = cyli
    bpy.context.view_layer.objects.active = cube2
    res = bpy.ops.object.modifier_apply(modifier="my_bool_mod")
    cube.select_set(state=False)
    cube2.select_set(state=False)
    cyli.select_set(state=True)
    bpy.ops.object.delete()

bpy.ops.mesh.primitive_cube_add(
    location=(9 / 2 * tiefe - 0.5 - tiefe * 2, (16 / 2 - 0.5) * breite, -4.29)
)
leg = scn.objects["Cube"]
leg.name = "Tischbein1"
leg.select_set(state=True)
bpy.ops.transform.resize(value=(0.5, 0.5, 4.5))
leg.select_set(state=False)
bpy.ops.mesh.primitive_cube_add(
    location=(-9 / 2 * tiefe + 0.5, (-16 / 2 + 0.5) * breite, -4.29)
)
leg = scn.objects["Cube"]
leg.name = "Tischbein2"
leg.select_set(state=True)
bpy.ops.transform.resize(value=(0.5, 0.5, 4.5))
leg.select_set(state=False)
bpy.ops.mesh.primitive_cube_add(
    location=(9 / 2 * tiefe - 0.5 - tiefe * 2, (-16 / 2 + 0.5) * breite, -4.29)
)
leg = scn.objects["Cube"]
leg.name = "Tischbein3"
leg.select_set(state=True)
bpy.ops.transform.resize(value=(0.5, 0.5, 4.5))
leg.select_set(state=False)
bpy.ops.mesh.primitive_cube_add(
    location=(-9 / 2 * tiefe + 0.5, (16 / 2 - 0.5) * breite, -4.29)
)
leg = scn.objects["Cube"]

leg.name = "Tischbein4"
leg.select_set(state=True)
bpy.ops.transform.resize(value=(0.5, 0.5, 4.5))
leg.select_set(state=False)


cupboards = []
for a in [-1, 1]:
    coords = ((-7 / 4 + 9 / 4) * tiefe, a * (16 / 2 * breite - (1.8 * breite)), -3.7)
    bpy.ops.mesh.primitive_cube_add(location=coords)
    cupboard = scn.objects["Cube"]
    cupboard.name = "cupboard_" + str(int((a + 1) / 2 + 1))
    cupboard.select_set(state=True)
    bpy.ops.transform.resize(value=(7 / 2 * tiefe, 1.8 * breite, 3.5))
    cupboards.append(cupboard)
    cupboard.select_set(state=False)
    mod_bool = scn.objects["Platte_2"].modifiers.new("my_bool_mod", "BOOLEAN")
    mod_bool.operation = "DIFFERENCE"
    mod_bool.object = cupboard
    bpy.context.view_layer.objects.active = scn.objects["Platte_2"]
    res = bpy.ops.object.modifier_apply(modifier="my_bool_mod")

for a in [-1, 1]:
    coords = ((-7 / 4 + 9 / 4) * tiefe, a * (16 / 2 * breite - (1.8 * breite)), -3.7)
    bpy.ops.mesh.primitive_cube_add(location=coords)
    cupboardb = scn.objects["Cube"]
    cupboardb.name = "cupboard_" + str(int((a + 1) / 2 + 1)) + "_in"
    cupboardb.select_set(state=True)
    bpy.ops.transform.resize(value=(7 / 2 * 1.4 * tiefe, 1.8 * breite - 0.4, 3.5 - 0.4))
    cupboardb.select_set(state=False)
    mod_bool = cupboards[int((a + 1) / 2)].modifiers.new("my_bool_mod", "BOOLEAN")
    mod_bool.operation = "DIFFERENCE"
    mod_bool.object = cupboardb
    bpy.context.view_layer.objects.active = cupboards[int((a + 1) / 2)]
    res = bpy.ops.object.modifier_apply(modifier="my_bool_mod")
    cupboard.select_set(state=False)
    cupboardb.select_set(state=True)
    bpy.ops.object.delete()

for a in [-1, 1]:
    for b in [[-4.5, 1], [-1, 0.4]]:
        coords = (
            (-7 / 4 + 9 / 4 - 2.5 + b[1]) * tiefe,
            a * (16 / 2 - 2 - 1.8) * breite,
            b[0],
        )
        bpy.ops.mesh.primitive_cube_add(location=coords)
        cupboardb = scn.objects["Cube"]
        cupboardb.name = "cupboardi_" + str(int((a + 1) / 2 + 1)) + "_behind"
        cupboardb.select_set(state=True)
        bpy.ops.transform.resize(value=(1.5 * b[1] * tiefe, 1 * breite, 1.5 * b[1]))
        cupboardb.select_set(state=False)
        mod_bool = cupboards[int((a + 1) / 2)].modifiers.new("my_bool_mod", "BOOLEAN")
        mod_bool.operation = "DIFFERENCE"
        mod_bool.object = cupboardb
        bpy.context.view_layer.objects.active = cupboards[int((a + 1) / 2)]
        res = bpy.ops.object.modifier_apply(modifier="my_bool_mod")
        cupboard.select_set(state=False)
        cupboardb.select_set(state=True)
        bpy.ops.object.delete()

# bpy.ops.mesh.primitive_cube_add(location = (-7/4+9/4,-16/2+2,-3.5))
# cupboard = scn.objects['Cube']
# cupboard.name = 'cupboard_2'
# cupboard.select = True
# bpy.ops.transform.resize(value=(7/2, 1.8, 3.5))
# cupboard.select = False
# s/(breite+tiefe)/2/math.sqrt(math.pow(breite,2)+math.pow(tiefe,2))/g

color = "663300"

r = float.fromhex(color[0:2]) / 255.0
g = float.fromhex(color[2:4]) / 255.0
b = float.fromhex(color[4:6]) / 255.0


# for l in bpy.data.lamps:
#    l.color = [r, g, b]
#    l.energy = 6


bpy.ops.object.camera_add(
    enter_editmode=False,
    location=(30, 10, 7),
    rotation=(math.pi * 1.4, -math.pi, math.pi * 1.6),
)
cam = scn.objects["Camera"]
cam.name = "cam_1"
bpy.data.cameras["Camera"].lens = 25

# bpy.ops.object.lamp_add(location=(0,0,8))
# for a in [10,-10]:
#    for b in [8,-8]:
#        bpy.ops.object.lamp_add(type='AREA',location=(a,b,8))
#        lamp = scn.objects['Area']
#        lamp.name = 'AREA-'+str(a)+'-'+str(b)
#        lamp = bpy.data.lamps['Area']
#        lamp.name = 'AREA-'+str(a)+'-'+str(b)
#        lamp.energy = 1
#        lamp.size = 10
#        lamp.shadow_ray_samples_x = 5
#        lamp.color=(lamp.color[0]-(a+10)/20/4,lamp.color[1]-(b+8)/16/4,lamp.color[2])
#        lamp.use_nodes = True


for i in [1]:
    if i == 1:
        bpy.ops.mesh.primitive_cube_add(location=(10, 10, 10))
    if i == 2:
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, -1))
    lamp = scn.objects["Cube"]
    lamp.name = "cycleslamp" + str(i)
    lamp.select_set(state=True)
    bpy.ops.transform.resize(value=(3 / i, 3 / i, 3 / i))
    bpy.data.objects["cycleslamp" + str(i)].cycles_visibility.camera = False

## Create a material.
# mat = bpy.data.materials.new(name = 'my_material')

## Set some properties of the material.
# mat.diffuse_color = (1, 0., 0.)
# mat.diffuse_shader = 'LAMBERT'
# mat.diffuse_intensity = 1.0
# mat.specular_color = (1., 1., 1.)
# mat.specular_shader = 'COOKTORR'
# mat.specular_intensity = 0.5
# mat.alpha = 1
# mat.ambient = 1

# materialart =  'WOOD'

# matname = "mat" + materialart
# texname = "tex" + materialart

# new material
# textur = bpy.data.textures.new(texname, type=materialart)
# textur.wood_type= 'RINGNOISE'
# textur.saturation = 0.0
# texture.active_texture = textur2
# material = bpy.data.materials.new(matname)
# holzmat = material
# material.texture_slots.add()
# material.active_texture = textur
# tex = bpy.data.textures.new("SomeName", type = 'IMAGE')
# tex.image = bpy.data.images.load('holz.jpg')
# material.texture_slots.add()
# material.active_texture = tex
# material.diffuse_color = (1.0, .3, 0)
# material.specular_color = (0.9, .4, 0.1)
##material.line_color = (0.9, .4, 1)
# material.mirror_color = (0.9, .4, 0.1)


# mesh.data.materials.append(material)


# obj = cube.data
# obj.materials.append(material)

# new texture
# bpy.data.textures[texname].specular_color=(0.9,0.3,0.0)
# textur.specular_color=(0.9,0.3,0.0)

# lits all properties and methods of a texture
# print(dir(textur))

# connect texture with material


mesh = cube.data
# mesh.materials.append(mat)
coords = (0, 0, -8.8 + 30)
bpy.ops.mesh.primitive_cube_add(location=coords)
cupboardb = scn.objects["Cube"]
cupboardb.name = "room"
cupboardb.select_set(state=True)
bpy.ops.transform.resize(value=(40, 50, 30))
cupboardb.select_set(state=False)

# materialart =  'MUSGRAVE'

# matname = "mat" + materialart
# texname = "tex" + materialart

# new material
# textur = bpy.data.textures.new(texname, type=materialart)
# o = scn.objects['Material']
# o.select = True
# bpy.ops.transform.resize(value=(.2, .2, .2))
# o.select = False
# textur.noise_scale=0.1
# textur.musgrave_type = 'HYBRID_MULTIFRACTAL'
# textur.saturation = 0.0
# texture.active_texture = textur2
# material = bpy.data.materials.new(matname)
# material.texture_slots.add()
# material.active_texture = textur
# material.resize(value=(0.2,0.2,0.2))
# tex = bpy.data.textures.new("SomeName", type = 'IMAGE')
# tex.image = bpy.data.images.load('wirr.jpg')
# tex.im .noise_scale=0.01
# tex.repeat_x=20
# tex.repeat_y=20
# material.texture_slots.add()
# material.active_texture = tex
# material.diffuse_color = (1.0, 1.0, 1.0)
# material.raytrace_mirror.use = True
# material.raytrace_mirror.reflect_factor = 0.4
# material.raytrace_mirror.gloss_factor = 0.9
# material.specular_color = (0.9, .4, 0.1)
##material.line_color = (0.9, .4, 1)
# material.mirror_color = (0.9, .4, 0.1)
# scn.objects['room'].data.materials.append(material)
# bpy.ops.wm.link(filepath="/home/alex/Downloads/Palm_Tree.blend")
# bpy.ops.wm.append(filepath="//Palm_Tree.blend",directory="/home/alex/Downloads",link=False)

# for lamp in bpy.data.lamps:
#    lamp.energy = 2

lightspheres = []

for a in [-1, 1]:
    for b in [-7.5, -1]:
        # bpy.ops.light.lamp_add(location=(3*tiefe,7*a*breite,b))
        bpy.ops.object.light_add(type="POINT", location=(3 * tiefe, 7 * a * breite, b))
        c = 0.0 if b == -7.5 else 0.2
        #        bpy.ops.mesh.primitive_ico_sphere_add(location=(3*tiefe,7*a*breite,b),radius=0.1)
        #        lightspheres.append((scn.objects[-1],(1.0,c,0.0,1.0)))
        # bpy.data.lamps[-1].color = (1.0,c,0.0)
        # bpy.data.lamps[-1].distance = 1.0
        # bpy.data.lamps[-1].energy = 10
        # bpy.data.lamps[-1].shadow_method = 'RAY_SHADOW'
        # bpy.data.lamps[-1].shadow_ray_samples = 3
        # print(str(dir(scn.objects[-1].data)))
        scn.objects[-1].color = (1.0, c, 0.0, 0.0)
        scn.objects[-1].data.color = (1.0, c, 0.0)
        scn.objects[-1].data.distance = 1.0
        scn.objects[-1].data.energy = 20
        # scn.objects[-1].data.shadow_method = 'RAY_SHADOW'
        # scn.objects[-1].data.shadow_ray_samples = 3


# for lamp in bpy.data.lamps:
#    lamp.shadow_method = 'RAY_SHADOW'


# Mesh\\['255_mesh_.001','255_mesh_']
# Object\\['255_mesh_.001','255_mesh_']
# Group\\255
# Image\\['blatt.jpg','holz.jpg','Render Result']
# Material\\['Material','Material.002','Material.001']
# Scene\\Scene
# Texture\\['Bild','bild','Blatt','Tex','Wood']

#          ['blatt.jpg','holz.jpg','Render Result'],
#          ['Material','Material.002','Material.001'],
#  ['Scene']
#         ['Bild','bild','Blatt','Tex','Wood']]


def import_(blendfile, locat, resiz, tree=False):
    objs = []
    for folder, things in zip(folders, inside):
        section = "\\" + folder + "\\"
        for object in things:
            filepath = blendfile + section + object
            directory = blendfile + section
            filename = object

            len1_ = len(scn.objects)
            bpy.ops.wm.append(filepath=filepath, filename=filename, directory=directory)
            len2_ = len(scn.objects)
            if len1_ < len2_:
                objs.append(scn.objects[-1])
    for obj in scn.objects:
        obj.select_set(state=False)
    if not resiz is None and not locat is None:
        for obj in inside[0]:
            obj = scn.objects[obj]
            obj.select_set(state=True)
            bpy.ops.transform.resize(value=resiz)
            obj.location = locat
            a = str(obj.name)
            if tree:
                obj.name = "tree 1 " + a
                bpy.ops.object.duplicate_move_linked()
                for obj2 in scn.objects:
                    obj2.select_set(state=False)
    return objs


folders = ["Mesh", "Object"]
inside = [["255_mesh_.001", "255_mesh_"], ["255_mesh_.001", "255_mesh_"]]
import_(
    "alxpalme.blend",
    (-13, 15, -8.8),
    (0.3, 0.3, 0.3),
    True,
)
folders = ["Mesh", "Object", "Material", "Texture"]
obj_ = ["Box01", "Box02", "Box03", "Box04", "Box05", "Box06", "Box13.Box14.Box15"]
for i in range(1, 10):
    obj_.append("Cylinder0" + str(i))
for i in range(10, 13):
    obj_.append("Cylinder" + str(i))
str_ = ""
for i in range(14, 19):
    str_ += "Cylinder" + str(i) + "."
str_ += "Cylinder"
obj_.append(str_)
str_ = ""
for i in range(21, 26):
    str_ += "Cylinder" + str(i) + "."
str_ += "Cylinder"
obj_.append(str_)
for i in range(28, 36):
    obj_.append("Cylinder" + str(i))
obj_.append("Object01")
obj_.append("Object02")
obj_.append("Shape01")
obj_.append("Sphere01")
for i in range(1, 5):
    obj_.append("Tube0" + str(i))
inside = [
    obj_,
    obj_,
    ["01 - Default", "10 - Default", "11 - Default", "13 - Default", "Material"],
    ["Tex"],
]
# print(str(obj_))
objs = import_(
    "pctower.blend", (0, 0, 0), (1, 1, 1)
)
# for obj in objs:
#    print(obj.name)
joinmerge(objs)
scn.objects["Box01"].select_set(state=True)
bpy.ops.transform.resize(value=(0.85, 0.85, 0.85))
bpy.context.view_layer.objects.active = scn.objects["Box01"]
bpy.context.object.rotation_euler = (0, 0, math.pi)
scn.objects["Box01"].location = (-0.3, 3.5 * breite, -7 + 0.4)
# 9/2*tiefe, 16/2*breite
bpy.ops.object.duplicate_move_linked(
    OBJECT_OT_duplicate={"linked": True, "mode": "TRANSLATION"},
    TRANSFORM_OT_translate={
        "value": (0, -11.5 * breite, 0),
        "constraint_axis": (False, False, False),
        "mirror": False,
        "proportional_edit_falloff": "SMOOTH",
        "proportional_size": 1,
        "snap": False,
        "snap_target": "CLOSEST",
        "snap_point": (0, 0, 0),
        "snap_align": False,
        "snap_normal": (0, 0, 0),
        "texture_space": False,
        "release_confirm": False,
        "use_proportional_connected": False,
        "use_proportional_projected": False,
        "orient_matrix_type": "GLOBAL",
        "orient_type": "GLOBAL",
    },
)
scn.objects["Box01"].select_set(state=False)


folders = ["Mesh", "Object", "Material", "Texture", "Image"]
# folders = ['Mesh','Object']
obj_ = ["Cube", "Keyboard"]
for a in range(5, 6):
    obj_.append("Plane.00" + str(a))
obj_.append("Plane")
mati_ = ["Material"]
for a in range(0, 8):
    mati_.append("Material.00" + str(a))
texti_ = ["Texture", "Texture.001", "Texture.002"]
imagi = [
    "Bildschirmfoto 2011-1",
    "Dots.png",
    "keyboard.jpg.001",
    "keyboard.jpg",
    "Mac Desktop.png",
    "Mac_back.png",
    "Mac_front.png",
    "Mac_side.png",
    "mouse side.jpg",
    "Render Result",
]
# meshi=['Cube.001','Cube']
# meshi=['Cube']
meshi = []
for a in range(5, 6):
    meshi.append("Plane.00" + str(a))
meshi.append("Plane")
inside = [meshi, obj_, mati_, texti_, imagi]
# print(str(meshi))
# inside = [meshi,obj_]
# print(str(obj_))
objs = import_("Mac_2.blend", None, None)
scn.objects["Cube"].name = "Halterung"


# scn.objects['Plane.005']


scn.objects["Plane"].select_set(state=False)
scn.objects["Keyboard"].select_set(state=True)

bpy.context.view_layer.objects.active = scn.objects["Keyboard"]
bpy.context.object.rotation_euler = (math.pi / 12, 0, math.pi / 2)
bpy.ops.transform.resize(value=(2, 2, 2))
scn.objects["Keyboard"].location = (2, -3, 0.45)
scn.objects["Keyboard"].select_set(state=False)


for o in [-1, -2]:
    bpy.data.objects[o].select_set(state=True)
    bpy.data.objects[o].location = (-13, -15, -8.8)
    bpy.data.objects[o].select_set(state=False)


# mist = bpy.data.worlds["World"].mist_settings
# mist.use_mist = True
# mist.start = 25
# mist.depth = 50
# cube = scn.objects['Cube'].name = 'ExCube'

bpy.ops.mesh.primitive_cube_add(location=(-(9 / 2 / 2 * tiefe), 0, 2))
scn = bpy.context.scene
cube = scn.objects["Cube"]
# bpy.context.scene.objects[0].select = True
bpy.ops.transform.resize(value=(9 / 2 / 2 * tiefe, 16 / 2 * breite, 0.2))
bpy.ops.mesh.primitive_cylinder_add(
    vertices=128,
    radius=5 * (breite + tiefe) / math.pi,
    location=(5.5 * tiefe - (9 / 2 / 2 * tiefe) * 2, 0, 3),
)
bpy.ops.transform.resize(value=(1 * tiefe / 1.5, 1.5 * breite, 4))
cylinder = scn.objects["Cylinder"]
cube.name = "Oberplatte"

oben = [cube]
obenname = [cube.name]

for a in [-3, 3]:
    bpy.ops.mesh.primitive_cube_add(
        location=(-(9 / 2 / 2 * tiefe), a * (16 / 2 * breite / 3 - 0.25), 1)
    )
    scn = bpy.context.scene
    oben.append(scn.objects["Cube"])
    # bpy.context.scene.objects[0].select = True
    bpy.ops.transform.resize(value=(9 / 2 / 2 * tiefe, 0.5, 1))
    oben[-1].name = "Oben seitlich " + str(a)
    obenname.append(oben[-1].name)
    bpy.ops.mesh.primitive_cube_add(
        location=(-tiefe, a * (16 / 2 * breite / 3 - 0.25) - 2.4 / a, 1)
    )
    bpy.ops.transform.resize(value=(0.5 * 16 / 9, 0.5, 0.5))
    oben.append(scn.objects["Cube"])
    oben[-1].name = "Drinnen seitlich " + str(a)
    obenname.append(oben[-1].name)

screenlocations = []
screenlocations.append(copy.deepcopy(oben[2].location))
screenlocations.append(copy.deepcopy(oben[4].location))
# print(str(screenlocation))

differ(oben[1], oben[2])
differ(oben[3], oben[4])

bpy.ops.object.select_all(action="DESELECT")
oben[0].select_set(state=False)
oben[1].select_set(state=False)
oben[2].select_set(state=True)
oben[3].select_set(state=False)
oben[4].select_set(state=True)
bpy.ops.object.delete()


oben = [oben[0], oben[1], oben[3]]

for a in oben:
    mod_bool = a.modifiers.new("my_bool_mod", "BOOLEAN")
    mod_bool.operation = "DIFFERENCE"
    mod_bool.object = cylinder
    bpy.context.view_layer.objects.active = a
    res = bpy.ops.object.modifier_apply(modifier="my_bool_mod")
    a.select_set(state=False)
    cylinder.select_set(state=True)

cylinder.select_set(state=True)
bpy.ops.object.delete()


# flurbreite = 216
# deckenwanddicke = 21
# lukelaenger=1.5
# treppenlaengenbereich = (165 + 6.65 + 20 - 20 + 63.5) * lukelaenger
# lukenende = flurlaenge /2 - 63.5 - treppenlaengenbereich /2 + 40 - ( treppenlaengenbereich )
# lukenmitte = -flurbreite + 59 + deckenwanddicke
# coords = [(lukenmitte,lukenende,224),(lukenmitte,(lukenende + flurlaenge) / 2-110,-110), (lukenmitte,flurlaenge,-224)]
# coords2 = [(lukenmitte+120,lukenende,224),(lukenmitte+120,(lukenende + flurlaenge) / 2-110,-110), (lukenmitte+120,flurlaenge,-224)]
# rot,grün,blau = x,y,z
coords = []
coords2 = []
coords3 = []
coords4 = []
ome = math.pow(3, 2)
for x2 in range(-int(1750 / 2), int(1750 / 2)):
    x = x2 / 100
    normalverteilung = (
        1 / (math.sqrt(2 * math.pi * ome)) * math.exp(-((x) * (x)) / (2 * ome))
    )
    coords.append((normalverteilung * 60 - 6.6, x, 0 - 0.1 - 0.3))
    coords2.append((normalverteilung * 60 - 6.6, x, 2 - 0.2 + 0.4))

for i, x2 in enumerate(range(-int(1750 / 2), int(1750 / 2))):
    if x2 < 0:
        coords3.append(coords2[i])
    else:
        coords4.append(coords2[int(len(coords2) * 1.5) - i - 1])

coords.append(coords[0])
coords2.append(coords2[0])

coords5 = []
coords6 = []
for x2 in range(-21, 22):
    x = x2 / 10
    y = math.sin(-x) * (x * x) + 0.5 * x
    coords5.append((x / 4.3 * 6.8 * tiefe - 1.4, 0 - 16 / 2 * breite, y + 2.7))
    coords6.append((x / 4.3 * 6.8 * tiefe - 1.4, 0.4 - 16 / 2 * breite, y + 2.7))

for coordsx in [coords5, coords6]:
    coordsx.append((coordsx[-1][0], coordsx[-1][1], 0.2))
    coordsx.append((coordsx[0][0], coordsx[0][1], 0.2))
    coordsx.append((coordsx[0][0], coordsx[0][1], coordsx[0][2]))

coords11 = []
coords12 = []
coords13 = []
coords14 = []
for x2 in range(-500, 501):
    x = x2 / 100
    y = math.cos(x * 2) + 0.08 * x * x - 0.001 * x * x * x * x + math.cos(x * 8) / 4
    for i, coordsx in enumerate([coords11, coords12]):
        coordsx.append((-9 / 2 * tiefe + i * 0.4, x / 10 * breite * 16, y + 5))
    for i, coordsx in enumerate([coords13, coords14]):
        coordsx.append((-9 / 2 * tiefe + i * 0.4, x / 10 * breite * 16, 0.2))
coords15 = [coords11[0], coords13[0], coords13[-1], coords11[-1]]
coords16 = [coords12[0], coords14[0], coords14[-1], coords12[-1]]

coords7 = []
coords8 = []
coords9 = []
coords10 = []
flag = 0
for i, coordsx in enumerate([coords5, coords6]):
    for coord in coordsx:
        # for coordsx2,coordsx3 in zip([coords7,coords9],[coords8,coords10]):
        for coordsx2, coordsx3 in zip([coords7, coords9], [coords8, coords10]):
            # if coord[2]-2.7 > -0.62 and flag == 0: # wenn in der mitte der analysis funktion
            if i < len(coordsx) - 2:  # wenn in der mitte der analysis funktion
                # print(str(coord))
                coordsx2.append(coord)
                coordsx3.append(coordsx[-2])
            else:
                flag = 1


# coords = [(1,1,0),(2,2,0),(5,3,0)]
# coords2 = [(1,1,3),(2,2,3),(5,3,3)]
# curveData = bpy.data.curves.new('myCurve', type='CURVE')

curvyobj(coords, coords2)
curvyobj(coords3, coords4)
curvyobj(coords5, coords6)
curvyobj(coords7, coords8)
curvyobj(coords9, coords10)
curvyobj(coords11, coords12)
curvyobj(coords11, coords13)
curvyobj(coords12, coords14)
curvyobj(coords15, coords16)
tojoin = []
for i in range(5, 10):
    tojoin.append(scn.objects["wave.00" + str(i)])

joinmerge([scn.objects["wave.001"], scn.objects["wave.003"]])
joinmerge(tojoin)

tojoin = []
for i in range(10, 18):
    tojoin.append(scn.objects["wave.0" + str(i)])
joinmerge(tojoin)

bpy.ops.object.select_all(action="DESELECT")
scn.objects["wave.005"].select_set(state=True)
bpy.ops.object.duplicate_move(
    OBJECT_OT_duplicate={"linked": False, "mode": "TRANSLATION"},
    TRANSFORM_OT_translate={
        "value": (0, -0.4 + 16 * breite, 0),
        "constraint_axis": (False, False, False),
        "mirror": False,
        "proportional_edit_falloff": "SMOOTH",
        "proportional_size": 1,
        "snap": False,
        "snap_target": "CLOSEST",
        "snap_point": (0, 0, 0),
        "snap_align": False,
        "snap_normal": (0, 0, 0),
        "texture_space": False,
        "release_confirm": False,
        "use_proportional_connected": False,
        "use_proportional_projected": False,
        "orient_matrix_type": "GLOBAL",
        "orient_type": "GLOBAL",
    },
)

bm = bmesh.new()
middlehigh = scn.objects["wave.001"].data
# bpy.context.view_layer.objects.active = middlehigh
# bpy.ops.object.editmode_toggle()
bm.from_mesh(middlehigh)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
bm.to_mesh(middlehigh)
middlehigh.update()
bm.clear()
bm.free()
# bpy.ops.object.editmode_toggle()

cylinders = []
bereich = [-5, -1.5, 1.5, 5]
for a in bereich:
    if a in [-5, 5]:
        #        bpy.ops.object.lamp_add(location=(-3.6*tiefe,a*breite,0))
        bpy.ops.object.light_add(type="POINT", location=(-3.6 * tiefe, a * breite, 0))
        scn.objects[-1].data.energy = 20
        # bpy.ops.mesh.primitive_ico_sphere_add(location=(-3.6*tiefe,a*breite,0),radius=0.1)
        # lightspheres.append((scn.objects[-1], (1, 1, 1, 1.0)))
    #    bpy.ops.object.lamp_add(location=(-3.6*tiefe,a*breite,2))
    bpy.ops.object.light_add(type="POINT", location=(-3.6 * tiefe, a * breite, 2))
    scn.objects[-1].data.energy = 20
    #    bpy.ops.mesh.primitive_ico_sphere_add(location=(-3.6*tiefe,a*breite,2),radius=0.1)
    #    lightspheres.append((scn.objects[-1],(1,1,1, 1.0)))

    bpy.ops.mesh.primitive_cylinder_add(
        vertices=128,
        radius=3 * (breite + tiefe) / math.pi,
        location=(-3.6 * tiefe, a * breite, 0),
    )
    bpy.ops.transform.resize(value=(0.2, 0.2, 10))
    cylinder = scn.objects["Cylinder"]
    cylinder.name = "hole_" + str(a)
    cylinders.append(cylinder)
    if a in [-5, 5]:
        differ(scn.objects["Tischplatte"], cylinder)
    differ(scn.objects["Oberplatte"], cylinder)
    differ(scn.objects["wave.001"], cylinder)
    cylinder.select_set(state=True)
    scn.objects["Tischplatte"].select_set(state=False)
    scn.objects["Oberplatte"].select_set(state=False)
    scn.objects["wave.001"].select_set(state=False)
    bpy.ops.object.delete()

# flurlaenge = 168+285+5
differ(scn.objects["Tischplatte"], scn.objects["wave.001"])

bpy.ops.mesh.primitive_cube_add(
    location=(
        9 / 2 * tiefe + (9 / 6 * tiefe),
        -16 / 2 * breite + (16 / 10 * breite),
        -4.5 + 0.2,
    )
)
cube = scn.objects["Cube"]
cube.select_set(state=True)
# print(bpy.context.scene.objects[0].name)
bpy.ops.transform.resize(value=(9 / 6 * tiefe, 16 / 10 * breite + 0.1, 4.5 + 0.1))
cube.select_set(state=False)
davor = scn.objects["Cube"]
davor.name = "davor"
davor.select_set(state=True)
# bpy.ops.object.editmode_toggle()


me = bpy.context.object.data

bm = bmesh.new()
bm.from_mesh(me)

# alx
EPSILON = 1.0e-5
for i, vert in enumerate(bm.verts):
    # if -EPSILON <= vert.co.x <= EPSILON:
    if i < 2:
        vert.select = True
        vert.co = vert.co[0] - tiefe, vert.co[1], vert.co[2]
# for edge in bm.edges:
#    if edge.verts[0].select and edge.verts[1].select:
#        edge.select = True

# bpy.ops.object.editmode_toggle()

bm.to_mesh(me)
bm.free()
# bpy.ops.object.duplicate_move_linked(OBJECT_OT_duplicate={"linked":True, "mode":'TRANSLATION'},TRANSFORM_OT_translate=(0,2*(16/2 * breite - (16/10*breite)),0))
bpy.ops.object.duplicate_move(
    OBJECT_OT_duplicate={"linked": False, "mode": "TRANSLATION"},
    TRANSFORM_OT_translate={
        "value": (0, 2 * (16 / 2 * breite - (16 / 10 * breite)), 0),
        "constraint_axis": (False, False, False),
        "mirror": False,
        "proportional_edit_falloff": "SMOOTH",
        "proportional_size": 1,
        "snap": False,
        "snap_target": "CLOSEST",
        "snap_point": (0, 0, 0),
        "snap_align": False,
        "snap_normal": (0, 0, 0),
        "texture_space": False,
        "release_confirm": False,
        "use_proportional_connected": False,
        "use_proportional_projected": False,
        "orient_matrix_type": "GLOBAL",
        "orient_type": "GLOBAL",
    },
)
davor.select_set(state=False)
bpy.context.object.rotation_euler = (math.pi, 0, 0)
davor.name = "davor.002"

scn.objects["davor.001"].name = "davor"
# bpy.ops.object.select_all(action='DESELECT')
for todiff in [scn.objects["davor"], scn.objects["davor.002"]]:
    for difffrom in [
        scn.objects["Tischplatte"],
        scn.objects["cupboard_1"],
        scn.objects["cupboard_2"],
    ]:
        differ(difffrom, todiff)
bpy.ops.object.select_all(action="DESELECT")


for torsize in [scn.objects["davor"], scn.objects["davor.002"]]:
    torsize.select_set(state=True)
    bpy.ops.transform.resize(value=(1, 1 / (16 / 10 * breite + 0.1), 1 / (4.5 + 0.1)))
    bpy.ops.transform.resize(value=(1, 16 / 10 * breite, 3))
    torsize.location.z -= 1.5
    torsize.select_set(state=False)
# 9/2*tiefe+(9/6*tiefe), -16/2 * breite + (16/10*breite), -4.5+0.2)
for a, obj in zip([-1, 1], [scn.objects["davor"], scn.objects["davor.002"]]):
    createCube(
        9 / 2 * tiefe + (9 / 6 * tiefe),
        a * (16 / 2 * breite - (16 / 10 * breite)),
        -4.5 + 0.2 - 1.5,
        9 / 6 * tiefe * 4,
        16 / 10 * breite - 0.3,
        3 - 0.3,
    )
    differ(obj, scn.objects["Cube"])
    bpy.ops.object.select_all(action="DESELECT")
    scn.objects["Cube"].select_set(state=True)
    bpy.ops.object.delete()


for davorz in [scn.objects["davor"], scn.objects["davor.002"]]:
    createCube(
        davorz.location.x,
        davorz.location.y,
        davorz.location.z,
        9 / 12 * tiefe - 0.1,
        0.2,
        2.9,
    )
    scn.objects["Cube"].name = davorz.name + "1"
    createCube(
        davorz.location.x,
        davorz.location.y,
        davorz.location.z,
        9 / 12 * tiefe - 0.1,
        16 / 10 * breite - 0.1,
        0.2,
    )
    scn.objects["Cube"].name = davorz.name + "2"

    unioner(davorz, scn.objects[davorz.name + "1"])
    unioner(davorz, scn.objects[davorz.name + "2"])

    davorz.select_set(state=False)
    scn.objects[davorz.name + "1"].select_set(state=True)
    scn.objects[davorz.name + "2"].select_set(state=True)
    bpy.ops.object.delete()
# scn.objects['davor'].select = True


# for i,davors in enumerate([scn.objects['davor'],scn.objects['davor.002']]):
#    createCube(davors.location.x,davors.location.y,davors.location.z,9/6*tiefe, 0.2, 4.5+0.1)
#    scn.objects['Cube'].name=davors.name+str(i)
#    createCube(davors.location.x,davors.location.y,davors.location.z,9/6*tiefe, 16/10*breite+0.1, 0.2)
#    scn.objects['Cube'].name=davors.name+str(i+2)

# for mesh in bpy.context.scene.objects:
#    if mesh.name in ['Tischplatte','Tischbein1','Tischbein2','Tischbein3','Tischbein4','Platte_2','cupboard_1','cupboard_2','Oberplatte'] or mesh.name in obenname:
#        mesh.data.materials.append(holzmat)

image_path = "holz2.jpg"

mat = bpy.data.materials.new("holz")
mat.use_nodes = True
nt = mat.node_tree
nodes = nt.nodes
links = nt.links
while nodes:
    nodes.remove(nodes[0])
output = nodes.new("ShaderNodeOutputMaterial")
diffuse = nodes.new("ShaderNodeBsdfDiffuse")
texture = nodes.new("ShaderNodeTexImage")
texture.projection = "BOX"
uvmap = nodes.new("ShaderNodeTexCoord")
bump = nodes.new("ShaderNodeBump")
texture.image = bpy.data.images.load(image_path)
links.new(output.inputs["Surface"], diffuse.outputs["BSDF"])
links.new(diffuse.inputs["Color"], texture.outputs["Color"])
links.new(texture.inputs["Vector"], uvmap.outputs["Generated"])
links.new(bump.inputs["Normal"], texture.outputs["Color"])
links.new(diffuse.inputs["Normal"], bump.outputs["Normal"])

for mesh in bpy.context.scene.objects:
    if (
        mesh.name
        in [
            "wave.010",
            "wave.005",
            "wave.003",
            "Cube.001",
            "wave.001",
            "davor",
            "davor.002",
            "tree 1 255_mesh_.000",
            "Tischplatte",
            "Tischbein1",
            "Tischbein2",
            "Tischbein3",
            "Tischbein4",
            "Platte_2",
            "cupboard_1",
            "cupboard_2",
            "Oberplatte",
        ]
        or mesh.name in obenname
    ):
        mesh.data.materials.clear()
        mesh.data.materials.append(mat)
# scn.render.engine =
joinmerge1 = []
joinmerge2 = []
for mesh in bpy.context.scene.objects:
    if (
        mesh.name
        in [
            "wave.010",
            "wave.005",
            "wave.003",
            "Cube.001",
            "wave.001",
            "Tischplatte",
            "Tischbein1",
            "Tischbein2",
            "Tischbein3",
            "Tischbein4",
            "Platte_2",
            "cupboard_1",
            "cupboard_2",
            "Oberplatte",
        ]
        or mesh.name in obenname
    ):
        joinmerge1.append(mesh)
for mesh in bpy.context.scene.objects:
    if mesh.name in ["davor", "davor.002"]:
        joinmerge2.append(mesh)
# joinmerge(joinmerge1)
# joinmerge(joinmerge2)
bpy.context.scene.render.engine = "CYCLES"

for i in [1]:
    mat = bpy.data.materials.new("lampmat")
    mat.use_nodes = True
    nt = mat.node_tree
    nodes = nt.nodes
    links = nt.links
    while nodes:
        nodes.remove(nodes[0])
    output = nodes.new("ShaderNodeOutputMaterial")
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs[1].default_value = 5
    links.new(output.inputs["Surface"], emission.outputs["Emission"])
    scn.objects["cycleslamp" + str(i)].data.materials.append(mat)

for kugel, farbe in lightspheres:
    mat = bpy.data.materials.new("lampmat")
    mat.use_nodes = True
    nt = mat.node_tree
    nodes = nt.nodes
    links = nt.links
    while nodes:
        nodes.remove(nodes[0])
    output = nodes.new("ShaderNodeOutputMaterial")
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs[1].default_value = 100
    emission.inputs[0].default_value = farbe
    links.new(output.inputs["Surface"], emission.outputs["Emission"])
    kugel.data.materials.append(mat)


for i in [1]:
    mat = bpy.data.materials.new("lampmat2")
    mat.use_nodes = True
    nt = mat.node_tree
    nodes = nt.nodes
    links = nt.links
    while nodes:
        nodes.remove(nodes[0])
    output = nodes.new("ShaderNodeOutputMaterial")
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs[1].default_value = 2
    links.new(output.inputs["Surface"], emission.outputs["Emission"])
    image_path = "linux_kde_plasma_desktop_by_vincecrue_d48eqs6-fullview.jpg"
    texture = nodes.new("ShaderNodeTexImage")
    texture.projection = "BOX"
    texture.image = bpy.data.images.load(image_path)
    texture.texture_mapping.rotation = (math.pi, 0, math.pi / 2)
    # bpy.context.object.rotation_euler = (-math.pi/2,0,math.pi/2)
    links.new(emission.inputs["Color"], texture.outputs["Color"])


for mesh in bpy.context.scene.objects:
    if mesh.name in ["Plane.005"]:
        #        scn.objects['Plane.005'].select = True
        #        bpy.context.object.rotation_euler = (math.pi/2,0,-math.pi/2)
        mesh.data.materials.clear()
        mesh.data.materials.append(mat)
#        bpy.context.object.rotation_euler = (-math.pi/2,0,math.pi/2)
#        scn.objects['Plane.005'].select = False


# scn.objects['Plane.005']

# for mesh in bpy.context.scene.objects:
#    if mesh.name in ['cycleslamp2','cyleslamp1']:
#        mesh.data.materials.append(mat)
# scn.objects['cycleslamp'+str(i)].data.materials.append(mat)

mat = bpy.data.materials.new("pflanze")
image_path = "blatt.jpg"
mat.use_nodes = True
nt = mat.node_tree
nodes = nt.nodes
links = nt.links
while nodes:
    nodes.remove(nodes[0])
output = nodes.new("ShaderNodeOutputMaterial")
diffuse = nodes.new("ShaderNodeBsdfDiffuse")
texture = nodes.new("ShaderNodeTexImage")
texture.projection = "BOX"
uvmap = nodes.new("ShaderNodeTexCoord")
bump = nodes.new("ShaderNodeBump")
texture.image = bpy.data.images.load(image_path)
links.new(output.inputs["Surface"], diffuse.outputs["BSDF"])
links.new(diffuse.inputs["Color"], texture.outputs["Color"])
links.new(texture.inputs["Vector"], uvmap.outputs["Generated"])
links.new(bump.inputs["Normal"], texture.outputs["Color"])
links.new(diffuse.inputs["Normal"], bump.outputs["Normal"])


for mesh in bpy.context.scene.objects:
    if mesh.name in ["tree 1 255_mesh_"]:
        mesh.data.materials.clear()
        mesh.data.materials.append(mat)
matwood = mat

mat = bpy.data.materials.new("Raumtex")
# image_path = 'PS-Lemon-Stone-grey58b2fc1bca16c.jpg'
mat.use_nodes = True
nt = mat.node_tree
nodes = nt.nodes
links = nt.links
while nodes:
    nodes.remove(nodes[0])
output = nodes.new("ShaderNodeOutputMaterial")
diffuse = nodes.new("ShaderNodeBsdfDiffuse")
texture = nodes.new("ShaderNodeTexBrick")
texture.inputs[2].default_value = (0.7, 0.7, 0.7, 1)
texture.inputs[3].default_value = (0.4, 0.4, 0.4, 1)
texture.inputs[4].default_value = 13
mix = nodes.new("ShaderNodeMixShader")
mix.inputs[0].default_value = 0.7
glossy = nodes.new("ShaderNodeBsdfGlossy")
glossy.distribution = "SHARP"
glossy2 = nodes.new("ShaderNodeBsdfGlossy")
uvmap = nodes.new("ShaderNodeTexCoord")
bump = nodes.new("ShaderNodeBump")
bump.inputs[0].default_value = 100
bump.inputs[1].default_value = 10
texture.inputs[4].default_value = 13
# texture.image = bpy.data.images.load(image_path)
links.new(output.inputs["Surface"], mix.outputs["Shader"])
links.new(diffuse.inputs["Color"], texture.outputs["Color"])
links.new(glossy.inputs["Color"], texture.outputs["Color"])
links.new(texture.inputs["Vector"], uvmap.outputs["Generated"])
links.new(texture.inputs[1], glossy2.outputs["BSDF"])
links.new(bump.inputs["Height"], texture.outputs["Color"])
links.new(diffuse.inputs["Normal"], bump.outputs["Normal"])
links.new(mix.inputs[1], diffuse.outputs["BSDF"])
links.new(mix.inputs[2], glossy.outputs["BSDF"])


# 2019-11-05
# for mesh in bpy.context.scene.objects:
#    if mesh.name in ['room']:
#        mesh.data.materials.clear()
#        mesh.data.materials.append(mat)

bpy.data.worlds["World"].use_nodes = True
# scn.render.layers[0].cycles.use_mist = True
# bpy.context.scene.render.layers[0].layers[5] = True
# scn.cycles.layers[5] = True
# render_layers[0] = True
# mist = bpy.data.worlds["World"].mist_settings
##mist.use_mist = True
# mist.start = 25
# mist.depth = 50

# scn.objects['Plane'].select = True
# bpy.ops.object.mode_set(mode = 'EDIT')
# bm = bmesh.from_edit_mesh(cn.objects['Plane'].data)
# bm.select_mode = {'FACE'}


bpy.ops.object.select_all(action="DESELECT")
scn.objects["Plane.005"].select_set(state=True)
bpy.ops.object.duplicate_move(
    OBJECT_OT_duplicate={"linked": False, "mode": "TRANSLATION"},
    TRANSFORM_OT_translate={
        "value": (0, 0, 0),
        "constraint_axis": (False, False, False),
        "mirror": False,
        "proportional_edit_falloff": "SMOOTH",
        "proportional_size": 1,
        "snap": False,
        "snap_target": "CLOSEST",
        "snap_point": (0, 0, 0),
        "snap_align": False,
        "snap_normal": (0, 0, 0),
        "texture_space": False,
        "release_confirm": False,
        "use_proportional_connected": False,
        "use_proportional_projected": False,
        "orient_matrix_type": "GLOBAL",
        "orient_type": "GLOBAL",
    },
)
scn.objects["Plane.001"].select_set(state=True)
bpy.ops.transform.resize(value=(1 / 2, 1 / 2, 1 / 2))
bpy.ops.object.select_all(action="DESELECT")
scn.objects["Plane.005"].select_set(state=True)
bpy.ops.object.duplicate_move(
    OBJECT_OT_duplicate={"linked": False, "mode": "TRANSLATION"},
    TRANSFORM_OT_translate={
        "value": (0, 0, 0),
        "constraint_axis": (False, False, False),
        "mirror": False,
        "proportional_edit_falloff": "SMOOTH",
        "proportional_size": 1,
        "snap": False,
        "snap_target": "CLOSEST",
        "snap_point": (0, 0, 0),
        "snap_align": False,
        "snap_normal": (0, 0, 0),
        "texture_space": False,
        "release_confirm": False,
        "use_proportional_connected": False,
        "use_proportional_projected": False,
        "orient_matrix_type": "GLOBAL",
        "orient_type": "GLOBAL",
    },
)
scn.objects["Plane.005"].select_set(state=False)
bpy.ops.transform.resize(value=(1 / 2, 1 / 2, 1 / 2))

bpy.ops.object.select_all(action="DESELECT")
joinmerge([scn.objects["Plane"], scn.objects["Plane.005"], scn.objects["Halterung"]])
bpy.context.view_layer.objects.active = scn.objects["Plane"]
bpy.context.object.rotation_euler = (-math.pi / 2, 0, math.pi / 2)
scn.objects["Plane"].select_set(state=True)
# scn.objects['Plane.005'].select_set(state=True)
# scn.objects['Halterung'].select_set(state=True)
bpy.ops.transform.resize(value=(2, 2, 2))
scn.objects["Plane"].location = (-4, 0, 5.1)


miniscreens = [scn.objects["Plane.001"], scn.objects["Plane.002"]]
for screens, locat in zip(miniscreens, screenlocations):
    #    screens.location.x -= screens.location.x
    #    screens.location.y -= screens.location.y
    #    screens.location.z -= screens.location.z
    screens.location = locat
    screens.location.x = screens.location.x + 0.05
    screens.location.z = screens.location.z - 0.05

miniscreens[0].location.y = miniscreens[0].location.y - 0.3
miniscreens[1].location.y = miniscreens[1].location.y + 0.3
bpy.context.view_layer.objects.active = miniscreens[1]
bpy.context.object.rotation_euler = (-math.pi / 2, 0, math.pi)

bpy.ops.object.select_all(action="DESELECT")
scn.objects["myCurve"].select_set(state=True)
for i in range(1, 9):
    scn.objects["myCurve.00" + str(i)].select_set(state=True)
for i in range(10, 19):
    try:
        scn.objects["myCurve.0" + str(i)].select_set(state=True)
    except:
        break

for i in range(20, 29):
    try:
        scn.objects["myCurve.0" + str(i)].select_set(state=True)
    except:
        break

bpy.ops.object.delete()
bpy.ops.object.select_all(action="DESELECT")


clipend = 1000000

for a in bpy.context.screen.areas:
    if a.type == "VIEW_3D":
        for s in a.spaces:
            if s.type == "VIEW_3D":
                s.clip_end = clipend
for cam_ in bpy.data.cameras:
    cam_.clip_end = clipend

bpy.data.cameras["Camera"].lens = 20
scn.frame_start = 0
# scn.frame_end = 799
scn.frame_end = 1300 * mult_frames - 1
scn.render.fps = 25
bpy.data.scenes["Scene"].cycles.samples = 150
bpy.data.scenes["Scene"].render.image_settings.file_format = "AVI_RAW"
# bpy.data.scenes['Scene'].render.filepath = '/media/alex/1800btrfs/blender/treppe'
if not socket.gethostname() == "d2b":
    # bpy.data.scenes['Scene'].render.filepath = '/media/diener2ssh/usb1/data/blender/results/'
    bpy.data.scenes["Scene"].render.filepath = "/media/alex/sda1-ssd-btrfs/blenderanim/"
else:
    bpy.data.scenes["Scene"].render.filepath = "/media/usb1/data/blender/results/"
bpy.data.scenes["Scene"].render.use_overwrite = False
scn.render.resolution_percentage = 100


def set4anim(objd, objs, fram, loca, rota=None):
    if not loca is None:
        objs.location = loca
        objs.keyframe_insert(data_path="location", frame=fram)
    if not rota is None:
        if not rota[0] is None:
            objs.rotation_euler[0] = rota[0]
        if not rota[1] is None:
            objs.rotation_euler[1] = rota[1]
        if not rota[2] is None:
            objs.rotation_euler[2] = rota[2]
        objs.keyframe_insert(data_path="rotation_euler", frame=fram)


camd = bpy.data.cameras["Camera"]
cams = scn.objects["cam_1"]
lampd = bpy.data.objects["cycleslamp1"]
lamps = scn.objects["cycleslamp1"]
# mult_frames = 4

cams.keyframe_insert(data_path="location", frame=0.0 * mult_frames)
cams.keyframe_insert(data_path="rotation_euler", frame=0.0 * mult_frames)
lamps.keyframe_insert(data_path="location", frame=0.0 * mult_frames)
lamps.keyframe_insert(data_path="rotation_euler", frame=0.0 * mult_frames)

# print(str(cams.rotation_axis_angle[0])+" "+str(cams.rotation_axis_angle[1])+" "+str(cams.rotation_axis_angle[2])+" "+str(cams.rotation_axis_angle[3]))
set4anim(
    camd,
    cams,
    100.0 * mult_frames,
    (cams.location[0] - 5, -cams.location[1], 3),
    (math.pi * 1.4, -math.pi, math.pi * 1.6 - math.pi / 4),
)
set4anim(lampd, lamps, 100.0 * mult_frames, (lamps.location[0], 0, 1), None)
set4anim(
    camd,
    cams,
    200.0 * mult_frames,
    (cams.location[0] - 10, 0, -4),
    (math.pi * 1.4, -math.pi, math.pi * 1.6),
)
set4anim(lampd, lamps, 200.0 * mult_frames, (lamps.location[0] - 4, -3, -4), None)
set4anim(
    camd,
    cams,
    300.0 * mult_frames,
    (cams.location[0] - 20, 0, -5),
    (math.pi * 1.4 + math.pi / 2, -math.pi, math.pi * 1.6),
)
set4anim(lampd, lamps, 300.0 * mult_frames, (lamps.location[0] - 5, 0, -5), None)
set4anim(
    camd,
    cams,
    400.0 * mult_frames,
    (cams.location[0] - 20, 0, 18),
    (math.pi * 1.4 + math.pi / 2 + math.pi / 3, 0, math.pi * 1.6),
)
set4anim(lampd, lamps, 350.0 * mult_frames, (0, 0, 22), None)
set4anim(
    camd,
    cams,
    500.0 * mult_frames,
    (0, -30, 10),
    (math.pi * 1.4 + math.pi, 0, math.pi * 1.6 + math.pi / 2),
)
set4anim(lampd, lamps, 450.0 * mult_frames, (0, 10, 22), None)
set4anim(
    camd,
    cams,
    600.0 * mult_frames,
    (30, -20, 0),
    (math.pi * 1.4 + math.pi, 0, math.pi * 1.6 + math.pi / 2 + math.pi / 4),
)
set4anim(
    camd,
    cams,
    700.0 * mult_frames,
    (7, 0, 27),
    (
        math.pi * 1.4 + math.pi - math.pi / 4,
        0,
        math.pi * 1.6 + math.pi / 2 + math.pi / 4,
    ),
)
set4anim(lampd, lamps, 800.0 * mult_frames, (10, 10, 10), None)
set4anim(
    camd,
    cams,
    800.0 * mult_frames,
    (30, 10, 7),
    (math.pi * 1.4, -math.pi, math.pi * 1.6),
)
set4anim(
    camd,
    cams,
    900.0 * mult_frames,
    (12.3, 23.8, 7),
    (math.pi * 1.4, -math.pi, math.pi * 1.72),
)
set4anim(
    camd,
    cams,
    1000.0 * mult_frames,
    (4, 16, 13),
    (math.pi * 1.26, -math.pi * 1.11, math.pi * 1.7),
)
set4anim(
    camd,
    cams,
    1100.0 * mult_frames,
    (11.1, -5, 3.3),
    (math.pi * 1.48, -math.pi * 1.02, math.pi * 1.42),
)
set4anim(
    camd,
    cams,
    1200.0 * mult_frames,
    (24, -9.76, -2),
    (math.pi * 1.48, -math.pi * 1.02, math.pi * 1.42),
)
set4anim(
    camd,
    cams,
    1300.0 * mult_frames,
    (30, 10, 7),
    (math.pi * 1.4, -math.pi, math.pi * 1.6),
)

# bpy.ops.screen.animation_play()
scn.render.image_settings.color_mode = "RGB"
scn.render.image_settings.file_format = "BMP"
scn.render.use_overwrite = False
scn.render.use_placeholder = True
scn.camera = cams

if socket.gethostname() == "d2b":
    for scene in bpy.data.scenes:
        scn.render.threads_mode = "FIXED"
        scn.render.threads = 4

# #bpy.ops.render.render(animation=True)

# 2019-11-02
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0.5

bpy.ops.object.lightprobe_add(type="GRID", location=(0, 0, 21.2))
grid = scn.objects["IrradianceVolume"]
bpy.ops.object.select_all(action="DESELECT")
grid.select_set(state=True)
bpy.ops.transform.resize(value=(40, 50, 30))
grid.data.grid_resolution_x = 16
grid.data.grid_resolution_y = 16
grid.data.grid_resolution_z = 16
grid.data.clip_end = 70

bpy.ops.object.lightprobe_add(type="CUBEMAP", location=(0, 0, 21.2))
grid = scn.objects["ReflectionCubemap"]
bpy.ops.object.select_all(action="DESELECT")
grid.select_set(state=True)
bpy.ops.transform.resize(value=(40, 50, 30))
grid.data.influence_type = "BOX"

# scn.objects['cycleslamp1'].hide_viewport = True
# scn.objects['cycleslamp1'].hide_render = True
scn.render.engine = "BLENDER_EEVEE"
bpy.data.scenes["Scene"].eevee.use_gtao = True
bpy.data.scenes["Scene"].eevee.use_ssr = True
bpy.data.scenes["Scene"].eevee.use_ssr_refraction = True
bpy.data.scenes["Scene"].eevee.ssr_thickness = 0.01
bpy.data.scenes["Scene"].eevee.ssr_quality = 1
bpy.data.scenes["Scene"].eevee.gtao_quality = 1
bpy.data.scenes["Scene"].eevee.gi_glossy_clamp = 5
bpy.data.scenes["Scene"].eevee.gi_diffuse_bounces = 5
bpy.data.scenes["Scene"].eevee.taa_render_samples = 64

bpy.data.scenes["Scene"].cycles.device = "GPU"

folders = ["Material"]
inside = [["Concrete 02"]]
import_("Materials_05.blend", None, None)

# bpy.data.materials['Concrete 02'].node_tree.nodes["Emission"]
# print(str(dir(bpy.data.materials['Concrete 02'].node_tree)))
# for a in bpy.data.materials['Concrete 02'].node_tree.nodes["Mapping"].scale:
#    a = 15

# bpy.data.materials['Concrete 02'].node_tree.nodes["Mapping"].scale[0]=15
# bpy.data.materials['Concrete 02'].node_tree.nodes["Mapping"].scale[1]=15
# bpy.data.materials['Concrete 02'].node_tree.nodes["Mapping"].scale[2]=15
bpy.data.materials["Concrete 02"].node_tree.nodes["Mapping"].inputs[3].default_value[
    0
] = 15
bpy.data.materials["Concrete 02"].node_tree.nodes["Mapping"].inputs[3].default_value[
    1
] = 15
bpy.data.materials["Concrete 02"].node_tree.nodes["Mapping"].inputs[3].default_value[
    2
] = 15
# bpy.ops.scene.light_cache_bake()


# for a,obj in zip([-1,1],[scn.objects['davor'],scn.objects['davor.002']]):
#    createCube(9/2*tiefe+(9/6*tiefe), a*(16/2 * breite - (16/10*breite)),-4.5+0.2 - 1.5,9/6*tiefe*4, 16/10*breite-0.3, 4)
#    differ(obj,scn.objects[-1])
#    bpy.ops.object.select_all(action='DESELECT')
#    scn.objects[-1].select_set(state=True)
#    #bpy.ops.object.delete()
# bisec mit fill
# bpy.ops.mesh.bisec()

# bm = bmesh.new()
# bm.from_mesh(scn.objects['davori.001'].data)
# scn.objects['davor.002'].select_set(state=True)
# cont = bpy.context
# print(str(cont)+'\n'+str(dir(cont)))
# bpy.context.scene.objects.active = scn.objects['davor']
# bpy.context.window = None
# bpy.context.screen = None
# bpy.context.view_layer.objects.active = scn.objects['davor.002']
# bpy.ops.object.mode_set(mode = 'EDIT')
# bpy.ops.mesh.bisect(plane_co=(-6.79,-14.6,-7.57), plane_no=(-0.1,0.15,1), clear_inner=True, use_fill=True, threshold=0.0001)

# bpy.ops.mesh.bisect(plane_co=(9,-9.6+16/10*breite-0.3,-6), plane_no=(0,1,0), clear_inner=True, use_fill=True, threshold=0.0001)
# bpy.ops.mesh.bisect(plane_co=(9,-9.6-16/10*breite+0.3,-6), plane_no=(0,1,0), clear_outer=True, use_fill=True, threshold=0.0001)

# bpy.ops.mesh.bisect(plane_co=(9,9.6+0.22,-6), plane_no=(0,1,0), clear_outer=True, use_fill=True, threshold=0.0001)
# bpy.ops.object.mode_set(mode = 'OBJECT')
# bpy.ops.object.mode_set(mode = 'EDIT')
# bpy.context.view_layer.objects.active = scn.objects['davor.002']
# scn.objects['davor.002'].select_set(state=True)
# bpy.ops.mesh.bisect(plane_co=(9,9.6-0.22,-6), plane_no=(0,-1,0), clear_outer=True, use_fill=True, threshold=0.0001)

# bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:],
# plane_co=(9,-9.6,-5.8),
#            plane_co=(-6.79,-14.6,-7.57),
#            plane_no=(-0.1,0.15,1),
#            clear_inner=True,
# use_fill=True
# threshold=0.0001
#            )
# bpy.ops.object.mode_set(mode = 'OBJECT')
# scn.objects['davor'].select_set(state=False)
# bpy.ops.mesh.primitive_plane_add(size=20.0, calc_uvs=True, enter_editmode=False, align='WORLD', location=(9, -9.6, -5.8), rotation=(1, 1, 1))
# dann
# google python seperate by selection
# folders = ['Object']
# inside = [['1D_field','1DM_B1','1DM_B2','1DM_F2','1DM_F3','1DM_K1','1DM_K2','1DM_K3','1DM_L1','1DM_L2','1DM_L3','1DM_L4','1DM_M1','1DM_M2','1DM_M3','1DM_MIRROR','1DM_TABLE','1DM_TABLE_SIDE']]
# import_("1D_Baroque Mirror Table (blend 2.76).blend",(0,0,-8),None)


def createPlane(name, size=1.0, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_plane_add(
        size=2.0,
        calc_uvs=True,
        enter_editmode=False,
        align="WORLD",
        location=location,
        rotation=rotation,
    )
    # bpy.ops.object.lightprobe_add(type='PLANAR', radius=2.0, align='WORLD', location=location, rotation=rotation)
    scn.objects[-1].name = name
    return scn.objects[-1]


# bpy.ops.transform.resize(value=(40,50,30))


def glasmat(variante=1):
    mat = bpy.data.materials.new("Spiegel")
    mat.use_nodes = True
    nt = mat.node_tree
    nodes = nt.nodes
    links = nt.links
    while nodes:
        nodes.remove(nodes[0])
    output = nodes.new("ShaderNodeOutputMaterial")
    glossy1 = nodes.new("ShaderNodeBsdfGlossy")
    glossy2 = nodes.new("ShaderNodeBsdfGlossy")
    glossy3 = nodes.new("ShaderNodeBsdfGlossy")
    glossy4 = nodes.new("ShaderNodeBsdfGlossy")
    mix1 = nodes.new("ShaderNodeMixShader")
    mix2 = nodes.new("ShaderNodeMixShader")
    layerweight1 = nodes.new("ShaderNodeLayerWeight")
    layerweight2 = nodes.new("ShaderNodeLayerWeight")

    if variante == 1:
        glossy1.inputs[0].default_value = (1, 0.5, 0.5, 1)
        glossy2.inputs[0].default_value = (0.5, 1, 0.5, 1)
        glossy3.inputs[0].default_value = (0.5, 0.5, 1, 1)
        glossy4.inputs[0].default_value = (0.8, 0.8, 0.8, 1)
    else:
        glossy1.inputs[0].default_value = (0.5, 0.5, 1, 1)
        glossy2.inputs[0].default_value = (1, 0.5, 0.5, 1)
        glossy3.inputs[0].default_value = (0.5, 1, 0.5, 1)
        glossy4.inputs[0].default_value = (0.9, 0.9, 0.9, 1)
    glossy1.inputs[1].default_value = 0
    glossy2.inputs[1].default_value = 0
    glossy3.inputs[1].default_value = 0
    glossy4.inputs[1].default_value = 0
    layerweight1.inputs[0].default_value = 0.920
    layerweight2.inputs[0].default_value = 0.5

    links.new(mix1.inputs[1], glossy1.outputs["BSDF"])
    links.new(mix1.inputs[2], glossy2.outputs["BSDF"])
    links.new(mix2.inputs[2], glossy3.outputs["BSDF"])

    links.new(mix1.inputs[0], layerweight1.outputs[1])
    links.new(mix2.inputs[0], layerweight2.outputs[1])

    glossy1.distribution = "SHARP"
    glossy2.distribution = "SHARP"
    glossy3.distribution = "SHARP"

    if variante == 3:
        links.new(mix2.inputs[1], mix1.outputs[0])
        links.new(output.inputs["Surface"], mix2.outputs[0])
    elif variante == 2:
        diffuse = nodes.new("ShaderNodeBsdfDiffuse")
        mix3 = nodes.new("ShaderNodeMixShader")
        # links.new(mix3.inputs[1], mix2.outputs[0])
        links.new(mix3.inputs[1], glossy4.outputs[0])
        links.new(mix3.inputs[2], diffuse.outputs[0])
        links.new(output.inputs["Surface"], mix3.outputs[0])
        diffuse.inputs[1].default_value = 0
        mix3.inputs[0].default_value = 0.2
    elif variante == 1:
        diffuse = nodes.new("ShaderNodeBsdfDiffuse")
        mix3 = nodes.new("ShaderNodeMixShader")
        # links.new(mix3.inputs[1], mix2.outputs[0])
        links.new(mix3.inputs[1], glossy4.outputs[0])
        links.new(mix3.inputs[2], diffuse.outputs[0])
        links.new(output.inputs["Surface"], mix3.outputs[0])
        diffuse.inputs[1].default_value = 0
        mix3.inputs[0].default_value = 0.15

    return mat


def makeKacheln():
    kacheln = []
    # for a in [-8.8+0.01,60-0.01-8.8]:
    for a in [60 - 0.01 - 8.8]:
        for i in range(-11, 11):
            for k in range(-14, 14):
                kacheln.append(
                    createPlane(
                        "kachel-" + str(a) + str(i) + str(k), 20, (4 * i, 4 * k, a)
                    )
                )

    for a in [39.9, -39.9]:
        for i in range(-10, 10):
            for k in range(-14, 14):
                kacheln.append(
                    createPlane(
                        "kachel-" + str(a) + str(i) + str(k),
                        20,
                        (a, 4 * k, -8.8 + 25 + i * 4),
                        rotation=(0, math.pi / 2, 0),
                    )
                )

    for a in [49.9, -49.9]:
        for i in range(-10, 10):
            for k in range(-14, 14):
                kacheln.append(
                    createPlane(
                        "kachel-" + str(a) + str(i) + str(k),
                        20,
                        (4 * k, a, -8.8 + 25 + i * 4),
                        rotation=(0, math.pi / 2, math.pi / 2),
                    )
                )

    bpy.ops.object.select_all(action="DESELECT")
    for kachel in kacheln:
        kachel.select_set(state=True)
    bpy.ops.object.join()
    scn.objects[-1].name = "Kacheln"
    scn.objects[-1].data.materials.append(glasmat(1))
    return scn.objects[-1]


scn.objects["room"].data.materials.append(bpy.data.materials["Concrete 02"])
# scn.objects['room'].data.materials.append(glasmat(2))

# obj.data.polygons[0].material_index = 2
folders = ["Material"]
inside = [["Concrete Tiles"]]
import_("Materials_11.blend", None, None)
scn.objects["room"].data.materials.append(bpy.data.materials["Concrete Tiles"])
scn.objects["room"].data.polygons[4].material_index = 1
bpy.data.materials["Concrete Tiles"].node_tree.nodes["Mapping"].inputs[3].default_value[
    0
] = 15
bpy.data.materials["Concrete Tiles"].node_tree.nodes["Mapping"].inputs[3].default_value[
    1
] = 15
bpy.data.materials["Concrete Tiles"].node_tree.nodes["Mapping"].inputs[3].default_value[
    2
] = 15
makeKacheln()
