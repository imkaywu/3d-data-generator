import bpy
import os
import math
import mathutils

# output properties
bpy.data.scenes['Scene'].render.resolution_x = 1280 # 1920
bpy.data.scenes['Scene'].render.resolution_y = 720 # 1080
bpy.data.scenes['Scene'].render.resolution_percentage = 100
bpy.data.scenes['Scene'].render.tile_x = 256
bpy.data.scenes['Scene'].render.tile_y = 256
bpy.data.scenes['Scene'].cycles.max_bounces = 4
bpy.data.scenes['Scene'].cycles.min_bounces = 0
bpy.data.scenes['Scene'].cycles.sample = 300

calib_scan = 0 # 0: calib, 1: scan
angles = mathutils.Vector((-20.0, 0.0, 20.0)) * math.pi / 180.0
ndim = 3 # number of angles, 3
nimg = 20 # number of patterns, 20

# name of object
obj_name = 'sphere'
# root directory of synthetic dataset
rdir = 'C:/Users/Admin/Documents/3D_Recon/Data/synthetic_data'
# input directory of the projection patterns
idir = '%s/textures/sl' % rdir
#input directory of the textures
idir_tex = '%s/textures/texture01_10' % rdir
# output directory of rendered images
odir = '%s/%s/sl' % (rdir, obj_name)

if (calib_scan):
    bpy.data.objects['Point'].hide_render = True
    bpy.data.objects['Lamp'].hide_render = False
    bpy.data.objects['Plane_Calib'].hide_render = True
    bpy.data.objects['Plane'].hide_render = True

    proj_nodes = bpy.data.lamps['Lamp'].node_tree.nodes
    tex_node = proj_nodes.get('Image Texture')

    subdir = 'tex_spec'
    for ind_tex in range(2, 9, 3):
        texture = bpy.data.images.load('%s/%02d.jpg' % (idir_tex, ind_tex))
        nodes = bpy.data.materials['Material'].node_tree.nodes
        nodes.get("Image Texture").image = texture
        nodes["Group"].inputs[1].default_value = 0.0 # Roughness

        for ind_spec in range(2, 9, 3):
            nodes["Group"].inputs[2].default_value = ind_spec / 10.0 # Specular

            subsubdir = '%02d%02d' % (ind_tex, ind_spec)
            outdir = '%s/%s/%s' % (odir, subdir, subsubdir)

            if not os.path.exists(outdir):
                os.makedirs(outdir)

            for ind_img in range(0, nimg):
                proj_ptn = bpy.data.images.load("%s/sl_v%d.jpg" % (idir, ind_img))
                tex_node.image = proj_ptn
                bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (outdir, ind_img)
                bpy.ops.render.render(write_still=True)
                
                proj_ptn = bpy.data.images.load("%s/sl_h%d.jpg" % (idir, ind_img))
                tex_node.image = proj_ptn
                bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (outdir, ind_img + nimg)
                bpy.ops.render.render(write_still=True)
            
            for ind_img in range(0, 2):
                proj_ptn = bpy.data.images.load("%s/sl_a%d.jpg" % (idir, 1 - ind_img))
                tex_node.image = proj_ptn
                bpy.data.scenes['Scene'].render.filepath = '%s/%04d.jpg' % (outdir, ind_img + 2 * nimg)
                bpy.ops.render.render(write_still=True)
else:
    ## for future reference: I made some changes to the the output directory, but this part of code is left unchanged,
    ## it's might be necessary to change some lines of codes of the calibration part
    odir = 'C:/Users/Admin/Documents/3D_Recon/Data/synthetic_data/calib'
    ## render printed pattern
    bpy.data.objects['Point'].hide_render = False
    bpy.data.objects['Lamp'].hide_render = True
    bpy.data.objects['Plane'].hide_render = False
    
    plane_nodes = bpy.data.materials['Material.001'].node_tree.nodes
    plane_links = bpy.data.materials['Material.001'].node_tree.links
    
    if plane_nodes.find("Image Texture") < 0:
        tex_node = plane_nodes.new(type="ShaderNodeTexImage")
        plane_links.new(plane_nodes.get("Texture Coordinate").outputs[0], tex_node.inputs[0])
        plane_links.new(tex_node.outputs[0], plane_nodes.get("Diffuse BSDF").inputs[0])
    elif len(plane_nodes) - len(plane_links) != 1:
        tex_node = plane_nodes.get("Image Texture")
        plane_links.new(tex_node.outputs[0], plane_nodes.get("Diffuse BSDF").inputs[0])
    else:
        tex_node = plane_nodes.get("Image Texture")
    
    cam_ptn = bpy.data.images.load('%s/calibration_pattern.jpg' % idir)
    tex_node.image = cam_ptn
    
    plane_calib = bpy.data.objects['Plane']
    plane_calib.location[2] = 0
    for i in range(0, ndim):
        for j in range(0, ndim):
            plane_calib.rotation_euler[0] = angles[i]
            plane_calib.rotation_euler[1] = angles[j]
            bpy.data.scenes['Scene'].render.filepath = '%s/cam_%04d.jpg' % (odir, (i * ndim) + j)
            bpy.ops.render.render(write_still=True)
    
    plane_calib.location[2] = -1
    for i in range(0, ndim):
        for j in range(0, ndim):
            plane_calib.rotation_euler[0] = angles[i]
            plane_calib.rotation_euler[1] = angles[j]
            bpy.data.scenes['Scene'].render.filepath = '%s/cam_%04d.jpg' % (odir, (i * ndim) + j + ndim * ndim)
            bpy.ops.render.render(write_still=True)
    
    ## render projected pattern
    bpy.data.objects['Point'].hide_render = True
    bpy.data.objects['Lamp'].hide_render = False
    bpy.data.objects['Plane'].hide_render = False
    
    # remove the texture node in Plane_Calib
    for ind_link in range(0, len(plane_links)):
        if plane_links[ind_link].from_node.name == "Image Texture":
            plane_links.remove(plane_links[ind_link])
    
    # load projection_pattern to Projector
    proj_ptn = bpy.data.images.load("%s/projection_pattern.bmp" % idir)
    proj_nodes = bpy.data.lamps['Lamp'].node_tree.nodes
    tex_node = proj_nodes.get('Image Texture')
    tex_node.image = proj_ptn
    
    plane_calib.location[2] = 0
    for i in range(0, ndim):
        for j in range(0, ndim):
            plane_calib.rotation_euler[0] = angles[i]
            plane_calib.rotation_euler[1] = angles[j]
            bpy.data.scenes['Scene'].render.filepath = '%s/proj_%04d.jpg' % (odir, (i * ndim) + j)
            bpy.ops.render.render(write_still=True)
    
    plane_calib.location[2] = -1
    for i in range(0, ndim):
        for j in range(0, ndim):
            plane_calib.rotation_euler[0] = angles[i]
            plane_calib.rotation_euler[1] = angles[j]
            bpy.data.scenes['Scene'].render.filepath = '%s/proj_%04d.jpg' % (odir, (i * ndim) + j + ndim * ndim)
            bpy.ops.render.render(write_still=True)