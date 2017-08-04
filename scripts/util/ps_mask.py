import bpy
import os
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
obj_name = ['bottle', 'cup', 'king', 'knight', 'Sphere']
# root directory of synthetic dataset
rdir = 'C:/Users/Admin/Documents/3D_Recon/Data/synthetic_data'
# get material nodes
nodes = bpy.data.materials['Material'].node_tree.nodes
# set the object invisible
bpy.data.objects['Sphere'].hide_render = True
bpy.data.objects['ball'].hide_render = True
bpy.data.objects['bottle'].hide_render = True
bpy.data.objects['cup'].hide_render = True
bpy.data.objects['king'].hide_render = True
bpy.data.objects['knight'].hide_render = True
# hide all the light sources
for ind_light in range(0, 24):
	bpy.data.objects['Lamp.%03d' % ind_light].hide_render = True

# green screen
nodes_world = bpy.data.worlds['World'].node_tree.nodes
links_world = bpy.data.worlds['World'].node_tree.links
links_world.new(nodes_world.get("Light Path").outputs[0], nodes_world.get("Background").inputs[1])
nodes_world["Background"].inputs['Color'].default_value = [0.0, 0.8, 0.0, 1]

bpy.data.objects['Lamp.000'].hide_render = False
bpy.data.objects['Lamp.001'].hide_render = False
bpy.data.objects['Lamp.005'].hide_render = False
bpy.data.objects['Lamp.007'].hide_render = False
bpy.data.objects['Lamp.009'].hide_render = False

for iobj in range(0, len(obj_name) - 1):
	bpy.data.objects[obj_name[iobj]].hide_render = False
	# output directory of rendered images
	if iobj == len(obj_name) - 1:
		odir = '%s/%s' % (rdir, obj_name[iobj])
	else:
		odir = '%s/testing/%s' % (rdir, obj_name[iobj])

	outdir = '%s/gt' % odir
	if not os.path.exists(outdir):
		os.makedirs(outdir)

	bpy.data.scenes['Scene'].render.filepath = '%s/mask_rgb.jpg' % outdir
	bpy.ops.render.render(write_still=True)

	bpy.data.objects[obj_name[iobj]].hide_render = True

bpy.data.objects['Lamp.000'].hide_render = True
bpy.data.objects['Lamp.001'].hide_render = True
bpy.data.objects['Lamp.005'].hide_render = True
bpy.data.objects['Lamp.007'].hide_render = True
bpy.data.objects['Lamp.009'].hide_render = True
links_world.remove(links_world[1])
nodes_world["Background"].inputs['Color'].default_value = [0.01, 0.01, 0.01, 1]
