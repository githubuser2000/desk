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
bpy.ops.transform.resize(value=(216, 168+285+5, 224))

bpy.ops.mesh.primitive_cube_add(location = (0, 0, 0))
scn = bpy.context.scene
cube2 = scn.objects['Cube']
cube2.name = '2'
cube2.select = True
bpy.ops.transform.resize(value=(216 + (-269 - 16 - 360 + 730) / 2 + 12 , 168+285+5 + (153+60-168)+12, 222 + 40)) # 40 ist Schätzwert
cube2.location[0] -= (-269 - 16 - 360 + 730) / 2 - 12
cube2.location[1] += (153+60-168)-12
cube2.location[2] += 20




bpy.ops.mesh.primitive_cube_add(location = (0, 0 , 222+20))
scn = bpy.context.scene
cube3 = scn.objects['Cube']
cube3.name = '3'
cube3.select = True
bpy.ops.transform.resize(value=(111, (168 + 285 + 5) - 120 - 64 ,80))
cube3.location[0] -= 216 - 111
cube3.location[1] += 64 - 120


mod_bool = cube2.modifiers.new('my_bool_mod', 'BOOLEAN')
mod_bool.operation = 'DIFFERENCE'
mod_bool.object = cube3
bpy.context.scene.objects.active = cube2
res = bpy.ops.object.modifier_apply(apply_as='DATA',modifier = 'my_bool_mod')
cube.select = False
cube3.select = True
bpy.ops.object.delete()


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
cube4 = scn.objects['Cube']
cube4.name = '4'
cube4.select = True
dachlen = math.sqrt(math.pow(222 + 40 + 224,2)+math.pow(165-20+63.5+179.5,2))
dachwidth = 216 + (-269 - 16 - 360 + 730) / 2 + 12
dacheuler=math.sin(165/222)
bpy.ops.transform.resize(value=(dachwidth, 20,dachlen))
cube4.rotation_euler = (dacheuler,0,math.pi*0)
#cube4.location[0] -= (168+285+5)/2-(165-20+63.5)/2
cube4.location[2] += (224/2)*2+60
cube4.location[1] += 168+285+5 - 63.5 + 20 - (153+60-168)
cube4.location[0] -= (153+60-168)-12

dach1 = cube4
dach1.select = True
dach1.name =  'dach 1'
bpy.ops.object.duplicate_move_linked()
dach2 = bpy.data.objects[-1]
dach2.name = 'dach 2'
#dacheuler/ dachwidthB = math.pi /  dachlen
dachwidthB = dachlen / math.sin(math.pi/2) * dacheuler
dach2.location[1] -= dachwidthB * 2
dach2.rotation_euler[1] += math.pi


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
bpy.ops.object.delete()


#bpy.ops.object.lamps.new(name="Area Lamp", type='AREA',location=(2000,0,200))
lamp_data = bpy.data.lamps.new(name="Area Lamp", type='AREA')
bpy.ops.object.camera_add(view_align=False,
                          location=[2000, 600, 1000],
                          rotation=[-math.pi/1.6, math.pi, math.pi*1.6])
#scene.objects.active = Cube
cam = scn.objects['Camera']
cam.data.clip_end=1000000

#bpy.ops.object.lamps.new(name="Area Lamp", type='AREA',location=(2000,0,200))
lamp_data = bpy.data.lamps.new(name="Area Lamp", type='AREA')
lamp_object = bpy.data.objects.new(name="New Lamp", object_data=lamp_data)
lamp_object.location=(2000,0,600)
lamp_data.energy = 2000
scn.objects.link(lamp_object)
#Create a material.
mat = bpy.data.materials.new(name = 'my_material')

# Set some properties of the material.
mat.diffuse_color = (1, 0., 0.)
mat.diffuse_shader = 'LAMBERT'
mat.diffuse_intensity = 1.0
mat.specular_color = (1., 1., 1.)
mat.specular_shader = 'COOKTORR'
mat.specular_intensity = 0.5
mat.alpha = 0.3
mat.ambient = 0.9
mat.raytrace_mirror.reflect_factor = 0.4
mat.use_transparency = True
mat.raytrace_mirror.use = True

cube4.data.materials.append(mat)
cube2.data.materials.append(mat)
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
#bpy.ops.object.mode_set(mode='EDIT')
#bpy.ops.mesh.remove_doubles(threshold=0.0001)
#for e in bpy.context.object.data.edges:
#    e.hide = True
#bpy.context.object.data.edges[0].location.x += 1000
#bpy.context.object.data.edges[0].select = True
##bpy.ops.transform.location = (1,2,3)
##bpy.ops.object.mode_set(mode='OBJECT')
#mesh = bpy.data.objects['1'].data
#mesh.vertices[3].co.z = -1
#mesh.vertices[7].co.z = -1



#bpy.ops.mesh.primitive_cylinder_add(radius=3,location=(5.5,0,0))
#bpy.ops.transform.resize(value=(1, 2, 1))
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
