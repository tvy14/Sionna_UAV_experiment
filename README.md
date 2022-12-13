# UAV_experiment


## iperf3 網速測試
* Server 
```
iperf3 -s --logfile log.txt -i 0.1 --timestamps
```
* Client
```
iperf3 -c client_ip -t 5 
```
