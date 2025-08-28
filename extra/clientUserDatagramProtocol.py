import socket
import sys


if not len(sys.argv) == 1 and sys.argv[1] == "ss":
    request = "screen:1280"
elif not len(sys.argv) == 1 and sys.argv[1] == "q": 
    request = "quit"
else:
    request = "Hello UDP Server!"


bytesToSend = str.encode(request)

serverAddress = ("127.0.0.1", 8080)
bufferSize = 1024


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPClientSocket:
    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddress)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)

    msg = "Message from Server {}".format(msgFromServer[0])

    print(msg)


quit()

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddress)

msgFromServer = UDPClientSocket.recvfrom(bufferSize)

msg = "Message from Server {}".format(msgFromServer[0])

print(msg)
