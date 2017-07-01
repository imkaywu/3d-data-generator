import bpy
import os
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
obj_name = 'sphere'
# number of images
nimages = 25
# root directory of synthetic dataset
rdir = 'C:/Users/Admin/Documents/3D_Recon/Data/synthetic_data'
# output directory of rendered images
odir = '%s/%s/train/ps' % (rdir, obj_name)
# list of properties
props = ['tex', 'alb', 'spec', 'rough', 'concav']
# index of effective properties
ind_props = [1, 2, 3]
# get material nodes
nodes = bpy.data.materials['Material'].node_tree.nodes
# set the object visible
bpy.data.objects['Sphere'].hide_render = False

# hide all the light sources
for ind_light in range(0, nimages):
	bpy.data.objects['Lamp.%03d' % ind_light].hide_render = True

set_prop_val(nodes, 0, 2) # set texture to 0.2
for ind_1 in range(2, 9, 3):
	set_prop_val(nodes, ind_props[0], ind_1)

	for ind_2 in range(2, 9, 3):
		set_prop_val(nodes, ind_props[1], ind_2)

		for ind_3 in range(2, 9, 3):
			set_prop_val(nodes, ind_props[2], ind_3)

			subdir = '00%02d%02d%02d' % (ind_1, ind_2, ind_3) # change if ind_props changes
			outdir = '%s/%s' % (odir, subdir)

			if not os.path.exists(outdir):
				os.makedirs(outdir)

			for ind_light in range(0, nimages):
				bpy.data.objects['Lamp.%03d' % ind_light].hide_render = False
				bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (outdir, ind_light)
				bpy.ops.render.render(write_still=True)
				bpy.data.objects['Lamp.%03d' % ind_light].hide_render = True