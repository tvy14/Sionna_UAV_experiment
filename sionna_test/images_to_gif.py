from PIL import Image
import imageio
def create_gif(image_path_list, gif_path, duration=3):
    images = []
    
    for path in image_path_list:
        img = Image.open(path)
        images.append(img)
    
    # save images to gif
    imageio.mimsave(gif_path, images,'GIF',duration=duration)

#input image path
image_paths = []
for i in range(0, 30):
    image_paths.append("image/scene{0:03d}.png".format(i))




#output gif path
gif_path = "output.gif" 

create_gif(image_paths, gif_path)