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
# number of images
nimages = len(bpy.data.objects) - 7;
# root directory of synthetic dataset
rdir = 'C:/Users/Admin/Documents/3D_Recon/Data/synthetic_data'
# input directory of the calibration patterns
idir = '%s/textures/texture01_10' % rdir
# output directory of rendered images
odir = '%s/%s/mvs' % (rdir, obj_name)

subdir = 'tex_spec'
for ind_tex in range(2, 9, 3):
    texture = bpy.data.images.load('%s/%02d.jpg' % (idir, ind_tex))
    nodes = bpy.data.materials['Material'].node_tree.nodes
    nodes.get("Image Texture").image = texture

    # nodes.get("Principled BSDF").inputs[7].default_value = 0.0 # Roughness
    nodes["Group"].inputs[1].default_value = 0.0 # Roughness
	
    for ind_spec in range(2, 9, 3):
        # nodes.get("Principled BSDF").inputs[5].default_value = ind_spec / 100.0 # Specular
        nodes["Group"].inputs[2].default_value = ind_spec / 10.0 # Specular
        
        subsubdir = '%02d%02d' % (ind_tex, ind_spec)
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