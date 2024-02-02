import cv2
import moviepy.editor as mp

def video_to_gif(video_path, gif_path, fps=10):
    clip = mp.VideoFileClip(video_path)
    clip.write_gif(gif_path, fps=fps)

# input video path
video_path = "output.mp4"

# output gif path
gif_path = "output.gif"


video_to_gif(video_path, gif_path)

