import time
from machine import Pin
import network
import socket

# WiFi initial configuration
ssid = "Your WiFi network name" 
password = "Your Wifi network password"
wlan = network.WLAN(network.STA_IF)

# Establish connection via WLAN
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connection
while wlan.isconnected() == False: 
    pass

print('WiFi connection on %s established. Device network information: ' % ssid)
print(wlan.ifconfig())

actuator = Pin(2, Pin.OUT)

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind(('', 80))
tcp_socket.listen(3)

while True:
    conn, addr = tcp_socket.accept()
    print('New connection at:  %s' % str(addr))
    request = conn.recv(1024)
    print('Request = %s' % str(request))

    # GET request from server
    request = str(request)

    # request.find == 6 since information is the 6th value on request
    if request.find('/actuator=on') == 6:
        print('Actuator ON')
        actuator.value(1)
    if request.find('/actuator=off') == 6:
        print('Actuator OFF')
        actuator.value(0)
    response = "OK"
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: closed\n\n')
    conn.sendall(response)
    conn.close()

