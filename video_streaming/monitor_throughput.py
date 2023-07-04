import psutil
import time

def get_network_throughput():
    # Get the current network statistics
    net_io = psutil.net_io_counters()
    
    # Retrieve the bytes sent and received
    bytes_sent = net_io.bytes_sent
    bytes_received = net_io.bytes_recv
    
    # Sleep for a short interval
    time.sleep(1)
    
    # Get the network statistics again after a short delay
    net_io = psutil.net_io_counters()
    
    # Calculate the throughput by comparing the new and old values
    new_bytes_sent = net_io.bytes_sent
    new_bytes_received = net_io.bytes_recv
    
    # Calculate the throughput in bytes/sec
    sent_throughput = new_bytes_sent - bytes_sent
    received_throughput = new_bytes_received - bytes_received
    
    # Convert to kilobytes/sec
    sent_throughput /= 1024
    received_throughput /= 1024
    
    return sent_throughput, received_throughput

# Example usage
while True:
    sent_throughput, received_throughput = get_network_throughput()
    print(f"Sent throughput: {sent_throughput:.2f} KB/sec")
    print(f"Received throughput: {received_throughput:.2f} KB/sec")
    #time.sleep(1)
