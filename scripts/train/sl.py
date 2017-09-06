import bpy
import os
import math
import mathutils
import sys
sys.path.append('./scripts/util')
from helper import set_prop_val

# output properties
bpy.data.scenes['Scene'].render.resolution_x = 1024 # 1920
bpy.data.scenes['Scene'].render.resolution_y = 768 # 1080
bpy.data.scenes['Scene'].render.resolution_percentage = 100
bpy.data.scenes['Scene'].render.tile_x = 256
bpy.data.scenes['Scene'].render.tile_y = 256
bpy.data.scenes['Scene'].cycles.max_bounces = 4
bpy.data.scenes['Scene'].cycles.min_bounces = 0
bpy.data.scenes['Scene'].cycles.sample = 300

angles = mathutils.Vector((-20.0, 0.0, 20.0)) * math.pi / 180.0
ndim = 3 # number of angles, 3
nimg = 20 # number of patterns, 20

# name of object
obj_name = 'sphere'
# root directory of synthetic dataset
rdir = 'C:/Users/Admin/Documents/3D_Recon/Data/synthetic_data'
# input directory of the projection patterns
idir = '%s/textures/sl' % rdir
# output directory of rendered images
odir = '%s/%s/train/sl' % (rdir, obj_name)
# list of properties
props = ['tex', 'alb', 'spec', 'rough', 'concav']
# index of effective properties
ind_props = [1, 2, 3]
# get material nodes
nodes = bpy.data.materials['Material'].node_tree.nodes
# set the object visible
bpy.data.objects['Sphere'].hide_render = False
bpy.data.objects['Point'].hide_render = True
bpy.data.objects['Lamp'].hide_render = False
bpy.data.objects['Plane'].hide_render = True

proj_nodes = bpy.data.lamps['Lamp'].node_tree.nodes
tex_node = proj_nodes.get('Image Texture')

set_prop_val(nodes, 0, 2) # set texture to 0.2
for ind_1 in range(2, 3, 3):
    set_prop_val(nodes, ind_props[0], ind_1)

    for ind_2 in range(2, 9, 3):
        set_prop_val(nodes, ind_props[1], ind_2)

        for ind_3 in range(8, 9, 3):
            set_prop_val(nodes, ind_props[2], ind_3)

            subdir = '00%02d%02d%02d' % (ind_1, ind_2, ind_3) # change if ind_props changes
            outdir = '%s/%s' % (odir, subdir)

            if not os.path.exists(outdir):
                os.makedirs(outdir)

            for ind_img in range(0, nimg):
                proj_ptn = bpy.data.images.load("%s/sl_v%d.jpg" % (idir, ind_img))
                tex_node.image = proj_ptn
                bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (outdir, ind_img)
                bpy.ops.render.render(write_still=True)
                
                proj_ptn = bpy.data.images.load("%s/sl_h%d.jpg" % (idir, ind_img))
                tex_node.image = proj_ptn
                bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (outdir, ind_img + nimg)
                bpy.ops.render.render(write_still=True)
            
            for ind_img in range(0, 2):
                proj_ptn = bpy.data.images.load("%s/sl_a%d.jpg" % (idir, 1 - ind_img))
                tex_node.image = proj_ptn
                bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (outdir, ind_img + 2 * nimg)
                bpy.ops.render.render(write_still=True)
