import ntplib
from time import time, sleep

# Create an NTP client
ntp_client = ntplib.NTPClient()

# Connect to the NTP server on Device 1's IP address
response = ntp_client.request('192.168.50.152', version=3)

# Calculate the round-trip time (latency)
round_trip_time =  response.orig_time - response.tx_time
while True:
    response = ntp_client.request('192.168.50.152', version=3)
    print(response.tx_time,response.dest_time ,response.offset)
    #print(response.tx_time)
    sleep(1)
    

#print("Round-Trip Time (Latency): {:.3f} seconds".format(round_trip_time))
