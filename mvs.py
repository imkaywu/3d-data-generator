import bpy

# output properties
bpy.data.scenes['Scene'].render.resolution_x = 1028 # 1920
bpy.data.scenes['Scene'].render.resolution_y = 720 # 1080
bpy.data.scenes['Scene'].render.resolution_percentage = 50
bpy.data.scenes['Scene'].render.tile_x = 64
bpy.data.scenes['Scene'].render.tile_y = 64
bpy.data.scenes['Scene'].cycles.sample = 500

for cam_ind in range(0, 3):
    bpy.context.scene.camera = bpy.data.objects['Camera.%03d' % cam_ind]
    bpy.data.scenes['Scene'].render.filepath = 'C:/Users/Daniela/Documents/3D_Recon/Data/synthetic_data/testing/image_%04d.jpg' % cam_ind
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