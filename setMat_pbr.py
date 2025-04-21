import bpy
import os

def setMat_pbr(mesh, texturePath, mr_path, hdri_path, meshColor, alpha= 1.0, colorspace_settting='sRGB'):
    mat = bpy.data.materials.new('MeshMaterial')
    mesh.data.materials.append(mat)
    mesh.active_material = mat
    mat.use_nodes = True
    tree = mat.node_tree

    # set principled BSDF
    PRI = tree.nodes["Principled BSDF"]
    PRI.inputs['Roughness'].default_value = 1.0
    PRI.inputs['Sheen Tint'].default_value = [0, 0, 0, 1]
    PRI.inputs['Alpha'].default_value = alpha

    TI = tree.nodes.new('ShaderNodeTexImage')
    absTexturePath = os.path.abspath(texturePath)
    TI.image = bpy.data.images.load(absTexturePath)
    TI.image.colorspace_settings.name = colorspace_settting

    tree.links.new(TI.outputs['Color'], PRI.inputs['Base Color'])

    MR = tree.nodes.new('ShaderNodeTexImage')
    absMRPath = os.path.abspath(mr_path)
    MR.image = bpy.data.images.load(absMRPath)
    TI.image.colorspace_settings.name = colorspace_settting

    SEP = tree.nodes.new('ShaderNodeSeparateColor')

    tree.links.new(MR.outputs['Color'], SEP.inputs['Color'])
    tree.links.new(SEP.outputs['Blue'], PRI.inputs['Metallic'])
    tree.links.new(SEP.outputs['Green'], PRI.inputs['Roughness'])

    bpy.context.scene.world.use_nodes = True

    world_nodes = bpy.context.scene.world.node_tree.nodes
    world_links = bpy.context.scene.world.node_tree.links
    world_nodes.clear()

    node_world_output = world_nodes.new(type='ShaderNodeOutputWorld')
    node_background = world_nodes.new(type='ShaderNodeBackground')
    node_hdri = world_nodes.new('ShaderNodeTexEnvironment')
    node_hdri.image = bpy.data.images.load(hdri_path)

    world_links.new(node_hdri.outputs["Color"], node_background.inputs["Color"])
    world_links.new(node_background.outputs["Background"], node_world_output.inputs["Surface"])
