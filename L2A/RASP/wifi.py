import os
import ipaddress
import wifi
import socketpool

import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

HOST = ""
PORT = 5000
TIMEOUT = None
MAXBUF = 256
buffer = bytearray(MAXBUF)

print()
print("Connecting to WiFi")

#  connect to your SSID
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

#wifi.radio.hostname = "palatut"
# Use the hostname to access your device on the network
print("My hostname is", wifi.radio.hostname)

"""print(tuple(map(int, os.getenv('IP_ADDRESS').split('.'))))

ipv4_address = tuple(map(int, os.getenv('IP_ADDRESS').split('.')))
ipv4_gateway = tuple(map(int, os.getenv('GATEWAY').split('.')))
ipv4_subnet = tuple(map(int, os.getenv('SUBNET_MASK').split('.')))
ipv4_dns = tuple(map(int, os.getenv('DNS_SERVER').split('.')))
wifi.radio.create_ap(ipv4_address, ipv4_gateway, ipv4_subnet, ipv4_dns)"""


print("Connected to WiFi")
pool = socketpool.SocketPool(wifi.radio)
s = pool.socket(pool.AF_INET,pool.SOCK_STREAM)

#  prints MAC address to REPL
print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

#  prints IP address to REPL
print("My IP address is", wifi.radio.ipv4_address)

#  pings Google
#ipv4 = ipaddress.ip_address("8.8.4.4")
#print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4)*1000))

#s.settimeout(TIMEOUT)

s.bind((HOST, PORT))
s.listen(5)
print("Listening")

print("Accepting connections")
conn, addr = s.accept()
    
#conn.settimeout(TIMEOUT)
print("Accepted from", addr)

while True:
    buf = conn.recv_into(buffer,MAXBUF)
    #print("Received", buffer.decode('utf-8'), "from", addr)
    #time.sleep(1)
    #text = buffer.decode('utf-8')
    time.sleep(0.01)  # Sleep for a bit to avoid a race condition on some systems
    keyboard = Keyboard(usb_hid.devices)
    keyboard.press(buffer[0])
    time.sleep(0.01)
    keyboard.release_all() 

    #print('NEXT KEY')
    #clear buffer
    #buffer = bytearray(MAXBUF)
    buffer[0] = 0
    #size = conn.sendall(buf)
    #print("Sent", buf[:size], size, "bytes to", addr)

    #conn.close()
    #microcontroller.reset()