import bpy
import colorsys
import os


def make_image_node(texAct, bsdf, input, mode):
    A = mat.node_tree.nodes.new(type="ShaderNodeTexImage")
    A.image = bpy.data.images.load(texAct)
    A.image.colorspace_settings.name = mode
    mat.node_tree.links.new(bsdf.inputs[input], A.outputs['Color'])



############### Texture directory and prefix 
dir = bpy.path.abspath('//') + "directory_name"
prefix = "texture_name_prefix"


###############
listTex = os.listdir(dir)
list_obj = []
for elem in listTex:
    red = elem.split(prefix)[1]
    texType = red.split('_')[-1]
    objName = red.split('_'+texType)[0]
    list_obj.append(objName)

list_obj = list(set(list_obj))


for object in list_obj:
    current = bpy.context.scene.objects[object]
    mat = bpy.data.materials[object]
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    
    BC = dir+'\\'+prefix+object+'_BaseColor.png'
    METAL = dir+'\\'+prefix+object+'_Metallic.png'
    NORMAL = dir+'\\'+prefix+object+'_Normal.png'
    ROUGH = dir+'\\'+prefix+object+'_Roughness.png'

    make_image_node(BC, bsdf, 'Base Color', 'sRGB')
    make_image_node(METAL, bsdf, 'Metallic', 'Non-Color')
    make_image_node(NORMAL, mat.node_tree.nodes["Normal Map"], 'Color', 'Non-Color')
    make_image_node(ROUGH, bsdf, 'Roughness', 'Non-Color')
    