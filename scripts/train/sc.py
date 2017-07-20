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
nimages = 41;
# root directory of synthetic dataset
rdir = 'C:/Users/Admin/Documents/3D_Recon/Data/synthetic_data'
# output directory of rendered images
odir = '%s/%s/train/sc' % (rdir, obj_name)
# get material nodes
nodes = bpy.data.materials['Material'].node_tree.nodes
# set the object visible
bpy.data.objects['Sphere'].hide_render = False
bpy.data.objects['Point'].hide_render = False
bpy.data.objects['Point.001'].hide_render = False
bpy.data.objects['Point.002'].hide_render = False
bpy.data.objects['Point.003'].hide_render = False

set_prop_val(nodes, 0, 10) # texture
set_prop_val(nodes, 1, 10) # albedo
set_prop_val(nodes, 2, 0); # specular
set_prop_val(nodes, 3, 0); # roughness

nodes_world = bpy.data.worlds['World'].node_tree.nodes
links_world = bpy.data.worlds['World'].node_tree.links
links_world.remove(links_world[1])
links_world.new(nodes_world.get("Light Path").outputs[0], nodes_world.get("Background").inputs[1])

if not os.path.exists(odir):
    os.makedirs(odir)

for ind_cam in range(0, nimages):
    bpy.context.scene.camera = bpy.data.objects['Camera.%03d' % ind_cam]
    bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (odir, ind_cam)
    bpy.ops.render.render(write_still=True)

bpy.data.objects['Point'].hide_render = True
bpy.data.objects['Point.001'].hide_render = True
bpy.data.objects['Point.002'].hide_render = True
bpy.data.objects['Point.003'].hide_render = True
links_world.remove(links_world[1])
links_world.new(nodes_world.get("Environment Texture").outputs[0], nodes_world.get("Background").inputs[1])
