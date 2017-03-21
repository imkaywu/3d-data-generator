import bpy

# output properties
bpy.data.scenes['Scene'].render.resolution_x = 1028 # 1920
bpy.data.scenes['Scene'].render.resolution_y = 720 # 1080
bpy.data.scenes['Scene'].render.resolution_percentage = 50
bpy.data.scenes['Scene'].render.tile_x = 64
bpy.data.scenes['Scene'].render.tile_y = 64
bpy.data.scenes['Scene'].cycles.sample = 500

for ind_light in range(0, 24):
    bpy.data.objects['Lamp.%03d' % ind_light].hide_render = True
    
for ind_light in range(0, 3):
    bpy.data.objects['Lamp.%03d' % ind_light].hide_render = False
    bpy.data.scenes['Scene'].render.filepath = 'C:/Users/Daniela/Documents/3D_Recon/Data/synthetic_data/testing/%04d.jpg' % ind_light
    bpy.ops.render.render(write_still=True)
    bpy.data.objects['Lamp.%03d' % ind_light].hide_render = True