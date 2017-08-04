import bpy
import os
import sys
sys.path.append('./scripts/util')
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
obj_name = 'sphere'
# number of images
nimages = 25
# root directory of synthetic dataset
rdir = 'C:/Users/Admin/Documents/3D_Recon/Data/synthetic_data'
# output directory of rendered images
odir = '%s/%s/train/ps_baseline' % (rdir, obj_name)
# list of properties
# props = ['tex', 'alb', 'spec', 'rough', 'concav']
# index of effective properties
ind_prop = [2, 8, 0, 8]
# get material nodes
nodes = bpy.data.materials['Material'].node_tree.nodes
# set the object visible
bpy.data.objects['Sphere'].hide_render = False
bpy.data.objects['ball'].hide_render = True
bpy.data.objects['cup'].hide_render = True
bpy.data.objects['king'].hide_render = True
bpy.data.objects['knight'].hide_render = True

# hide all the light sources
for ind_light in range(0, nimages):
	bpy.data.objects['Lamp.%03d' % ind_light].hide_render = True

set_prop_val(nodes, 0, ind_prop[0]) # set texture
set_prop_val(nodes, 1, ind_prop[1]) # set albedo
set_prop_val(nodes, 2, ind_prop[2]) # set specular
set_prop_val(nodes, 3, ind_prop[3]) # set roughness

outdir = odir
if not os.path.exists(outdir):
	os.makedirs(outdir)

for ind_light in range(0, nimages):
	bpy.data.objects['Lamp.%03d' % ind_light].hide_render = False
	bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (outdir, ind_light)
	bpy.ops.render.render(write_still=True)
	bpy.data.objects['Lamp.%03d' % ind_light].hide_render = True