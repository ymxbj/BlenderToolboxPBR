import blendertoolbox as bt
import bpy
import os
from mathutils import Vector
from blenderInit import blenderInit
from setMat_pbr import setMat_pbr
cwd = os.getcwd()

gpu_id = 0
os.environ["CUDA_VISIBLE_DEVICES"] = f"{gpu_id}"

bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'
bpy.context.preferences.addons["cycles"].preferences.get_devices()
print(bpy.context.preferences.addons["cycles"].preferences.compute_device_type)
for d in bpy.context.preferences.addons["cycles"].preferences.devices:
    d["use"] = 1 # Using all devices, include GPU and CPU
    print(d["name"], d["use"])
bpy.context.preferences.addons["cycles"].preferences.compute_device_type = 'CUDA'
device_type = bpy.context.preferences.addons['cycles'].preferences.compute_device_type

## initialize blender
imgRes_x = 1080
imgRes_y = 1080
numSamples = 200
exposure = 1.5

mesh_dir = './telescope'
output_dir = mesh_dir
meshPath = os.path.join(mesh_dir, 'mesh.obj')
outputPath = os.path.join(output_dir, 'pbr.png')

# # set material (TODO: this has some new issue due to new version of Blender)
# colorObj(RGBA, H, S, V, Bright, Contrast)
useless = (0,0,0,1)
meshColor = bt.colorObj(useless, 0.5, 1.0, 1.0, 0.2, 0.5)

albedo_Path = os.path.join(mesh_dir, 'mesh_albedo.png')
mr_Path = os.path.join(mesh_dir, 'mesh_mr.png')
hdri_Path = './Env/rogland_sunset_4k.exr'

blenderInit(imgRes_x, imgRes_y, numSamples, exposure, transparent = True)
## read mesh (choose either readPLY or readOBJ)

location = (0, 0, 0.5) 
rotation = (90, 0, -90)
scale = (0.5, 0.5, 0.5) 
mesh = bt.readMesh(meshPath, location, rotation, scale)

setMat_pbr(mesh, albedo_Path, mr_Path, hdri_Path, meshColor)

## set camera (recommend to change mesh instead of camera, unless you want to adjust the Elevation)
camLocation =  (3, 0, 2)
lookAtLocation = (0, 0, 0.5)
focalLength = 90 # (UI: click camera > Object Data > Focal Length)
cam = bt.setCamera(camLocation, lookAtLocation, focalLength)

## set gray shadow to completely white with a threshold
bt.shadowThreshold(alphaThreshold = 0.05, interpolationMode = 'CARDINAL')

## save rendering
bt.renderImage(outputPath, cam)
