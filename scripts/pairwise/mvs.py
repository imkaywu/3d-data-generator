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
nimages = len(bpy.data.objects) - 3;
# root directory of synthetic dataset
rdir = 'C:/Users/Admin/Documents/3D_Recon/Data/synthetic_data'
# output directory of rendered images
odir = '%s/%s/mvs' % (rdir, obj_name)
# list of properties
props = ['tex', 'alb', 'spec', 'rough']
# obtain the nodes
nodes = bpy.data.materials['Material'].node_tree.nodes
# set the object visible
bpy.data.objects['Sphere'].hide_render = False

for i in range(0, len(props)):
	for j in range(i + 1, len(props)):
		subdir = '%s_%s' % (props[i], props[j])
		set_prop_val(nodes, 0, 8) # Texture
		set_prop_val(nodes, 1, 8) # Albedo
		set_prop_val(nodes, 2, 0) # Specular
		set_prop_val(nodes, 3, 0) # Roughness

		for ind_1 in range(2, 9, 3):
			set_prop_val(nodes, i, ind_1)

			for ind_2 in range(2, 9, 3):
				set_prop_val(nodes, j, ind_2)

				subsubdir = '%02d%02d' % (ind_1, ind_2)
				outdir = '%s/%s/%s/visualize' % (odir, subdir, subsubdir)
				if not os.path.exists(outdir):
					os.makedirs(outdir)

				for ind_cam in range(0, nimages):
					bpy.context.scene.camera = bpy.data.objects['Camera.%03d' % ind_cam]
					bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (outdir, ind_cam)
					bpy.ops.render.render(write_still=True)


# scene = bpy.context.scene
# currentcam = bpy.context.scene.camera
# setcam = False

# for ob in scene.objects:
#     if ob.type == 'CAMERA':
#         if ob == currentcam:
#             setcam = True
#         elif setcam:
#             bpy.context.scene.camera = ob
#             break

# if currentcam == bpy.context.scene.camera:      
#     for ob in scene.objects:
#         if ob.type == 'CAMERA':
#             bpy.context.scene.camera = ob
#             break