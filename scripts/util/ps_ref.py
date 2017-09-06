import bpy
import os

# output properties
bpy.data.scenes['Scene'].render.resolution_x = 1280 # 1920
bpy.data.scenes['Scene'].render.resolution_y = 720 # 1080
bpy.data.scenes['Scene'].render.resolution_percentage = 100
bpy.data.scenes['Scene'].render.tile_x = 256
bpy.data.scenes['Scene'].render.tile_y = 256
bpy.data.scenes['Scene'].cycles.max_bounces = 4
bpy.data.scenes['Scene'].cycles.min_bounces = 0
bpy.data.scenes['Scene'].cycles.sample = 500

# number of light sources
nimg = 25
# root directory of synthetic dataset
rdir = 'C:/Users/Admin/Documents/3D_Recon/Data/synthetic_data'
# output directory of rendered images
odir = '%s/3DRecon_Algo_Eval/data/synth/ref_obj' % rdir

# hide all the light sources
for ind_light in range(0, nimg):
	bpy.data.objects['Lamp.%03d' % ind_light].hide_render = True

# hide the target object (manually)

for ind_ref in range(0, 2):
    bpy.data.objects['Sphere.%03d' % ind_ref].hide_render = True

# generate reference object
for ind_ref in range(0, 2):
    outdir = '%s/%04d' % (odir, ind_ref)
    bpy.data.objects['Sphere.%03d' % ind_ref].hide_render = False

    if not os.path.exists(outdir):
    	os.makedirs(outdir)

    for ind_light in range(0, nimg):
    	bpy.data.objects['Lamp.%03d' % ind_light].hide_render = False
    	bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (outdir, ind_light)
    	bpy.ops.render.render(write_still=True)
    	bpy.data.objects['Lamp.%03d' % ind_light].hide_render = True
    
    bpy.data.objects['Sphere.%03d' % ind_ref].hide_render = True

# generate mask images

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

for ind_ref in range(0, 2):
    bpy.data.objects['Sphere.%03d' % ind_ref].hide_render = False

    outdir = '%s/mask' % odir
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (outdir, ind_ref)
    bpy.ops.render.render(write_still=True)
    
    bpy.data.objects['Sphere.%03d' % ind_ref].hide_render = True

bpy.data.objects['Lamp.000'].hide_render = True
bpy.data.objects['Lamp.001'].hide_render = True
bpy.data.objects['Lamp.005'].hide_render = True
bpy.data.objects['Lamp.007'].hide_render = True
bpy.data.objects['Lamp.009'].hide_render = True
links_world.remove(links_world[1])
nodes_world["Background"].inputs['Color'].default_value = [0.01, 0.01, 0.01, 1]
