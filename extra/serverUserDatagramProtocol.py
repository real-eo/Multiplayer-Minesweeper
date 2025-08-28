# User Datagram Protocol Server
import threading
import socket


localIP = "127.0.0.1"
localPort = 8080
bufferSize = 1024

msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPServerSocket:
    # Bind to address and port
    UDPServerSocket.bind((localIP, localPort))

    print("[$] UDP server up and listening")

    # Listen for incoming datagrams
    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        clientMsg = "[$] Message from Client: {}".format(message)
        clientAddress  = "[$] Client Address: {}".format(address)
        
        print(clientMsg)
        print(clientAddress)

        # Sending a reply to client
        UDPServerSocket.sendto(bytesToSend, address)

        if message == b"quit":
            print("[$] Quitting!")
            break


quit()


# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and port
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    
    print(clientMsg)
    print(clientIP)

    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address)
