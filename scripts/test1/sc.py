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
obj_name = ['barrel', 'vase2']
# number of images
nimages = 41;
# root directory of synthetic dataset
rdir = 'C:/Users/Admin/Documents/3D_Recon/Data/synthetic_data/synth'
# set the object invisible
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
# set up the lighting
for ilight in range(0, 8):
	bpy.data.objects['Point.%03d' % ilight].hide_render = False

# green screen
nodes_world = bpy.data.worlds['World'].node_tree.nodes
links_world = bpy.data.worlds['World'].node_tree.links
links_world.remove(links_world[1])
links_world.new(nodes_world.get("Light Path").outputs[0], nodes_world.get("Background").inputs[1])

for iobj in range(1, len(obj_name)):
	# set obj visible
	if ind_obj == 0:
		bpy.data.objects['Planks'].hide_render = False
		bpy.data.objects['TopPlanks'].hide_render = False
	else:
		bpy.data.objects[obj_name[ind_obj]].hide_render = False
	# output directory of rendered images
	odir = '%s/%s/vh' % (rdir, obj_name[iobj])

	if not os.path.exists(odir):
	    os.makedirs(odir)

	for ind_cam in range(0, nimages):
	    bpy.context.scene.camera = bpy.data.objects['Camera.%03d' % ind_cam]
	    bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (odir, ind_cam)
	    bpy.ops.render.render(write_still=True)

	if ind_obj == 0:
		bpy.data.objects['Planks'].hide_render = True
		bpy.data.objects['TopPlanks'].hide_render = True
	else:
		bpy.data.objects[obj_name[ind_obj]].hide_render = True

links_world.remove(links_world[1])
links_world.new(nodes_world.get("Environment Texture").outputs[0], nodes_world.get("Background").inputs[1])
