import socket

def connectToRasp():
    host = 'circuitpython.local'  # as both code is running on same pc
    port = 5000  # socket server port number
    #ipv4_address = socket.gethostbyname(host)
    client_socket = socket.socket()  # instantiate
    client_socket.connect(("192.168.1.106", port))  # connect to the server
    return client_socket

"""message = input(" -> ")  # take input

while message.lower().strip() != 'bye':
    client_socket.send(message.encode())  # send message
    #data = client_socket.recv(1024).decode()  # receive response

    #print('Received from server: ' + data)  # show in terminal

    message = input(" -> ")  # again take input

client_socket.close()  # close the connection8"""