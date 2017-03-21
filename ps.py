import bpy

for ind_light in range(0, 24):
    bpy.data.objects['Lamp.%03d' % ind_light].hide_render = True
    
for ind_light in range(0, 3):
    bpy.data.objects['Lamp.%03d' % ind_light].hide_render = False
    bpy.data.scenes['Scene'].render.filepath = 'C:/Users/Daniela/Documents/3D_Recon/Data/synthetic_data/testing/%04d.jpg' % ind_light
    bpy.ops.render.render(write_still=True)
    bpy.data.objects['Lamp.%03d' % ind_light].hide_render = True