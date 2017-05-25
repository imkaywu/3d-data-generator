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
# root directory of synthetic dataset
rdir = 'C:/Users/Admin/Documents/3D_Recon/Data/synthetic_data'
# output directory of rendered images
odir = '%s/%s/ps' % (rdir, obj_name)
# list of properties
props = ['tex', 'alb', 'spec', 'rough', 'concav']
# obtain the nodes
nodes = bpy.data.materials['Material'].node_tree.nodes
# set the object visible
bpy.data.objects['Sphere'].hide_render = False

# hide all the light sources
for ind_light in range(0, 24):
	bpy.data.objects['Lamp.%03d' % ind_light].hide_render = True

gen_data = 1
if gen_data:
	for i in range(0, 4):
		for j in range(i + 1, 4):
			subdir = '%s_%s' % (props[i], props[j])
			set_prop_val(nodes, 0, 0) # Texture
			set_prop_val(nodes, 1, 10) # Albedo
			set_prop_val(nodes, 2, 0) # Specular
			set_prop_val(nodes, 3, 0) # Roughness

			for ind_1 in range(2, 9, 3):
				set_prop_val(nodes, i, ind_1)

				for ind_2 in range(2, 9, 3):
					set_prop_val(nodes, j, ind_2)

					subsubdir = '%02d%02d' % (ind_1, ind_2)
					outdir = '%s/%s/%s' % (odir, subdir, subsubdir)

					if not os.path.exists(outdir):
						os.makedirs(outdir)

					for ind_light in range(0, 24):
						bpy.data.objects['Lamp.%03d' % ind_light].hide_render = False
						bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (outdir, ind_light)
						bpy.ops.render.render(write_still=True)
						bpy.data.objects['Lamp.%03d' % ind_light].hide_render = True
else:
	# get the mask
	nodes = bpy.data.materials['Material'].node_tree.nodes
	set_prop_val(nodes, 0, 0.0) # texture = 0.0
	set_prop_val(nodes, 1, 1.0) # albedo = 1.0
	set_prop_val(nodes, 2, 0.0) # specularity = 0.0
	set_prop_val(nodes, 3, 0.0) # roughness = 0.0
	for ind_light in range(0, 24):
		bpy.data.objects['Lamp.%03d' % ind_light].hide_render = False
	bpy.data.scenes['Scene'].render.filepath = '%s/%s/gt/mask.bmp' % (rdir, obj_name)
	bpy.ops.render.render(write_still=True)