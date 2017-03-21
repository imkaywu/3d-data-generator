import bpy
import math
import mathutils

deg2rad = math.pi/180.0
calib_scan = 0 # 0: calib, 1: scan
angles = mathutils.Vector((-20.0, 0.0, 20.0))
dim = 3
num = 2 # number of patterns

# input directory of the calibration patterns
idir = 'C:/Users/Daniela/Documents/3D_Recon/Data/synthetic_data/textures/sl'
# output directory of rendered images
odir = 'C:/Users/Daniela/Documents/3D_Recon/Data/synthetic_data/testing'

if (calib_scan == 0):
    ## render printed pattern
    bpy.data.objects['Point'].hide_render = False
    bpy.data.objects['Lamp'].hider_render = True
    bpy.data.objects['Plane_Calib'].hide_render = False
    bpy.data.objects['Plane'].hide_render = True
    
    plane_calib = bpy.data.objects['Plane_Calib']
    plane_calib.location[2] = 0
    for i in range(0, dim):
        for j in range(0, dim):
            plane.calib.rotation_euler[0] = angles[i]
            plane.calib.rotation_euler[1] = angles[j]
            bpy.data.scenes['Scene'].render.filepath = '%s/cam_%04d.jpg' % (odir, (i * dim) + j)
            bpy.ops.render.render(write_still=True)
    
    # plane_calib.location[2] = 5
    # for i in range(0, dim):
    #     for j in range(0, dim):
    #         plane.calib.rotation_euler[0] = angles[i]
    #         plane.calib.rotation_euler[1] = angles[j]
    #         bpy.data.scenes['Scene'].render.filepath = '%s/cam_%04d.jpg' % (odir, (i * dim) + j + dim * dim)
    #         bpy.ops.render.render(write_still=True)
    
    # ## render projected pattern
    # bpy.data.objects['Point'].hide_render = True
    # bpy.data.objects['Lamp'].hider_render = False
    # bpy.data.objects['Plane_Calib'].hide_render = False
    # bpy.data.objects['Plane'].hide_render = True
    
    # # remove the texture node in Plane_Calib
    # plane_nodes = bpy.data.materials['Material.000'].node_tree.nodes
    # tex_node = plane_nodes.get('Image Texture')
    # plane_nodes.remove(tex_node)
    
    # # load projection_pattern to Projector
    # proj_ptn = bpy.data.images.load("%s/projection_pattern.jpg" % idir)
    # proj_nodes = bpy.data.lamps['Lamp'].node_tree.nodes
    # tex_node = proj_nodes.get('Image Texture')
    # tex_node.image = proj_ptn
    
    # plane_calib.location[2] = 0
    # for i in range(0, dim):
    #     for j in range(0, dim):
    #         plane.calib.rotation_euler[0] = angles[i]
    #         plane.calib.rotation_euler[1] = angles[j]
    #         bpy.data.scenes['Scene'].render.filepath = '%s/proj_%04d.jpg' % (odir, (i * dim) + j)
    #         bpy.ops.render.render(write_still=True)
    
    # plane_calib.location[2] = 5
    # for i in range(0, dim):
    #     for j in range(0, dim):
    #         plane.calib.rotation_euler[0] = angles[i]
    #         plane.calib.rotation_euler[1] = angles[j]
    #         bpy.data.scenes['Scene'].render.filepath = '%s/proj_%04d.jpg' % (odir, (i * dim) + j + dim * dim)
    #         bpy.ops.render.render(write_still=True)
# else:
#     bpy.data.objects['Point'].hide_render = True
#     bpy.data.objects['Lamp'].hider_render = False
#     bpy.data.objects['Plane_Calib'].hide_render = True
#     bpy.data.objects['Plane'].hide_render = False

#     proj_nodes = bpy.data.lamps['Lamp'].node_tree.nodes
#     tex_node = proj_nodes.get('Image Texture')
    
#     for ind_img in range(0, num):
#         proj_ptn = bpy.data.images.load("%s/sl_v%d.jpg" % (idir, ind_img))
#         tex_node.image = proj_ptn
#         bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (odir, ind_img)
#         bpy.ops.render.render(write_still=True)
        
#         proj_ptn = bpy.data.images.load("%s/sl_h%d.jpg" % (idir, ind_img))
#         tex_node_image = proj_ptn
#         bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (odir, ind_img + num)
#         bpy.ops.render.render(write_still=True)
        
#     for ind_img in range(0, 2):
#         proj_ptn = bpy.data.images.load("%s/sl_a%d.jpg" % (idir, 1 - ind_img))
#         tex_node.image = proj_ptn
#         bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (odir, ind_img + 2 * num)
#         bpy.ops.render.render(write_still=True)