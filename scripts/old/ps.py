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

# name of object
obj_name = 'sphere'
# root directory of synthetic dataset
rdir = 'C:/Users/Admin/Documents/3D_Recon/Data/synthetic_data'
# input directory of the calibration patterns
idir = '%s/textures/texture01_10' % rdir
# output directory of rendered images
odir = '%s/%s/ps' % (rdir, obj_name)

# hide all the light sources
for ind_light in range(0, 24):
	bpy.data.objects['Lamp.%03d' % ind_light].hide_render = True

gen_data = 1
if gen_data:
	subdir = 'tex_spec'
	for ind_tex in range(2, 9, 3):
		texture = bpy.data.images.load('%s/%02d.jpg' % (idir, ind_tex))
		nodes = bpy.data.materials['Material'].node_tree.nodes
		nodes.get("Image Texture").image = texture
		# nodes.get("Principled BSDF").inputs[7].default_value = 0.0 # Roughness
		nodes["Group"].inputs[1].default_value = 0.2 # Roughness

		for ind_spec in range(2, 9, 3):
			# nodes.get("Principled BSDF").inputs[5].default_value = ind_spec / 100.0 # Specular
			nodes["Group"].inputs[2].default_value = ind_spec / 10.0 # Specular

			subsubdir = '%02d%02d' % (ind_tex, ind_spec)
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
	nodes.get("Image Texture").image = bpy.data.images.load('%s/textures/allone.bmp' % rdir)
	nodes["Group"].inputs[1].default_value = 0.0
	nodes["Group"].inputs[2].default_value = 0.0
	for ind_light in range(0, 24):
		bpy.data.objects['Lamp.%03d' % ind_light].hide_render = False
	bpy.data.scenes['Scene'].render.filepath = '%s/%s/gt/mask.bmp' % (rdir, obj_name)
	bpy.ops.render.render(write_still=True)