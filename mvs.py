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

for img_ind in range(10, 11):
    texture = bpy.data.images.load('%s/%02d.jpg' % (idir, img_ind))
    nodes = bpy.data.materials['diffuse'].node_tree.nodes
    nodes.get("Image Texture").image = texture
    
    subdir = '%02d' % img_ind
    outdir = '%s/%s/visualize' % (odir, subdir)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    
    for cam_ind in range(0, 36):
        bpy.context.scene.camera = bpy.data.objects['Camera.%03d' % cam_ind]
        bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (outdir, cam_ind)
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