import time
import os
import datetime 
import subprocess
import csv

folder_exist=os.path.isdir("data")
if not folder_exist:
    print("forder \"data\" is not exist, create \"data\"......")
    os.mkdir("data")
    print("finished")
print("start to record Wi-Fi info")
nowTime = datetime.datetime.now() 
filename="data/RSSI_record_{}_{}_{}_{}_{}_{}.csv".format(nowTime.year, nowTime.month, nowTime.day, nowTime.hour , nowTime.minute, nowTime.second)

with open(filename, 'a+', newline='') as csvfile:
    print("filepath:",filename)
    # 以空白分隔欄位，建立 CSV 檔寫入器
    writer = csv.writer(csvfile, delimiter=' ')
    writer.writerow(['time', "band", "RSSI", "max_rx_rate"])
    while True:
        s = subprocess.getstatusoutput("iw wlp3s0 link")
        current_time=str(datetime.datetime.now() )
        data_split=s[1].split("\n")
        band=data_split[2].split()[1]
        rssi=data_split[5].split()[1]
        #print(rssi)
        max_rx_rate=data_split[6].split()[2]
        writer.writerow([current_time, band, rssi, max_rx_rate])
        time.sleep(0.1)
