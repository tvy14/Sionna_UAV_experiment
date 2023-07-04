import socket
import cv2
import numpy
import zlib
from datetime import datetime
def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

save_video=False
TCP_IP = "192.168.50.36"
TCP_PORT = 8002
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((TCP_IP, TCP_PORT))
s.listen(True)
conn, addr = s.accept()
count=0
fourcc = cv2.VideoWriter_fourcc(*'MPEG')

now = datetime.now()
video_name="output_{}_{}_{}_{}_{}.mp4".format(now.month, now.day, now.hour, now.minute, now.second)
if save_video:
    out = cv2.VideoWriter(video_name, fourcc, 30.0, (640, 480))
while 1:
    count+=1
    length = recvall(conn,16)
    length=length.decode('utf-8')
    stringData = recvall(conn, int(length))
    #stringData = zlib.decompress(stringData)
    #print('old={} new={}'.format(len(stringData), len(zlib.compress(stringData)) ))
    data = numpy.fromstring(stringData, dtype='uint8')
    decimg=cv2.imdecode(data,1)
    #decimg = cv2.resize(decimg, (1600, 1200))
    if save_video:
        out.write(decimg)
    cv2.imshow('SERVER',decimg)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('c'):
        now = datetime.now()
        cv2.imwrite("output_{}_{}_{}_{}_{}.jpg".format(now.month, now.day, now.hour, now.minute, now.second), decimg)
        print("save img: output_{}_{}_{}_{}_{}.jpg".format(now.month, now.day, now.hour, now.minute, now.second))

if save_video:
    out.release()
s.close()
cv2.destroyAllWindows()


