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

# number of images
nimages = len(bpy.data.objects) - 7;
# root directory of synthetic dataset
rdir = 'C:/Users/Admin/Documents/3D_Recon/Data/synthetic_data'
# output directory of rendered images
odir = '%s/sphere/vh/mask' % rdir
# odir = '%s/sphere/vh/visualize' % rdir

for ind_light in range(0, 6):
	bpy.data.objects['Lamp.%03d' % ind_light].hide_render = False

for ind_cam in range(0, nimages):
    bpy.context.scene.camera = bpy.data.objects['Camera.%03d' % ind_cam]
    bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (odir, ind_cam)
    bpy.ops.render.render(write_still=True)

for ind_light in range(0, 6):
	bpy.data.objects['Lamp.%03d' % ind_light].hide_render = True