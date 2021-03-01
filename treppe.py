import bpy
import math
def reset_blend():
    #bpy.ops.wm.read_factory_settings()

    for scene in bpy.data.scenes:
        for obj in scene.objects:
            scene.objects.unlink(obj)

    # only worry about data in the startup scene
    for bpy_data_iter in (
            bpy.data.objects,
            bpy.data.meshes,
            bpy.data.lamps,
            bpy.data.materials,
            bpy.data.cameras,
    ):
        for id_data in bpy_data_iter:
            bpy_data_iter.remove(id_data)

#bpy.ops.wm.
##bpy.ops.wm.open_mainfile(filepath="/home/alex/Downloads/Palm_Tree.blend")
reset_blend()
for area in bpy.context.screen.areas: # iterate through areas in current screen
    if area.type == 'VIEW_3D':
        for space in area.spaces: # iterate through spaces in current VIEW_3D area
            if space.type == 'VIEW_3D':
                space.viewport_shade = 'WIREFRAME'
##import bpy
##def setState0():
##    for ob in bpy.data.objects.values():ob.selected=False
##    bpy.context.scene.objects.active = None
##setState0()
##original_type = bpy.context.area.type
###bpy.context.area.type = "VIEW_3D"
##bpy.context.mode='OBJECT'
##bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
##bpy.context.area.type = original_type
##bpy.ops.wm.read_homefile(use_empty=True)
##bpy.ops.wm.read_factory_settings(use_empty=True)
##original_type = bpy.context.area.type
##bpy.context.
##bpy.context.area.type = "VIEW_3D"
##bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
##bpy.context.area.type = original_type
##bpy.ops.mesh.primitive_cube_add()
##cont = bpy.context.area.type
##print(str(cont))
##myobject = bpy.context.active_object
##bpy.context.scene.objects.active = myobject
##myobject.select = True
bpy.ops.mesh.primitive_cube_add(location = (0, 0, 0))
scn = bpy.context.scene
cube = scn.objects['Cube']
cube.name = '1'
bpy.context.scene.objects[0].select = True
#bpy.ops.transform.resize(value=(216, 168+285+5, 222))
flurlaenge = 168+285+5
flurbreite = 216
bpy.ops.transform.resize(value=(flurbreite, flurlaenge, 224))

bpy.ops.mesh.primitive_cube_add(location = (0, 0, 0))
scn = bpy.context.scene
cube2 = scn.objects['Cube']
cube2.name = '2'
cube2.select = True
deckenwanddicke = 21
bpy.ops.transform.resize(value=(flurbreite + (-269 - 16 - 360 + 730) / 2 + 12 , flurlaenge + (153+60-168)+12, 222 + deckenwanddicke*2)) # 40 ist Schätzwert
cube2.location[0] -= (-269 - 16 - 360 + 730) / 2 - 12
cube2.location[1] += (153+60-168)-12
cube2.location[2] += deckenwanddicke




bpy.ops.mesh.primitive_cube_add(location = (0, 0 , 222+deckenwanddicke/2))
scn = bpy.context.scene
luke = scn.objects['Cube']
luke.name = '3'
luke.select = True
lukelaenger=1.5
treppenlaengenbereich = (165 + 6.65 + 20 - 20 + 63.5) * lukelaenger
bpy.ops.transform.resize(value=(59, treppenlaengenbereich ,deckenwanddicke*4))
luke.location[0] = -flurbreite + 59 + deckenwanddicke
luke.location[1] = +flurlaenge /2 - 63.5 - treppenlaengenbereich /2 + 40 + (treppenlaengenbereich /2 * (1-lukelaenger))
lukenende = flurlaenge /2 - 63.5 - treppenlaengenbereich /2 + 40 - ( treppenlaengenbereich )
treppenlaengenbereich /= 1.5
lukelaenger = 1
lukenende = flurlaenge /2 - 63.5 - treppenlaengenbereich /2 + 40 - ( treppenlaengenbereich )

mod_bool = cube2.modifiers.new('my_bool_mod', 'BOOLEAN')
mod_bool.operation = 'DIFFERENCE'
mod_bool.object = luke
bpy.context.scene.objects.active = cube2
res = bpy.ops.object.modifier_apply(apply_as='DATA',modifier = 'my_bool_mod')
cube.select = False
luke.select = False
#bpy.ops.object.delete()
luke.hide_render = True


mod_bool = cube2.modifiers.new('my_bool_mod', 'BOOLEAN')
mod_bool.operation = 'DIFFERENCE'
mod_bool.object = cube
bpy.context.scene.objects.active = cube2
res = bpy.ops.object.modifier_apply(apply_as='DATA',modifier = 'my_bool_mod')
cube2.select = False
cube.select = True
bpy.ops.object.delete()


bpy.ops.mesh.primitive_cube_add(location = (0,0, 0))
scn = bpy.context.scene
dach1 = scn.objects['Cube']
dach1.name = '4'
dach1.select = True
bisdachmitte = 165 + 6.65
dachlen = math.sqrt(math.pow(222 + deckenwanddicke + 224,2)+math.pow(bisdachmitte-20+63.5+179.5 + 20 ,2))
dachwidth = 216 + (-269 - 16 - 360 + 730) / 2 + 12
dacheuler=math.sin(bisdachmitte/222)
#bpy.ops.transform.resize(value=(dachwidth, 20,dachlen+70))
bpy.ops.transform.resize(value=(dachwidth, 20,dachlen))
dach1.rotation_euler = (dacheuler,0,math.pi*0)
#dach1.location[0] -= (168+285+5)/2-(165-20+63.5)/2
dach1.location[2] += (224/2)*2+60
dach1.location[1] += flurlaenge - 63.5 + 20 - (153+60-168)
dach1.location[0] -= (153+60-168)-12

dach1.select = True
dach1.name =  'dach 1'
bpy.ops.object.duplicate_move_linked()
dach2 = bpy.data.objects[-1]
dach2.name = 'dach 2'
#dacheuler/ dachwidthB = math.pi /  dachlen
dachwidthB = dachlen / math.sin(math.pi/2) * dacheuler
dach2.location[1] -= dachwidthB * 2
dach2.rotation_euler[1] += math.pi

for dach in [dach1,dach2]:
    dach.location[2] += 20

dach2.location[1] += 135

bpy.ops.mesh.primitive_cube_add(location = (-216-40,-((168+285+5) - 163 - 61.5)/2, 0))
scn = bpy.context.scene
fenster = scn.objects['Cube']
fenster.name = 'fenster1'
fenster.select = True
bpy.ops.transform.resize(value=(80 , 61.5,114))

mod_bool = cube2.modifiers.new('my_bool_mod', 'BOOLEAN')
mod_bool.operation = 'DIFFERENCE'
mod_bool.object = fenster
bpy.context.scene.objects.active = cube2
res = bpy.ops.object.modifier_apply(apply_as='DATA',modifier = 'my_bool_mod')
cube2.select = False
fenster.select = True
#bpy.ops.object.delete()
fenster.hide_render = True


#bpy.ops.object.lamps.new(name="Area Lamp", type='AREA',location=(2000,0,200))
lamp_data = bpy.data.lamps.new(name="Area Lamp", type='AREA')
bpy.ops.object.camera_add(view_align=False,
                          location=[2400, 720, 1200],
                          rotation=[-math.pi/1.6, math.pi, math.pi*1.6])
#scene.objects.active = Cube
cam = scn.objects['Camera']
cam.data.clip_end=1000000

lukenmitte = -flurbreite + 59 + deckenwanddicke
bpy.ops.mesh.primitive_cylinder_add(radius=2,location=(lukenmitte,flurlaenge - (63.5 * 2),224))
cyl = scn.objects['Cylinder']
cyl.name = 'Kreis'
bpy.ops.transform.resize(value=(200, 200, 59))
cyl.rotation_euler = (math.pi/2,math.pi/2,math.pi/2)

coords = [(lukenmitte,lukenende,224),(lukenmitte,(lukenende + flurlaenge) / 2-110,-110), (lukenmitte,flurlaenge,-224)]
coords2 = [(lukenmitte+120,lukenende,224),(lukenmitte+120,(lukenende + flurlaenge) / 2-110,-110), (lukenmitte+120,flurlaenge,-224)]
#curveData = bpy.data.curves.new('myCurve', type='CURVE')
curveData = bpy.data.curves.new('myCurve', type='SURFACE')
curveData2 = bpy.data.curves.new('myCurve', type='SURFACE')
curveData.dimensions = '3D'
curveData.resolution_u = 3
curveData.resolution_v = 3
curveData2.dimensions = '3D'
curveData2.resolution_u = 3
curveData2.resolution_v = 3
polyline = curveData.splines.new('POLY')
polyline.points.add(len(coords)-1)
polyline2 = curveData.splines.new('POLY')
polyline2.points.add(len(coords)-1)
for i, coord in enumerate(coords):
    x,y,z = coord
    polyline.points[i].co = (x, y, z, 1)
for i, coord in enumerate(coords2):
    x,y,z = coord
    polyline2.points[i].co = (x, y, z, 1)

# create Object
surface_object = bpy.data.objects.new('myCurve', curveData)
surface_object2 = bpy.data.objects.new('myCurve', curveData2)
#curveData.bevel_depth = 100

# attach to scene and validate context
scn = bpy.context.scene
scn.objects.link(surface_object)
scn.objects.link(surface_object2)
#scn.objects.active = curveOB
splines = surface_object.data.splines
for s in splines:
    for p in s.points:
        p.select = True
splines = surface_object2.data.splines
for s in splines:
    for p in s.points:
        p.select = True

bpy.context.scene.objects.active = surface_object
#bpy.ops.object.mode_set(mode = 'EDIT')
#bpy.ops.curve.make_segment()
#bpy.ops.object.mode_set(mode = 'OBJECT')


# mesh arrays
verts = []  # the vertex array
faces = []  # the face array

# mesh variables
numX = 3  # number of quadrants in the x direction
numY = 2  # number of quadrants in the y direction

# wave variables
freq = 1  # the wave frequency
amp = 1  # the wave amplitude
scale = 1  #the scale of the mesh


#fill verts array
coords3=coords[0],coords2[0]
coords4=coords[1],coords2[1]
coords5=coords[2],coords2[2]

for i in [coords3,coords4,coords5]:
    for x,y,z in i:
        vert = (x,y,z)
        verts.append(vert)

#create mesh and object
mesh = bpy.data.meshes.new("wave")
object = bpy.data.objects.new("wave",mesh)

#set mesh location
object.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(object)

#create mesh from python data
mesh.from_pydata(verts,[],faces)
mesh.update(calc_edges=True)

#fill faces array
count = 0
for i in range (0, numY *(numX-1)):
    if count < numY-1:
        A = i  # the first vertex
        B = i+1  # the second vertex
        C = (i+numY)+1 # the third vertex
        D = (i+numY) # the fourth vertex

        face = (A,B,C,D)
        faces.append(face)
        count = count + 1
    else:
        count = 0

#create mesh and object
mesh = bpy.data.meshes.new("wave")
object = bpy.data.objects.new("wave",mesh)

#set mesh location
object.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(object)

#create mesh from python data
mesh.from_pydata(verts,[],faces)
mesh.update(calc_edges=True)

w = bpy.data.worlds["World"]
#bpy.ops.cycles.use_shading_nodes = True
w.use_nodes = True
#world.color =  world.node_tree.nodes['Sky Texture']
#world.use_sky_blend = True
#world.horizon_color = (0.5,0.5,1)
bpy.ops.texture.new()
t = bpy.data.textures[-1]
# set World texture
slot = w.texture_slots.add()
output  = bpy.data.textures.new('Himmel', type="CLOUDS")
slot.texture = output
slot.use_map_horizon = True

def cube(name,xx,yy,zz,s1,s2,s3):
    bpy.ops.mesh.primitive_cube_add(location = (xx,yy,zz))
    cube = bpy.context.scene.objects['Cube']
    cube.name = name
    bpy.ops.transform.resize(value = (s1,s2,s3))
    bpy.context.scene.objects[0].select = True
    return cube

itt = -224
treppen = []

winkel1isin= math.sin((coords[1][2]-coords[2][2])/math.sqrt(math.pow((coords[1][2]-coords[2][2]),2)+math.pow((coords[1][1]-coords[2][1]),2)))
treppenabstand1 = 20
treppentieferung1 = 2/math.pi * treppenabstand1 / winkel1isin * (math.pi/2 - winkel1isin)
winkel2isin= math.sin((coords[0][2]-coords[1][2])/math.sqrt(math.pow((coords[0][2]-coords[1][2]),2)+math.pow((coords[0][1]-coords[1][1]),2)))
treppenabstand2 = 17*2
treppentieferung2 = 2/math.pi *  treppenabstand2 / winkel2isin * (math.pi/2 - winkel2isin)
treppenabstand3 = 20
treppentieferung3 = treppentieferung1 * 2/math.pi
#winkel1 / 20 = 90-winkel1 Grad / teifer
# 20 / winkel1 = tiefer / 90 - winkel1
# tiefer = 20 / winkel1 * (90 - winkel1)
treppe = 0
treppe2 = 0
treppe3 = 0
xxx = scn.objects['Kreis'].location[0]
while (itt<224+deckenwanddicke):
    if itt < -100-treppenabstand1/3.4:
        treppen.append(cube('Treppe '+str(itt),xxx,coords[2][1]-treppe*treppentieferung1,itt,59,20,4))
        itt += treppenabstand1
    else:
        if itt < 224- 90:
            treppen.append(cube('Treppe '+str(itt),xxx,coords[1][1]-treppe2*treppentieferung2,itt,59,20,4))
            itt += treppenabstand2
            treppe2 += 1
        else:
            treppen.append(cube('Treppe '+str(itt),xxx,coords[1][1]-treppe2*treppentieferung2-treppe3*treppentieferung3,itt,59,20,4))
            itt += treppenabstand3
            treppe3 += 1
    treppe += 1

#treppen[-1].location[1] -= 100
#bpy.ops.transform.resize(value = (1,3,1))
#treppen[-2].location[1] -= 50
#treppen[-1].select = False
#treppen[-2].select = True
#bpy.ops.transform.resize(value = (1,3,1))
#treppen[-2].select = False

#treppen[0].select = True
#treppen[0].rotation_euler[2] -= math.pi/2/4*4
#treppen[1].rotation_euler[2] -= math.pi/2/4*3
#treppen[2].rotation_euler[2] -= math.pi/2/4*2
#treppen[3].rotation_euler[2] -= math.pi/2/4*1

treppen[6].location[1] += 30
#scn.objects['2'].hide = False
#scn.objects['dach 1'].hide = True
#scn.objects['dach 2'].hide = True
#scn.objects['wave.001'].hide = False

for a in [0,1,2,3]:
    treppen[a].rotation_euler[2] -= math.pi/2/4*(4-a)
    treppen[a].location[0] += (4-a)/3*59
    treppen[a].location[1] -= 59/4*(4-a)
for a in [-5,-4,-3,-2,-1]:
    treppen[a].rotation_euler[2] -= math.pi/2/5*(5-a)
    treppen[a].location[0] += ((a-4)/3*59 + 59 * 3) * 2/3


#mitte = cube('dachmitte',0,flurlaenge-(165-20+36.5-6.65)+165,224,flurbreite,20,222)
mitte = cube('dachmitte',0,flurlaenge-(63.5+165)*2,224+deckenwanddicke*2+222,flurbreite,20,222)

for ob in bpy.data.objects:
    if ob.name in ['wave','wave.001','myCurve','myCurve.001','Kreis','dachmitte']:
        ob.hide_render = True
        ob.hide = True

#treppen[0].select = False

#    bpy.ops.object.delete()
#
#color = '663300'
#
#r = float.fromhex(color[0:2])/255.0
#g = float.fromhex(color[2:4])/255.0
#b = float.fromhex(color[4:6])/255.0
#
#

#cylinder = scn.objects['Cylinder']


#cylinder = scn.objects['Cylinder']
#cube.name = 'Tischplatte'
#
#mod_bool = cube.modifiers.new('my_bool_mod', 'BOOLEAN')
#mod_bool.operation = 'DIFFERENCE'
#mod_bool.object = cylinder
#bpy.context.scene.objects.active = cube
#res = bpy.ops.object.modifier_apply(apply_as='DATA',modifier = 'my_bool_mod')
#cube.select = False
#cylinder.select = True
#bpy.ops.object.delete()
#
#bpy.ops.mesh.primitive_cube_add(location = (-(9/2-7/2), 0, -2))
#cube2 = scn.objects['Cube']
#cube2.name = 'Platte_2'
#bpy.ops.transform.resize(value=(7/2, 16/2, 0.2))
#bpy.ops.mesh.primitive_cylinder_add(radius=3,location=(2.5,0,-2))
#bpy.ops.transform.resize(value=(1, 2, 1))
#cylinder = scn.objects['Cylinder']
#
#mod_bool = cube2.modifiers.new('my_bool_mod', 'BOOLEAN')
#mod_bool.operation = 'DIFFERENCE'
#mod_bool.object = cylinder
#bpy.context.scene.objects.active = cube2
#res = bpy.ops.object.modifier_apply(apply_as='DATA',modifier = 'my_bool_mod')
#cube.select = False
#cube2.select = False
#cylinder.select = True
#bpy.ops.object.delete()
#cylinder.select = False
#
#bpy.ops.mesh.primitive_cube_add(location = (9/2-0.5, 16/2-0.5, -4.5+0.1))
#leg = scn.objects['Cube']
#leg.name = 'Tischbein1'
#leg.select = True
#bpy.ops.transform.resize(value=(0.5, 0.5, 4.5))
#leg.select = False
#bpy.ops.mesh.primitive_cube_add(location = (-9/2+0.5, -16/2+0.5,-4.5+0.1))
#leg = scn.objects['Cube']
#leg.name = 'Tischbein2'
#leg.select = True
#bpy.ops.transform.resize(value=(0.5, 0.5, 4.5))
#leg.select = False
#bpy.ops.mesh.primitive_cube_add(location = (9/2-0.5, -16/2+0.5, -4.5+0.1))
#leg = scn.objects['Cube']
#leg.name = 'Tischbein3'
#leg.select = True
#bpy.ops.transform.resize(value=(0.5, 0.5, 4.5))
#leg.select = False
#bpy.ops.mesh.primitive_cube_add(location = (-9/2+0.5, 16/2-0.5, -4.5+0.1))
#leg = scn.objects['Cube']
#
#leg.name = 'Tischbein4'
#leg.select = True
#bpy.ops.transform.resize(value=(0.5, 0.5, 4.5))
#leg.select = False
#
#cupboards = []
#for a in [-1,1]:
#    coords=(-7/4+9/4,a*(16/2-2),-3.5)
#    bpy.ops.mesh.primitive_cube_add(location = coords)
#    cupboard = scn.objects['Cube']
#    cupboard.name = 'cupboard_'+str(int((a+1)/2+1))
#    cupboard.select = True
#    bpy.ops.transform.resize(value=(7/2, 1.8, 3.5))
#    cupboards.append(cupboard)
#    cupboard.select = False
#    mod_bool = scn.objects['Platte_2'].modifiers.new('my_bool_mod', 'BOOLEAN')
#    mod_bool.operation = 'DIFFERENCE'
#    mod_bool.object = cupboard
#    bpy.context.scene.objects.active = scn.objects['Platte_2']
#    res = bpy.ops.object.modifier_apply(apply_as='DATA',modifier = 'my_bool_mod')
#
#for a in [-1,1]:
#    coords=(-7/4+9/4,a*(16/2-2),-3.5)
#    bpy.ops.mesh.primitive_cube_add(location = coords)
#    cupboardb = scn.objects['Cube']
#    cupboardb.name = 'cupboard_'+str(int((a+1)/2+1))+'_in'
#    cupboardb.select = True
#    bpy.ops.transform.resize(value=(7/2*1.4, 1.8-0.4, 3.5-0.4))
#    cupboardb.select = False
#    mod_bool = cupboards[int((a+1)/2)].modifiers.new('my_bool_mod', 'BOOLEAN')
#    mod_bool.operation = 'DIFFERENCE'
#    mod_bool.object = cupboardb
#    bpy.context.scene.objects.active = cupboards[int((a+1)/2)]
#    res = bpy.ops.object.modifier_apply(apply_as='DATA',modifier = 'my_bool_mod')
#    cupboard.select = False
#    cupboardb.select = True
#    bpy.ops.object.delete()
#
#for a in [-1,1]:
#    for b in [[-4.5,1],[-1,0.4]]:
#        coords=(-7/4+9/4-1,a*(16/2-2-1.8),b[0])
#        bpy.ops.mesh.primitive_cube_add(location = coords)
#        cupboardb = scn.objects['Cube']
#        cupboardb.name = 'cupboardi_'+str(int((a+1)/2+1))+'_behind'
#        cupboardb.select = True
#        bpy.ops.transform.resize(value=(1.5*b[1], 0.5, 1.5*b[1]))
#        cupboardb.select = False
#        mod_bool = cupboards[int((a+1)/2)].modifiers.new('my_bool_mod', 'BOOLEAN')
#        mod_bool.operation = 'DIFFERENCE'
#        mod_bool.object = cupboardb
#        bpy.context.scene.objects.active = cupboards[int((a+1)/2)]
#        res = bpy.ops.object.modifier_apply(apply_as='DATA',modifier = 'my_bool_mod')
#        cupboard.select = False
#        cupboardb.select = True
#        bpy.ops.object.delete()
#
##bpy.ops.mesh.primitive_cube_add(location = (-7/4+9/4,-16/2+2,-3.5))
##cupboard = scn.objects['Cube']
##cupboard.name = 'cupboard_2'
##cupboard.select = True
##bpy.ops.transform.resize(value=(7/2, 1.8, 3.5))
##cupboard.select = False
#
#for a in [-3,0,3]:
#    bpy.ops.object.lamp_add(location=(-3.6,a,0))
#    bpy.ops.mesh.primitive_cylinder_add(radius=3,location=(-3.6,a,0))
#    bpy.ops.transform.resize(value=(0.2, 0.2, 1))
#    cylinder = scn.objects['Cylinder']
#    cylinder.name = 'hole_'+str(a)
#    mod_bool = cube.modifiers.new('my_bool_mod', 'BOOLEAN')
#    mod_bool.operation = 'DIFFERENCE'
#    mod_bool.object = cylinder
#    bpy.context.scene.objects.active = cube
#    res = bpy.ops.object.modifier_apply(apply_as='DATA',modifier = 'my_bool_mod')
#    cube.select = False
#    cylinder.select = True
#    bpy.ops.object.delete()
#
#color = '663300'
#
#r = float.fromhex(color[0:2])/255.0
#g = float.fromhex(color[2:4])/255.0
#b = float.fromhex(color[4:6])/255.0
#
#
#for l in bpy.data.lamps:
#    l.color = [r, g, b]
#
#
#bpy.ops.object.camera_add(view_align=True,
#                          enter_editmode=False,
#                          location=(30, 10, 7),
#                          rotation=(math.pi*1.4, -math.pi, math.pi*1.6))
#cam = scn.objects['Camera']
#cam.name = 'cam_1'
#bpy.ops.object.lamp_add(location=(0,0,8))
#bpy.ops.object.lamp_add(location=(-10,8,8))
#bpy.ops.object.lamp_add(location=(10,-8,8))
#bpy.ops.object.lamp_add(location=(10,8,8))
#bpy.ops.object.lamp_add(location=(-10,-8,8))
#
## Create a material.
#mat = bpy.data.materials.new(name = 'my_material')
#
## Set some properties of the material.
#mat.diffuse_color = (1, 0., 0.)
#mat.diffuse_shader = 'LAMBERT'
#mat.diffuse_intensity = 1.0
#mat.specular_color = (1., 1., 1.)
#mat.specular_shader = 'COOKTORR'
#mat.specular_intensity = 0.5
#mat.alpha = 1
#mat.ambient = 1
#
#materialart =  'WOOD'
#
#matname = "mat" + materialart
#texname = "tex" + materialart
#
## new material
#textur = bpy.data.textures.new(texname, type=materialart)
#textur.wood_type= 'RINGNOISE'
#textur.saturation = 0.0
##texture.active_texture = textur2
#material = bpy.data.materials.new(matname)
#material.texture_slots.add()
#material.active_texture = textur
#tex = bpy.data.textures.new("SomeName", type = 'IMAGE')
#tex.image = bpy.data.images.load('holz.jpg')
#material.texture_slots.add()
#material.active_texture = tex
#material.diffuse_color = (1.0, .3, 0)
#material.specular_color = (0.9, .4, 0.1)
##material.line_color = (0.9, .4, 1)
#material.mirror_color = (0.9, .4, 0.1)
#
#
#for mesh in bpy.context.scene.objects:
#    if mesh.name in ['Tischplatte','Tischbein1','Tischbein2','Tischbein3','Tischbein4','Platte_2','cupboard_1','cupboard_2']:
#        mesh.data.materials.append(material)
#        #mesh.data.materials.append(material)
#
#
#
#obj = cube.data
#obj.materials.append(material)
#
## new texture
##bpy.data.textures[texname].specular_color=(0.9,0.3,0.0)
##textur.specular_color=(0.9,0.3,0.0)
#
## lits all properties and methods of a texture
## print(dir(textur))
#
## connect texture with material
#
#
#mesh = cube.data
##mesh.materials.append(mat)
#coords=(0,0,-8+30)
#bpy.ops.mesh.primitive_cube_add(location = coords)
#cupboardb = scn.objects['Cube']
#cupboardb.name = 'room'
#cupboardb.select = True
#bpy.ops.transform.resize(value=(30,30,30))
#cupboardb.select = False
#
#materialart =  'MUSGRAVE'
#
#matname = "mat" + materialart
#texname = "tex" + materialart
#
## new material
#textur = bpy.data.textures.new(texname, type=materialart)
##o = scn.objects['Material']
##o.select = True
##bpy.ops.transform.resize(value=(.2, .2, .2))
##o.select = False
#textur.noise_scale=0.1
##textur.musgrave_type = 'HYBRID_MULTIFRACTAL'
##textur.saturation = 0.0
##texture.active_texture = textur2
#material = bpy.data.materials.new(matname)
#material.texture_slots.add()
#material.active_texture = textur
##material.resize(value=(0.2,0.2,0.2))
#tex = bpy.data.textures.new("SomeName", type = 'IMAGE')
#tex.image = bpy.data.images.load('wirr.jpg')
##tex.im .noise_scale=0.01
#tex.repeat_x=10
#tex.repeat_y=10
#material.texture_slots.add()
#material.active_texture = tex
#material.diffuse_color = (1.0, 1.0, 1.0)
##material.specular_color = (0.9, .4, 0.1)
###material.line_color = (0.9, .4, 1)
##material.mirror_color = (0.9, .4, 0.1)
#scn.objects['room'].data.materials.append(material)
##bpy.ops.wm.link(filepath="/home/alex/Downloads/Palm_Tree.blend")
##bpy.ops.wm.append(filepath="//Palm_Tree.blend",directory="/home/alex/Downloads",link=False)

bpy.context.scene.render.engine = 'CYCLES'


mat = bpy.data.materials.new('glass')
mat.use_nodes = True
nt = mat.node_tree
nodes = nt.nodes
links = nt.links
while(nodes): nodes.remove(nodes[0])
output  = nodes.new("ShaderNodeOutputMaterial")
glass = nodes.new("ShaderNodeBsdfGlass")
glass.inputs[0].default_value = (0.7,0.7,1,1)
links.new( output.inputs['Surface'], glass.outputs['BSDF'])

#glassvol  = nodes.new("ShaderNodeVolumeAbsorption")
#glassvol.inputs[1].default_value = 0.05
#links.new( output.inputs['Volume'], glassvol.outputs['Volume'])

for mesh in bpy.context.scene.objects:
    if not mesh.name in ['Camera'] and mesh.name in ['1','2','3','4','dach 1','dach 2','Kreis']:
        mesh.data.materials.append(mat)
for mesh in treppen:
    mesh.data.materials.append(mat)

mat = bpy.data.materials.new('lampmat')
mat.use_nodes = True
nt = mat.node_tree
nodes = nt.nodes
links = nt.links
while(nodes): nodes.remove(nodes[0])
output  = nodes.new("ShaderNodeOutputMaterial")
emission  = nodes.new("ShaderNodeEmission")
emission.inputs[1].default_value = 3
links.new( output.inputs['Surface'], emission.outputs['Emission'])

for mesh in bpy.data.lamps:
    if mesh.name in ['cycleslamp']:
        mesh.data.materials.append(mat)

clipend = 1000000

for a in bpy.context.screen.areas:
    if a.type == 'VIEW_3D':
        for s in a.spaces:
            if s.type == 'VIEW_3D':
                s.clip_end = clipend
for cam_ in bpy.data.cameras:
    cam_.clip_end = clipend





#bpy.data.objects["Camera"].location = (0,0,0)
bpy.data.cameras["Camera"].lens = 20
cam.keyframe_insert(data_path = 'location', frame=0.0)
cam.keyframe_insert(data_path = 'rotation_euler', frame=0.0)
bpy.data.objects["Camera"].location = (flurbreite*0.8,flurlaenge*0.8,-224+200)
bpy.data.objects["Camera"].rotation_euler[0] -= math.pi/10
cam.keyframe_insert(data_path = 'location', frame=40.0)
cam.keyframe_insert(data_path = 'rotation_euler', frame=40.0)
bpy.data.objects["Camera"].rotation_euler[2] += math.pi/2
bpy.data.objects["Camera"].location[0] = -flurbreite*0.6
bpy.data.objects["Camera"].location[1] = 50
bpy.data.objects["Camera"].location[2] = 100
cam.keyframe_insert(data_path = 'location', frame=80.0)
cam.keyframe_insert(data_path = 'rotation_euler', frame=80.0)
bpy.data.objects["Camera"].location[0] = -flurbreite*0.9
bpy.data.objects["Camera"].location[1] = 0
bpy.data.objects["Camera"].location[2] = 100 + 224
cam.keyframe_insert(data_path = 'location', frame=120.0)
cam.keyframe_insert(data_path = 'rotation_euler', frame=120.0)
bpy.data.objects["Camera"].location[2] = 224 + 222
bpy.data.objects["Camera"].rotation_euler[2] += math.pi
cam.keyframe_insert(data_path = 'location', frame=160.0)
cam.keyframe_insert(data_path = 'rotation_euler', frame=160.0)
bpy.data.objects["Camera"].location[0] = flurbreite*0.8
bpy.data.objects["Camera"].location[1] = -flurlaenge*0.8
bpy.data.objects["Camera"].rotation_euler[2] += math.pi/4
cam.keyframe_insert(data_path = 'location', frame=200.0)
cam.keyframe_insert(data_path = 'rotation_euler', frame=200.0)
bpy.data.objects["Camera"].location[1] = flurlaenge*0.8
bpy.data.objects["Camera"].rotation_euler[2] += math.pi/2
cam.keyframe_insert(data_path = 'location', frame=240.0)
cam.keyframe_insert(data_path = 'rotation_euler', frame=240.0)
bpy.data.objects["Camera"].location[2] = 0
bpy.data.objects["Camera"].rotation_euler[2] -= math.pi/3
cam.keyframe_insert(data_path = 'location', frame=280.0)
cam.keyframe_insert(data_path = 'rotation_euler', frame=280.0)
bpy.data.objects["Camera"].location[0] = -flurbreite*0.8
bpy.data.objects["Camera"].location[1] = -flurlaenge*0.8
bpy.data.objects["Camera"].location[2] = 224 + 21 + 100
bpy.data.objects["Camera"].rotation_euler[2] -= math.pi/1.7
bpy.data.objects["Camera"].rotation_euler[0] -= math.pi/7
cam.keyframe_insert(data_path = 'location', frame=290.0)
cam.keyframe_insert(data_path = 'rotation_euler', frame=290.0)
bpy.data.objects["Camera"].location[1] += 170
cam.keyframe_insert(data_path = 'location', frame=310.0)
cam.keyframe_insert(data_path = 'rotation_euler', frame=310.0)
bpy.data.objects["Camera"].location[1] += 190
bpy.data.objects["Camera"].location[2] -= 150
cam.keyframe_insert(data_path = 'location', frame=340.0)
cam.keyframe_insert(data_path = 'rotation_euler', frame=340.0)
bpy.data.objects["Camera"].location[1] = flurlaenge*0.8
bpy.data.objects["Camera"].location[2] = 0
cam.keyframe_insert(data_path = 'location', frame=370.0)
#cam.keyframe_insert(data_path = 'rotation_euler', frame=370.0)
bpy.data.objects["Camera"].location[1] = flurlaenge*0.65
bpy.data.objects["Camera"].location[2] = 0
bpy.data.objects["Camera"].location[0] = flurbreite*0.8
bpy.data.objects["Camera"].rotation_euler[2] -= math.pi/2
cam.keyframe_insert(data_path = 'location', frame=400.0)
cam.keyframe_insert(data_path = 'rotation_euler', frame=400.0)

scn.frame_start = 0
scn.frame_end = 400
scn.render.fps = 10
bpy.data.scenes['Scene'].cycles.samples = 70
bpy.data.scenes['Scene'].render.image_settings.file_format = 'AVI_RAW'
bpy.data.scenes['Scene'].render.filepath = '/media/alex/1800btrfs/blender/treppe'
bpy.data.scenes['Scene'].render.use_overwrite = False
#bpy.ops.viewnumpad(type='CAMERA')
bpy.ops.screen.animation_play()
#bpy.context.screen.areas[3].spaces[0].region_3d.view_perspective = 'CAMERA'
#for area in bpy.context.screen.areas:
#    if area.type == 'VIEW_3D':
#        for space in area.spaces:
#            try:
#                space.region_3d.view_perspective = 'CAMERA'
#            except:
#                pass
