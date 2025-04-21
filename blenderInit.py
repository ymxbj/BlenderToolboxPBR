import bpy

def blenderInit(resolution_x, resolution_y, numSamples = 128, exposure = 1.5, transparent = True, use_GPU = True, resolution_percentage = 100):
	# clear all
	bpy.ops.wm.read_homefile()
	bpy.ops.object.select_all(action = 'SELECT')
	bpy.ops.object.delete() 
	# use cycle
	bpy.context.scene.render.engine = 'CYCLES'
	bpy.context.scene.render.resolution_x = resolution_x 
	bpy.context.scene.render.resolution_y = resolution_y 
	bpy.context.scene.render.film_transparent = transparent
	bpy.context.scene.cycles.samples = numSamples 
	bpy.context.scene.cycles.max_bounces = 6
	bpy.context.scene.cycles.film_exposure = exposure
	bpy.context.scene.render.resolution_percentage = resolution_percentage

	# Denoising
	bpy.data.scenes[0].view_layers[0]['cycles']['use_denoising'] = 0

	# set devices
	cyclePref  = bpy.context.preferences.addons['cycles'].preferences
	for dev in cyclePref.devices:
		print("using rendering device", dev.name, ":", dev.use)
	if use_GPU:
		bpy.context.scene.cycles.device = "GPU"
	else:
		bpy.context.scene.cycles.device = "CPU"
	print("cycles rendering with:", bpy.context.scene.cycles.device)
	return 0