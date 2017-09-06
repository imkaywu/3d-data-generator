import bpy
import os
import math
import mathutils
import numpy
import sys

# output properties
bpy.data.scenes['Scene'].render.resolution_x = 1024
bpy.data.scenes['Scene'].render.resolution_y = 768
bpy.data.scenes['Scene'].render.resolution_percentage = 100
bpy.data.scenes['Scene'].render.tile_x = 256
bpy.data.scenes['Scene'].render.tile_y = 256
bpy.data.scenes['Scene'].cycles.max_bounces = 4
bpy.data.scenes['Scene'].cycles.min_bounces = 0
bpy.data.scenes['Scene'].cycles.sample = 300

# number of images
nimg = 20 # number of patterns, 20
# name of object
obj_name = ['barrel', 'vase2']
# root directory of synthetic dataset
rdir = 'C:/Users/Admin/Documents/3D_Recon/Data/synthetic_data'
# input directory of the projection patterns
idir = '%s/blender_proj_script/textures/sl' % rdir

# hide all objects except the projector
bpy.data.objects['Sphere'].hide_render = True
bpy.data.objects['bottle'].hide_render = True
bpy.data.objects['king'].hide_render = True
bpy.data.objects['knight'].hide_render = True
bpy.data.objects['Lamp'].hide_render = False
bpy.data.objects['Point'].hide_render = True # used in calibration, TO-BE-DELETED
bpy.data.objects['Plane'].hide_render = True # used in calibration, TO-BE-DELETED
for ind_obj in range(0, len(obj_name)):
    if ind_obj == 0:
        bpy.data.objects['BarrelBulge'].hide_render = True
        bpy.data.objects['BarrelCircle'].hide_render = True
        bpy.data.objects['MetalRing'].hide_render = True
        bpy.data.objects['Planks'].hide_render = True
        bpy.data.objects['TopPlanks'].hide_render = True
    else:
        bpy.data.objects[obj_name[ind_obj]].hide_render = True

# get material nodes and projector texture image node
proj_nodes = bpy.data.lamps['Lamp'].node_tree.nodes
tex_node = proj_nodes.get('Image Texture')

for ind_obj in range(1, len(obj_name)):
    if ind_obj == 0:
        bpy.data.objects['Planks'].hide_render = False
        bpy.data.objects['TopPlanks'].hide_render = False
    else:
        bpy.data.objects[obj_name[ind_obj]].hide_render = False
        
    # output directory of rendered images
    outdir = '%s/synth/%s/sl' % (rdir, obj_name[ind_obj])
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
    
    if ind_obj == 0:
        bpy.data.objects['Planks'].hide_render = True
        bpy.data.objects['TopPlanks'].hide_render = True
    else:
        bpy.data.objects[obj_name[ind_obj]].hide_render = True
