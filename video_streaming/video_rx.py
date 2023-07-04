import socket
import cv2
import numpy
import zlib
import json
from datetime import datetime
import ntplib
import time

try:
    print("time sync...")
    # Create an NTP client
    ntp_client = ntplib.NTPClient()

    # Connect to the NTP server on Device 1's IP address
    response = ntp_client.request('192.168.50.152', version=3)

    # Calculate the round-trip time (latency)
    round_trip_time =  response.orig_time - response.tx_time

    # Client local time -> orig_time t1
    # NTP server receives at the server time ->recv_time t2
    # NTP server replies at server time -> tx_time t3
    # Client receives that reply at local time -> dest_time t4
    t1=response.orig_time
    t2=response.recv_time
    t3=response.tx_time
    t4=response.dest_time
    sync_time=t3+(t4-t3+t2-t1)/2
    start_time=time.time()


    print("sync finished")
except:
    print("no ntp server, shut down")









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
    #length = recvall(conn,16)
    #length=length.decode('utf-8')
    json_msg=recvall(conn,200)
    json_msg=json_msg.decode('utf-8')
    json_msg=json.loads(json_msg)
    print(json_msg)
    latency=sync_time+time.time()-start_time-json_msg["time"]
    print("latency={:.3f}s".format(latency))
    #print(type(json_msg["size"]))
    #stringData = recvall(conn, int(length))
    stringData = recvall(conn, json_msg["size"])
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


