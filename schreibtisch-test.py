import bpy
import math
import bmesh
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

def joinmerge(obs):
    ctx = bpy.context.copy()
    # one of the objects to join
    ctx['active_object'] = obs[0]
    ctx['selected_objects'] = obs
    ctx['selected_editable_bases'] = [scn.object_bases[ob.name] for ob in obs]
    bpy.ops.object.join(ctx)

def createCube(x,y,z,xx,yy,zz):
    bpy.ops.mesh.primitive_cube_add(location = (x, y, z))
    #cube = bpy.context.scene.objects[-1]
    bpy.ops.transform.resize(value=(xx, yy, zz))

def differ(from_,to):
        mod_bool = from_.modifiers.new('my_bool_mod', 'BOOLEAN')
        mod_bool.operation = 'DIFFERENCE'
        mod_bool.object = to
        bpy.context.scene.objects.active = from_
        res = bpy.ops.object.modifier_apply(apply_as='DATA',modifier = 'my_bool_mod')


#bpy.ops.wm.
#bpy.ops.wm.open_mainfile(filepath="/home/alex/Downloads/Palm_Tree.blend")
reset_blend()
#import bpy
#def setState0():
#    for ob in bpy.data.objects.values():ob.selected=False
#    bpy.context.scene.objects.active = None
#setState0()
#original_type = bpy.context.area.type
#bpy.context.area.type = "VIEW_3D"
#bpy.context.mode='OBJECT'
#bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
#bpy.context.area.type = original_type
#bpy.ops.wm.read_homefile(use_empty=True)
#bpy.ops.wm.read_factory_settings(use_empty=True)
#original_type = bpy.context.area.type
#bpy.context.
#bpy.context.area.type = "VIEW_3D"
#bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
#bpy.context.area.type = original_type
breite = 1.5
tiefe = 1.5

bpy.ops.mesh.primitive_cube_add(location = (0, 0, 0))
#bpy.ops.mesh.primitive_cube_add()
#cont = bpy.context.area.type
#print(str(cont))
#myobject = bpy.context.active_object
#bpy.context.scene.objects.active = myobject
#myobject.select = True
scn = bpy.context.scene
cube = scn.objects['Cube']
bpy.context.scene.objects[0].select = True
bpy.ops.transform.resize(value=(9/2*tiefe, 16/2*breite, 0.2))
bpy.ops.mesh.primitive_cylinder_add(radius=3*(breite+tiefe)/math.pi,location=(5.5*tiefe,0,0))
bpy.ops.transform.resize(value=(1*tiefe, 2*breite, 1))
cylinder = scn.objects['Cylinder']
cube.name = 'Tischplatte'
bpy.context.scene.objects[0].select = False

mod_bool = cube.modifiers.new('my_bool_mod', 'BOOLEAN')
mod_bool.operation = 'DIFFERENCE'
mod_bool.object = cylinder
bpy.context.scene.objects.active = cube
res = bpy.ops.object.modifier_apply(apply_as='DATA',modifier = 'my_bool_mod')
cube.select = False
cylinder.select = True
bpy.ops.object.delete()

bpy.ops.mesh.primitive_cube_add(location = (-(9/2-7/2)*tiefe, 0, -2))
cube2 = scn.objects['Cube']
cube2.name = 'Platte_2'
bpy.ops.transform.resize(value=(7/2*tiefe, 16/2*breite, 0.2))
bpy.ops.mesh.primitive_cylinder_add(radius=3*(breite+tiefe)/math.pi,location=(2.5*tiefe,0,-2))
bpy.ops.transform.resize(value=(1*tiefe, 2*breite, 1))
cylinder = scn.objects['Cylinder']

mod_bool = cube2.modifiers.new('my_bool_mod', 'BOOLEAN')
mod_bool.operation = 'DIFFERENCE'
mod_bool.object = cylinder
bpy.context.scene.objects.active = cube2
res = bpy.ops.object.modifier_apply(apply_as='DATA',modifier = 'my_bool_mod')
cube.select = False
cube2.select = False
cylinder.select = True
bpy.ops.object.delete()
cylinder.select = False

bpy.ops.mesh.primitive_cube_add(location = (9/2*tiefe-0.5-tiefe*2, (16/2-0.5)*breite, -4.5+0.1))
leg = scn.objects['Cube']
leg.name = 'Tischbein1'
leg.select = True
bpy.ops.transform.resize(value=(0.5, 0.5, 4.5))
leg.select = False
bpy.ops.mesh.primitive_cube_add(location = (-9/2*tiefe+0.5, (-16/2+0.5)*breite,-4.5+0.1))
leg = scn.objects['Cube']
leg.name = 'Tischbein2'
leg.select = True
bpy.ops.transform.resize(value=(0.5, 0.5, 4.5))
leg.select = False
bpy.ops.mesh.primitive_cube_add(location = (9/2*tiefe-0.5-tiefe*2, (-16/2+0.5)*breite, -4.5+0.1))
leg = scn.objects['Cube']
leg.name = 'Tischbein3'
leg.select = True
bpy.ops.transform.resize(value=(0.5, 0.5, 4.5))
leg.select = False
bpy.ops.mesh.primitive_cube_add(location = (-9/2*tiefe+0.5, (16/2-0.5)*breite, -4.5+0.1))
leg = scn.objects['Cube']

leg.name = 'Tischbein4'
leg.select = True
bpy.ops.transform.resize(value=(0.5, 0.5, 4.5))
leg.select = False

cupboards = []
for a in [-1,1]:
    coords=((-7/4+9/4)*tiefe,a*(16/2*breite-(1.8*breite)),-3.5)
    bpy.ops.mesh.primitive_cube_add(location = coords)
    cupboard = scn.objects['Cube']
    cupboard.name = 'cupboard_'+str(int((a+1)/2+1))
    cupboard.select = True
    bpy.ops.transform.resize(value=(7/2*tiefe, 1.8*breite, 3.5))
    cupboards.append(cupboard)
    cupboard.select = False
    mod_bool = scn.objects['Platte_2'].modifiers.new('my_bool_mod', 'BOOLEAN')
    mod_bool.operation = 'DIFFERENCE'
    mod_bool.object = cupboard
    bpy.context.scene.objects.active = scn.objects['Platte_2']
    res = bpy.ops.object.modifier_apply(apply_as='DATA',modifier = 'my_bool_mod')

for a in [-1,1]:
    coords=((-7/4+9/4)*tiefe,a*(16/2*breite-(1.8*breite)),-3.5)
    bpy.ops.mesh.primitive_cube_add(location = coords)
    cupboardb = scn.objects['Cube']
    cupboardb.name = 'cupboard_'+str(int((a+1)/2+1))+'_in'
    cupboardb.select = True
    bpy.ops.transform.resize(value=(7/2*1.4*tiefe, 1.8*breite-0.4, 3.5-0.4))
    cupboardb.select = False
    mod_bool = cupboards[int((a+1)/2)].modifiers.new('my_bool_mod', 'BOOLEAN')
    mod_bool.operation = 'DIFFERENCE'
    mod_bool.object = cupboardb
    bpy.context.scene.objects.active = cupboards[int((a+1)/2)]
    res = bpy.ops.object.modifier_apply(apply_as='DATA',modifier = 'my_bool_mod')
    cupboard.select = False
    cupboardb.select = True
    bpy.ops.object.delete()

for a in [-1,1]:
    for b in [[-4.5,1],[-1,0.4]]:
        coords=((-7/4+9/4-2.5+b[1])*tiefe,a*(16/2-2-1.8)*breite,b[0])
        bpy.ops.mesh.primitive_cube_add(location = coords)
        cupboardb = scn.objects['Cube']
        cupboardb.name = 'cupboardi_'+str(int((a+1)/2+1))+'_behind'
        cupboardb.select = True
        bpy.ops.transform.resize(value=(1.5*b[1]*tiefe, 1*breite, 1.5*b[1]))
        cupboardb.select = False
        mod_bool = cupboards[int((a+1)/2)].modifiers.new('my_bool_mod', 'BOOLEAN')
        mod_bool.operation = 'DIFFERENCE'
        mod_bool.object = cupboardb
        bpy.context.scene.objects.active = cupboards[int((a+1)/2)]
        res = bpy.ops.object.modifier_apply(apply_as='DATA',modifier = 'my_bool_mod')
        cupboard.select = False
        cupboardb.select = True
        bpy.ops.object.delete()

#bpy.ops.mesh.primitive_cube_add(location = (-7/4+9/4,-16/2+2,-3.5))
#cupboard = scn.objects['Cube']
#cupboard.name = 'cupboard_2'
#cupboard.select = True
#bpy.ops.transform.resize(value=(7/2, 1.8, 3.5))
#cupboard.select = False
#s/(breite+tiefe)/2/math.sqrt(math.pow(breite,2)+math.pow(tiefe,2))/g
for a in [-5,0,5]:
    bpy.ops.object.lamp_add(location=(-3.6*tiefe,a*breite,0))
    bpy.ops.mesh.primitive_cylinder_add(radius=3*(breite+tiefe)/math.pi,location=(-3.6*tiefe,a*breite,0))
    bpy.ops.transform.resize(value=(0.2, 0.2, 1))
    cylinder = scn.objects['Cylinder']
    cylinder.name = 'hole_'+str(a)
    mod_bool = cube.modifiers.new('my_bool_mod', 'BOOLEAN')
    mod_bool.operation = 'DIFFERENCE'
    mod_bool.object = cylinder
    bpy.context.scene.objects.active = cube
    res = bpy.ops.object.modifier_apply(apply_as='DATA',modifier = 'my_bool_mod')
    cube.select = False
    cylinder.select = True
    bpy.ops.object.delete()

color = '663300'

r = float.fromhex(color[0:2])/255.0
g = float.fromhex(color[2:4])/255.0
b = float.fromhex(color[4:6])/255.0


for l in bpy.data.lamps:
    l.color = [r, g, b]
    l.energy = 6


bpy.ops.object.camera_add(view_align=True,
                          enter_editmode=False,
                          location=(30, 10, 7),
                          rotation=(math.pi*1.4, -math.pi, math.pi*1.6))
cam = scn.objects['Camera']
cam.name = 'cam_1'
bpy.data.cameras['Camera'].lens = 25

#bpy.ops.object.lamp_add(location=(0,0,8))
#for a in [10,-10]:
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

bpy.ops.mesh.primitive_cube_add(location = (10, 10, 10))
lamp = scn.objects['Cube']
lamp.name = 'cycleslamp'
lamp.select = True
bpy.ops.transform.resize(value=(3,3,3))
bpy.data.objects['cycleslamp'].cycles_visibility.camera = False

## Create a material.
#mat = bpy.data.materials.new(name = 'my_material')

## Set some properties of the material.
#mat.diffuse_color = (1, 0., 0.)
#mat.diffuse_shader = 'LAMBERT'
#mat.diffuse_intensity = 1.0
#mat.specular_color = (1., 1., 1.)
#mat.specular_shader = 'COOKTORR'
#mat.specular_intensity = 0.5
#mat.alpha = 1
#mat.ambient = 1

#materialart =  'WOOD'

#matname = "mat" + materialart
#texname = "tex" + materialart

# new material
#textur = bpy.data.textures.new(texname, type=materialart)
#textur.wood_type= 'RINGNOISE'
#textur.saturation = 0.0
#texture.active_texture = textur2
#material = bpy.data.materials.new(matname)
#holzmat = material
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


        #mesh.data.materials.append(material)



#obj = cube.data
#obj.materials.append(material)

# new texture
#bpy.data.textures[texname].specular_color=(0.9,0.3,0.0)
#textur.specular_color=(0.9,0.3,0.0)

# lits all properties and methods of a texture
# print(dir(textur))

# connect texture with material


mesh = cube.data
#mesh.materials.append(mat)
coords=(0,0,-8.8+30)
bpy.ops.mesh.primitive_cube_add(location = coords)
cupboardb = scn.objects['Cube']
cupboardb.name = 'room'
cupboardb.select = True
bpy.ops.transform.resize(value=(40,50,30))
cupboardb.select = False

#materialart =  'MUSGRAVE'

#matname = "mat" + materialart
#texname = "tex" + materialart

# new material
#textur = bpy.data.textures.new(texname, type=materialart)
#o = scn.objects['Material']
#o.select = True
#bpy.ops.transform.resize(value=(.2, .2, .2))
#o.select = False
#textur.noise_scale=0.1
#textur.musgrave_type = 'HYBRID_MULTIFRACTAL'
#textur.saturation = 0.0
#texture.active_texture = textur2
#material = bpy.data.materials.new(matname)
#material.texture_slots.add()
#material.active_texture = textur
#material.resize(value=(0.2,0.2,0.2))
#tex = bpy.data.textures.new("SomeName", type = 'IMAGE')
#tex.image = bpy.data.images.load('wirr.jpg')
#tex.im .noise_scale=0.01
#tex.repeat_x=20
#tex.repeat_y=20
#material.texture_slots.add()
#material.active_texture = tex
#material.diffuse_color = (1.0, 1.0, 1.0)
#material.raytrace_mirror.use = True
#material.raytrace_mirror.reflect_factor = 0.4
#material.raytrace_mirror.gloss_factor = 0.9
#material.specular_color = (0.9, .4, 0.1)
##material.line_color = (0.9, .4, 1)
#material.mirror_color = (0.9, .4, 0.1)
#scn.objects['room'].data.materials.append(material)
#bpy.ops.wm.link(filepath="/home/alex/Downloads/Palm_Tree.blend")
#bpy.ops.wm.append(filepath="//Palm_Tree.blend",directory="/home/alex/Downloads",link=False)

#for lamp in bpy.data.lamps:
#    lamp.energy = 2

for a in [-1,1]:
    for b in [-7.5,-1]:
        bpy.ops.object.lamp_add(location=(3*tiefe,7*a*breite,b))
        c = 0.0 if b == -7.5 else 0.2
        bpy.data.lamps[-1].color = (1.0,c,0.0)
        bpy.data.lamps[-1].distance = 1.0
        bpy.data.lamps[-1].energy = 10
        bpy.data.lamps[-1].shadow_method = 'RAY_SHADOW'
        bpy.data.lamps[-1].shadow_ray_samples = 3


for lamp in bpy.data.lamps:
    lamp.shadow_method = 'RAY_SHADOW'


#Mesh\\['255_mesh_.001','255_mesh_']
#Object\\['255_mesh_.001','255_mesh_']
#Group\\255
#Image\\['blatt.jpg','holz.jpg','Render Result']
#Material\\['Material','Material.002','Material.001']
#Scene\\Scene
#Texture\\['Bild','bild','Blatt','Tex','Wood']

#          ['blatt.jpg','holz.jpg','Render Result'],
#          ['Material','Material.002','Material.001'],
        #  ['Scene']
 #         ['Bild','bild','Blatt','Tex','Wood']]


def import_(blendfile,locat,resiz,tree = False):
    objs=[]
    for folder,things in zip(folders,inside):
        section   = "\\"+folder+"\\"
        for object in things:
            filepath  = blendfile + section + object
            directory = blendfile + section
            filename  = object

            len1_ = len(scn.objects)
            bpy.ops.wm.append(
                filepath=filepath,
                filename=filename,
                directory=directory)
            len2_ = len(scn.objects)
            if len1_ < len2_:
                objs.append(scn.objects[-1])
    for obj in scn.objects:
        obj.select = False
    for obj in inside[0]:
        obj = scn.objects[obj]
        obj.select = True
        bpy.ops.transform.resize(value=resiz)
        obj.location = locat
        a = str(obj.name)
        if tree:
            obj.name = 'tree 1 '+a
            bpy.ops.object.duplicate_move_linked()
            for obj2 in scn.objects:
                obj2.select = False
    return objs
folders = ['Mesh','Object']
inside = [['255_mesh_.001','255_mesh_'],
          ['255_mesh_.001','255_mesh_']]
import_("alxpalme.blend",(-13,15,-8.8),(0.3, 0.3, 0.3),True)
folders = ['Mesh','Object','Material','Texture']
obj_ = ['Box01','Box02','Box03','Box04','Box05','Box06','Box13.Box14.Box15']
for i in range(1,10):
    obj_.append('Cylinder0'+str(i))
for i in range(10,13):
    obj_.append('Cylinder'+str(i))
str_=""
for i in range(14,19):
    str_+="Cylinder"+str(i)+"."
str_+="Cylinder"
obj_.append(str_)
str_=""
for i in range(21,26):
    str_+="Cylinder"+str(i)+"."
str_+="Cylinder"
obj_.append(str_)
for i in range(28,36):
    obj_.append('Cylinder'+str(i))
obj_.append('Object01')
obj_.append('Object02')
obj_.append('Shape01')
obj_.append('Sphere01')
for i in range(1,5):
    obj_.append('Tube0'+str(i))
inside = [obj_,obj_,['01 - Default','10 - Default','11 - Default','13 - Default','Material'],['Tex']]
#print(str(obj_))
objs = import_("pctower.blend",(0,0,0),(1,1,1))
#for obj in objs:
#    print(obj.name)
joinmerge(objs)
scn.objects['Box01'].select = True
bpy.ops.transform.resize(value=(0.85,0.85,0.85))
scn.objects.active = scn.objects['Box01']
bpy.context.object.rotation_euler = (0,0,math.pi)
scn.objects['Box01'].location = (-0.3,3.5*breite,-7+0.4)
#9/2*tiefe, 16/2*breite
bpy.ops.object.duplicate_move_linked(OBJECT_OT_duplicate={"linked":True, "mode":'TRANSLATION'},TRANSFORM_OT_translate={"value":(0,-11.5*breite,0), "constraint_axis":(False, False, False),
"constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST',
"snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "texture_space":False, "release_confirm":False})
scn.objects['Box01'].select = False


folders = ['Mesh','Object','Material','Texture','Image']
#folders = ['Mesh','Object']
obj_=['Cube','Keyboard']
for a in range(5,6):
    obj_.append('Plane.00'+str(a))
obj_.append('Plane')
mati_=['Material']
for a in range(0,8):
    mati_.append('Material.00'+str(a))
texti_=['Texture','Texture.001','Texture.002']
imagi=['Bildschirmfoto 2011-1','Dots.png','keyboard.jpg.001','keyboard.jpg','Mac Desktop.png','Mac_back.png','Mac_front.png','Mac_side.png','mouse side.jpg','Render Result']
#meshi=['Cube.001','Cube']
#meshi=['Cube']
meshi=[]
for a in range(5,6):
    meshi.append('Plane.00'+str(a))
meshi.append('Plane')
inside = [meshi,obj_,mati_,texti_,imagi]
#print(str(meshi))
#inside = [meshi,obj_]
#print(str(obj_))
objs = import_("Mac_2.blend",(0,0,0),(1,1,1))
joinmerge([scn.objects['Plane'],scn.objects['Plane.005']])
scn.objects.active = scn.objects['Plane']
bpy.context.object.rotation_euler = (-math.pi/2,0,math.pi/2)
bpy.ops.transform.resize(value=(2,2,2))
scn.objects['Plane'].location = (-3,-3,4.4)

scn.objects['Plane'].select = False
scn.objects['Keyboard'].select = True

scn.objects.active = scn.objects['Keyboard']
bpy.context.object.rotation_euler = (math.pi/12,0,math.pi/2)
bpy.ops.transform.resize(value=(2,2,2))
scn.objects['Keyboard'].location = (2,-3,0.45)
scn.objects['Keyboard'].select = False




for o in [-1,-2]:
    bpy.data.objects[o].select = True
    bpy.data.objects[o].location = (-13,-15,-8.8)
    bpy.data.objects[o].select = False


#mist = bpy.data.worlds["World"].mist_settings
#mist.use_mist = True
#mist.start = 25
#mist.depth = 50


bpy.ops.mesh.primitive_cube_add(location = (-(9/2/2*tiefe), 0, 2))
scn = bpy.context.scene
cube = scn.objects['Cube']
#bpy.context.scene.objects[0].select = True
bpy.ops.transform.resize(value=(9/2/2*tiefe, 16/2*breite, 0.2))
bpy.ops.mesh.primitive_cylinder_add(radius=5*(breite+tiefe)/math.pi,location=(5.5*tiefe-(9/2/2*tiefe)*2,0,3))
bpy.ops.transform.resize(value=(1*tiefe/1.5, 1.5*breite,4))
cylinder = scn.objects['Cylinder']
cube.name = 'Oberplatte'

oben=[cube]
obenname=[cube.name]

for a in [-3,-1,1,3]:
    bpy.ops.mesh.primitive_cube_add(location = (-(9/2/2*tiefe), a*(16/2*breite/3-0.25), 1))
    scn = bpy.context.scene
    oben.append(scn.objects['Cube'])
    #bpy.context.scene.objects[0].select = True
    bpy.ops.transform.resize(value=(9/2/2*tiefe, 0.5, 1))
    oben[-1].name = 'Oben seitlich '+str(a)
    obenname.append(oben[-1].name)


for a in oben:
    mod_bool = a.modifiers.new('my_bool_mod', 'BOOLEAN')
    mod_bool.operation = 'DIFFERENCE'
    mod_bool.object = cylinder
    bpy.context.scene.objects.active = a
    res = bpy.ops.object.modifier_apply(apply_as='DATA',modifier = 'my_bool_mod')
    a.select = False
    cylinder.select = True
bpy.ops.object.delete()


