import numpy as np
import cv2
import time


cap = cv2.VideoCapture("udp://127.0.0.1:6000")
#cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
#cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("width:{}, height:{} ".format(width,height))
count=0
while(True):
  ret, frame = cap.read()
  if ret:
    count+=1
    #frame_display=cv2.resize(frame, (960,540))
    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('s'):
      cv2.imwrite("png_save/frame{}.png".format(count), frame)
      print("save frame{}.png".format(count))
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
cap.release()
cv2.destroyAllWindows()
