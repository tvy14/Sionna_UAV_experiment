import cv2
import os

def images_to_video(image_path_list, video_path, fps=30):

    frame = cv2.imread(image_path_list[0])
    height, width, layers = frame.shape


    video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    for img_path in image_path_list:
        video.write(cv2.imread(img_path))

    cv2.destroyAllWindows()
    video.release()

#input image path
image_paths = []
for i in range(0, 30):
    image_paths.append("image/scene{0:03d}.png".format(i))

# output video path
video_path = "output.mp4"

images_to_video(image_paths, video_path)
