import bpy
import os
import numpy
import sys

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
obj_name = ['barrel', 'vase2']
# number of images
nimages = 25
# root directory of synthetic dataset
rdir = 'C:/Users/Admin/Documents/3D_Recon/Data/synthetic_data'

# hide all the light sources
for ind_light in range(0, nimages):
	bpy.data.objects['Lamp.%03d' % ind_light].hide_render = True

# hide all objects except the projector
bpy.data.objects['Sphere'].hide_render = True
bpy.data.objects['bottle'].hide_render = True
bpy.data.objects['king'].hide_render = True
bpy.data.objects['knight'].hide_render = True
for ind_obj in range(0, len(obj_name)):
    if ind_obj == 0:
        bpy.data.objects['BarrelBulge'].hide_render = True
        bpy.data.objects['BarrelCircle'].hide_render = True
        bpy.data.objects['MetalRing'].hide_render = True
        bpy.data.objects['Planks'].hide_render = True
        bpy.data.objects['TopPlanks'].hide_render = True
    else:
        bpy.data.objects[obj_name[ind_obj]].hide_render = True

for ind_obj in range(1, len(obj_name)):
    if ind_obj == 0:
        bpy.data.objects['Planks'].hide_render = False
        bpy.data.objects['TopPlanks'].hide_render = False
    else:
        bpy.data.objects[obj_name[ind_obj]].hide_render = False

    # output directory of rendered images
    outdir = '%s/synth/%s/ps' % (rdir, obj_name[ind_obj])
    if not os.path.exists(outdir):
    	os.makedirs(outdir)

    for ind_light in range(0, nimages):
        bpy.data.objects['Lamp.%03d' % ind_light].hide_render = False
        bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (outdir, ind_light)
        bpy.ops.render.render(write_still=True)
        bpy.data.objects['Lamp.%03d' % ind_light].hide_render = True
    
    if ind_obj == 0:
        bpy.data.objects['Planks'].hide_render = True
        bpy.data.objects['TopPlanks'].hide_render = True
    else:
        bpy.data.objects[obj_name[ind_obj]].hide_render = True
