import os
from PIL import Image

mesh_path = './telescope'

roughness_path = os.path.join(mesh_path, 'roughness.png')
metallic_path = os.path.join(mesh_path, 'metallic.png')

roughness = Image.open(roughness_path).convert('L')  
metallic = Image.open(metallic_path).convert('L')   

width, height = roughness.size
new_image = Image.new('RGB', (width, height))

for x in range(width):
    for y in range(height):
        g = roughness.getpixel((x, y)) 
        b = metallic.getpixel((x, y))  
        new_image.putpixel((x, y), (255, g, b)) 

# 保存合成的RGB图像
save_path = os.path.join(mesh_path, "mesh_mr.png")
new_image.save(save_path)