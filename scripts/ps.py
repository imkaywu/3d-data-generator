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
bpy.data.scenes['Scene'].cycles.sample = 300
bpy.context.scene.cycles.device = 'GPU'

# input directory of the calibration patterns
idir = 'C:/Users/Admin/Documents/3D Recon/Data/synthetic data/textures/texture00-10'
# output directory of rendered images
odir = 'C:/Users/Admin/Documents/3D Recon/Data/synthetic data/test'

for ind_tex in range(1, 11):
	texture = bpy.data.images.load('%s/%02d.jpg' % (idir, ind_tex))
	nodes = bpy.data.materials['mixed.000'].node_tree.nodes
	nodes.get("Image Texture").image = texture
	
	subdir = 'ps/%02d' % ind_tex
	outdir = '%s/%s/visualize' % (odir, subdir)
	if not os.path.exists(outdir):
		os.makedirs(outdir)
	
	for ind_light in range(0, 24):
		bpy.data.objects['Lamp.%03d' % ind_light].hide_render = True
    
	for ind_light in range(0, 24):
		bpy.data.objects['Lamp.%03d' % ind_light].hide_render = False
		bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (outdir, ind_light)
		bpy.ops.render.render(write_still=True)
		bpy.data.objects['Lamp.%03d' % ind_light].hide_render = True