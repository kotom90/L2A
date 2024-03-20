import serial
import time
from keycode import Keycode

# Replace "COM6" with the correct serial port on your computer
uart = serial.Serial("COM7", baudrate=9600)

try:
    while True:
        # Send data
        #uart.write(Keycode.F1)
        #text = input("write here: ")
        uart.write(bytes([Keycode.A]))
        uart.flush()
        # Read data
        #received_data = uart.readline()
        print("sent")
        #print("Received:", received_data.decode("utf-8"))

        # Wait for a moment
        time.sleep(1)

except KeyboardInterrupt:
    # Do any cleanup needed on program exit
    uart.close()