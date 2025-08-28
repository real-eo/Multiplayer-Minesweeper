import configparser
import socket
import time


def getCoords(window):
    winCoords = window.controller.geometry().split("+")[1:]

    winCoordX = int(winCoords[0])
    winCoordY = int(winCoords[1])

    return (winCoordX, winCoordY)

def _init_(name):
    global mainSocket, serverAddress, BUFFER_SIZE, NAMETAG

    config = configparser.ConfigParser()
    config.read("settings.ini")

    SERVER_IP = config.get("Client", "serverIp")
    SERVER_PORT = config.getint("Client", "serverPort")
    BUFFER_SIZE = config.getint("Client", "bufferSize")

    NAMETAG = name

    serverAddress = (SERVER_IP, SERVER_PORT)

    mainSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mainSocket.settimeout(5.0)
    
    mainSocket.sendto(f"connect:{name}".encode("utf-8"), serverAddress)
    recievedInitString = mainSocket.recvfrom(BUFFER_SIZE)[0].decode("utf-8")

    print(f"[$] Successfully connected!")
    print(f"[:] InitString: {recievedInitString}")
    
    return recievedInitString.split(":")

def restart(gameID):
    global clientRunning
    
    mainSocket.sendto(f"reset:{gameID}".encode("utf-8"), serverAddress)

def exit(exitCode):
    global mainSocket

    if exitCode == 1:
        mainSocket.sendto(f"disconnect:{NAMETAG}".encode("utf-8"), serverAddress)
        print(f"[!] Attempting to disconnect...")
    elif exitCode == 0:
        mainSocket.close()
        print(f"[!] Connection successfully closed!")

def send(action, tile, name):
    mainSocket.sendto(f"{action}%{tile['coords']}%{name}".encode("utf-8"), serverAddress)

def recieve(window):
    global clientRunning

    clientRunning = True

    while clientRunning:
        try:
            request = mainSocket.recvfrom(BUFFER_SIZE)[0].decode("utf-8")
        except TimeoutError:
            print("[ ] Timeout tick:")
            print(f"[:]  - Clients running: {clientRunning}")
            if clientRunning:
                continue

            break

        if "%" in request:
            action, tileIDString, name = request.split("%")
            
            exec(f"global tileID\ntileID = {tileIDString}")

            if action == "0":
                window.onClick(tileID, player=name, local=False)                    # ? Raises warnings, but it always gets declared right above
            elif action == "1":
                window.onRightClick(tileID, player=name, local=False)               # ? Raises warnings, but it always gets declared right above
            elif "focus" in action:
                window.animationPlayerCursor(tileID, action)                        # ? Raises warnings, but it always gets declared right above
        # * [1] 
        elif "reset" in request:
            # * [2] 
            # (Swapped, was [3])
            recievedInitString = request.split("&")
            print(f"[:] InitString: {recievedInitString}")

            window.updateSettings(initString=recievedInitString[1].split(":"))

            # * [3] 
            # (Swapped, was [2])
            window.restart()
        elif request == "close":
            clientRunning = False
            break
        else:
            print(request)
    
    exit(exitCode=0)
