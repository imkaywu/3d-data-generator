import bpy
import os
import math
import mathutils
import sys
sys.path.append('./scripts')
from helper import set_prop_val

# output properties
bpy.data.scenes['Scene'].render.resolution_x = 1024
bpy.data.scenes['Scene'].render.resolution_y = 768
bpy.data.scenes['Scene'].render.resolution_percentage = 100
bpy.data.scenes['Scene'].render.tile_x = 256
bpy.data.scenes['Scene'].render.tile_y = 256
bpy.data.scenes['Scene'].cycles.max_bounces = 4
bpy.data.scenes['Scene'].cycles.min_bounces = 0
bpy.data.scenes['Scene'].cycles.sample = 300

angles_x = mathutils.Vector((0.0, 20.0, 0.0, 20.0)) * math.pi / 180.0
angles_y = mathutils.Vector((0.0, 0.0, 20.0, 20.0)) * math.pi / 180.0
ngroups = 4 # number of angles, 3
nimg = 20 # number of patterns, 20

# root directory of synthetic dataset
rdir = 'C:/Users/Admin/Documents/3D_Recon/Data/synthetic_data'
# input directory of the projection patterns
idir = '%s/textures/sl' % rdir
# output directory of rendered images
odir = '%s/cam_proj_calib' % rdir

# set the calibration plane and projector visible
bpy.data.objects['Plane'].hide_render = False
bpy.data.objects['Lamp'].hide_render = False
bpy.data.objects['Sphere'].hide_render = True

# material node and link of calibration plane
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

# assign checkboard to plane_calib
cam_ptn = bpy.data.images.load('%s/calibration_pattern.jpg' % idir)
tex_node.image = cam_ptn

# get calibration plane
plane_calib = bpy.data.objects['Plane']
plane_calib.location[2] = 0

# get projector and the corresponding texture node
proj_nodes = bpy.data.lamps['Lamp'].node_tree.nodes
tex_node = proj_nodes.get('Image Texture')

for i in range(0, ngroups):
    outdir = '%s/set_%02d' % (odir, i)
    plane_calib.rotation_euler[0] = angles_x[i]
    plane_calib.rotation_euler[1] = angles_y[i]

    for ind_img in range(0, 2):
        proj_ptn = bpy.data.images.load("%s/sl_a%d.jpg" % (idir, 1 - ind_img))
        tex_node.image = proj_ptn
        bpy.data.scenes['Scene'].render.filepath = '%s/%02d.jpg' % (outdir, ind_img + 1)
        bpy.ops.render.render(write_still=True)

    for ind_img in range(0, nimg):
        proj_ptn = bpy.data.images.load("%s/sl_v%d.jpg" % (idir, ind_img))
        tex_node.image = proj_ptn
        bpy.data.scenes['Scene'].render.filepath = '%s/%02d.jpg' % (outdir, ind_img + 3)
        bpy.ops.render.render(write_still=True)

        proj_ptn = bpy.data.images.load("%s/sl_h%d.jpg" % (idir, ind_img))
        tex_node.image = proj_ptn
        bpy.data.scenes['Scene'].render.filepath = '%s/%02d.jpg' % (outdir, ind_img + nimg + 3)
        bpy.ops.render.render(write_still=True)

# remove the texture node in plane
for ind_link in range(0, len(plane_links)):
    if plane_links[ind_link].from_node.name == "Image Texture":
        plane_links.remove(plane_links[ind_link])

# set the calibration plane and projector invisible
bpy.data.objects['Plane'].hide_render = True
bpy.data.objects['Lamp'].hide_render = False
bpy.data.objects['Sphere'].hide_render = False