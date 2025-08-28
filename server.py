import configparser
import threading
import datetime
import socket
import time


config = configparser.ConfigParser()
config.read("settings.ini")

def initGame():
    global GAME_SEED, GAME_STARTED, GAME_START_TIME, RESET_QUEUED, GAME_ID, gameLog  # , addressNametagDict
    print("[$] Game initializing!")

    GAME_SEED = time.time()
    GAME_STARTED = False
    GAME_START_TIME = None

    RESET_QUEUED = False
    GAME_ID += 1
    gameLog = []
    
    if debug:
        print(f"[:]  - Game seed: {GAME_SEED}")

    print("[$] Game initialized!")

def getSettings(getInitString=False):
    global INIT_STRING, LOCAL_PORT, BUFFER_SIZE, GAME_ID

    if getInitString:
        INIT_STRING = f"{INIT_STRING[:INIT_STRING.rfind(':')]}:{GAME_START_TIME}"
        return

    print(f"{lineSeparator}[$] Fetching game settings...")

    SEED = GAME_SEED
    SIZE_X = config.getint("Game", "gridSizeX")
    SIZE_Y = config.getint("Game", "gridSizeY")
    MINE_PERCENTAGE = config.getfloat("Game", "minePercentage")

    INIT_STRING = f"{SEED}:{SIZE_X}:{SIZE_Y}:{MINE_PERCENTAGE}:{GAME_ID}:{GAME_START_TIME}"

    LOCAL_PORT = config.getint("Server", "localPort")
    BUFFER_SIZE = config.getint("Server", "bufferSize")

    if debug:
        print(f"[:]  - Seed: {SEED}")
        print(f"[:]  - Grid X: {SIZE_X}")
        print(f"[:]  - Grid Y: {SIZE_Y}")
        print(f"[:]  - Minepercent: {MINE_PERCENTAGE}% ({MINE_PERCENTAGE})")

        print(f"[:]  - Initialization String: {INIT_STRING}")

        print(f"[:]  - Local Port: {LOCAL_PORT}")
        print(f"[:]  - Buffer Size: {BUFFER_SIZE}")

    print(f"[$] Game settings fetched!\n{lineSeparator[:-1]}")

def setupServer():
    global serverSocket, serverOnline

    print("[$] Launching server...")

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind(("0.0.0.0", LOCAL_PORT))
    serverSocket.settimeout(10.0)

    serverOnline = True

    print("[$] Server online!")

def parseRequests():
    global addressNametagDict, serverOnline, gameLog, GAME_STARTED, GAME_START_TIME, RESET_QUEUED

    print(f"{lineSeparator}[$] Waiting for connections...")

    while serverOnline:
        try:
            request, address = serverSocket.recvfrom(BUFFER_SIZE)
        except TimeoutError:
            if len(addressNametagDict) == 0:
                serverOnline = False

                print("[!] Server closing!")

                serverSocket.close()

                print("[!] Server successfully closed!")
                print("[-] See you later! o/")
                
                break

            continue
        except ConnectionResetError:
            continue

        if b"disconnect" in request:
            try:
                addressNametagDict.pop(address)
            except KeyError:
                pass
            
            sendCallback(b"close", address)            
            
            print(f"[$] Player disconnected: {request.split(b':')[1].decode('utf-8')} {address}")
            
            if len(addressNametagDict) == 0:
                
                print(f"{lineSeparator}[!] No players connected! Server closing in 10 seconds...")
        elif b"connect" in request and address not in addressNametagDict:
            # // print(addressNametagDict)
            # // print(request)

            addressNametagDict[address] = request.split(b':')[1].decode('utf-8')

            threading.Thread(target=loadGame, args=(address,)).start()

            print(f"[$] Player joined: {request.split(b':')[1].decode('utf-8')} {address}")
        elif b"%" in request:
            sendMulticast(request, list(set(addressNametagDict.keys()) - set([address])))
            if request[1] == 37:  # Ascii for "%"
                gameLog.append(request)
                if not GAME_STARTED and request[0] == 48:
                    GAME_START_TIME = str(datetime.datetime.now()).replace(":", ".")
                    GAME_STARTED = True
        elif b"reset" in request:  # int(request.split(b":")[1].decode("utf-8")) > GAME_ID
            print(f"[:] Reset request by: {addressNametagDict[address]} {address}")
            
            # ? [0]
            if not RESET_QUEUED and int(request.split(b":")[1].decode("utf-8")) == GAME_ID:
                RESET_QUEUED = True

                print(f"{lineSeparator}[!] Server resetting...\n{lineSeparator[:-1]}")
                
                # ? [1]
                # Server Reset
                initGame()
                getSettings()

                print(f"[!] Server successfully reset!\n{lineSeparator[:-1]}")

            # ? [2]
            threading.Thread(target=loadGame, args=(address, True)).start()
        else:
            print(f"[!] Unknown request: {request.decode('utf-8')}")

def loadGame(address, reset=False):
    getSettings(getInitString=True)
    
    if reset:
        sendCallback(f"reset&{INIT_STRING}".encode("utf-8"), address)
    else:
        sendCallback(INIT_STRING.encode("utf-8"), address)

    for i in gameLog:
        sendCallback(i, address)

def sendCallback(binaryData, address):
    serverSocket.sendto(binaryData, address)

def sendMulticast(binaryData, connectionList):
    for address in connectionList:
        serverSocket.sendto(binaryData, address)

if __name__ == "__main__":
    debug = config.getboolean("Server", "launchInDebugMode")
    lineSeparator = "[ ]\n"

    GAME_ID = -1
    addressNametagDict = {}

    initGame()
    getSettings()
    setupServer()

    parseRequests()
