import cv2
import time
import os
from datetime import datetime
cap=cv2.VideoCapture("udp://127.0.0.1:6000")
ret, frame=cap.read()

now=datetime.now()
file_name="output_{}_{}_{}_{}_{}.mp4".format(now.month, now.day, now.hour, now.minute, now.second)
txt_name="output_{}_{}_{}_{}_{}.txt".format(now.month, now.day, now.hour, now.minute, now.second)
print("{}".format(file_name))

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps=30
size=(width, height)
print("w: {}, h: {}, fps: {}".format(width, height, fps))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(filename=file_name, apiPreference=cv2.CAP_ANY, fourcc=fourcc, fps=fps, frameSize=size)
start_time=time.time()

while True:
    ret, frame=cap.read()
    if ret:
        with open(txt_name,"a+") as f:
            now=datetime.now()
            f.write("{}\n".format(str(now)))
            out.write(frame)
        cv2.namedWindow("webcam", cv2.WINDOW_NORMAL)
        cv2.imshow("webcam",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
out.release()
cv2.destroyAllWindows()
