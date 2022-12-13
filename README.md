# UAV_experiment


## iperf3 網速測試
* Server 
```
iperf3 -s
```
* Client (server send UDP to client)
``` 
iperf3 -c 10.42.0.1 -t 100 --logfile log.txt -i 0.1 -R -V --udp --bitrate 0

```
* Client (server send TCP to client)
``` 
iperf3 -c 10.42.0.1 -t 100 --logfile log.txt -i 0.1 -R -V --bitrate 0

```
