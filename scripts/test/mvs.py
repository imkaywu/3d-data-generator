import bpy
import os
import numpy
import sys
sys.path.append('./scripts')
from helper import set_prop_val

# output properties
bpy.data.scenes['Scene'].render.resolution_x = 1280 # 1920
bpy.data.scenes['Scene'].render.resolution_y = 720 # 1080
bpy.data.scenes['Scene'].render.resolution_percentage = 100
bpy.data.scenes['Scene'].render.tile_x = 256
bpy.data.scenes['Scene'].render.tile_y = 256
bpy.data.scenes['Scene'].cycles.max_bounces = 4
bpy.data.scenes['Scene'].cycles.min_bounces = 0
bpy.data.scenes['Scene'].cycles.sample = 300

# name of object
obj_name = ['cup', 'vase', 'pot']
# number of images
nimages = len(bpy.data.objects) - 11;
# root directory of synthetic dataset
rdir = 'C:/Users/Admin/Documents/3D_Recon/Data/synthetic_data'
# list of properties
ind_prop = numpy.matrix([[2, 2, 2, 5], [2, 2, 8, 2], [2, 8, 2, 5], [8, 2, 2, 5]])

# hide all objects
bpy.data.objects['Circle.002'].hide_render = True
bpy.data.objects['Circle.001'].hide_render = True
bpy.data.objects['Cylinder'].hide_render = True

# get material nodes
nodes = bpy.data.materials['Material'].node_tree.nodes

for ind_obj in range(2, 3):
    # output directory of rendered images
    odir = '%s/%s' % (rdir, obj_name[ind_obj])
    if ind_obj == 0:
        bpy.data.objects['Cylinder'].hide_render = False
    elif ind_obj == 1:
        bpy.data.objects['Circle.001'].hide_render = False
    else:
        bpy.data.objects['Circle.002'].hide_render = False

    for row in range(1, 2):
        subdir = '%02d%02d%02d%02d' % (ind_prop[row, 0], ind_prop[row, 1], ind_prop[row, 2], ind_prop[row, 3])

        # set the other properties to default values
        nodes["Group"].inputs[1].default_value = ind_prop[row, 0] / 10.0 # Texture
        nodes["Group"].inputs[2].default_value = ind_prop[row, 1] / 10.0 # Albedo
        nodes.get("Principled BSDF").inputs[5].default_value = ind_prop[row, 2] # Specular
        nodes.get("Principled BSDF").inputs[7].default_value = ind_prop[row, 3] / 10.0 # Roughness

        outdir = '%s/mvs/%s/visualize' % (odir, subdir)
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        
        for ind_cam in range(0, nimages):
            bpy.context.scene.camera = bpy.data.objects['Camera.%03d' % ind_cam]
            bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (outdir, ind_cam)
            bpy.ops.render.render(write_still=True)

    if ind_obj == 0:
        bpy.data.objects['Cylinder'].hide_render = True
    elif ind_obj ==  1:
        bpy.data.objects['Circle.001'].hide_render = True
    else:
        bpy.data.objects['Circle.002'].hide_render = True