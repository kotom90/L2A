# Replace 'COM3' with your actual COM port
ser = serial.Serial('COM3', baudrate=115200, timeout=1)

try:
    while True:
        # Send data to the Pico
        message = input("Enter a message to send: ")
        ser.write(message.encode('utf-8'))

        # Read data from the Pico
        received_data = ser.readline().decode('utf-8').strip()
        print(f"Received: {received_data}")

except KeyboardInterrupt:
    print("Communication terminated by the user.")
finally:
    ser.close()