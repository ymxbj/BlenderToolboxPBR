import av
import os
from PIL import Image

mesh_dir = './telescope'
input_folder = os.path.join(mesh_dir, 'pbr_images')
output_video = os.path.join(mesh_dir, 'pbr_video.mp4')

image_files = [os.path.join(input_folder, f'{i}.png') for i in range(360)]

fps = 60 
width, height = Image.open(image_files[0]).size 

container = av.open(output_video, mode="w")
stream = container.add_stream("h264", rate=fps)
stream.width = width
stream.height = height
stream.pix_fmt = "yuv420p"

for img_path in image_files:
    print(img_path)
    img = Image.open(img_path).convert("RGB")  
    frame = av.VideoFrame.from_image(img)
    packet = stream.encode(frame)
    if packet:
        container.mux(packet)

packet = stream.encode(None)
if packet:
    container.mux(packet)
container.close()
