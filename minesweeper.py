# File: minesweeper.py

from tkinter import messagebox as tkMessageBox
from datetime import time, date, datetime
import libs.themeConfig as themeConfig
from PIL import Image, ImageTk
from collections import deque
from tkinter.font import Font
from libs.animation import *
import libs.color as color
from tkinter import *
import configparser
import connection
import threading
import platform
import ctypes
import random
import time
import sys


STATE_DEFAULT = 0
STATE_CLICKED = 1
STATE_FLAGGED = 2

BTN_CLICK = "<Button-1>"
BTN_FLAG = "<Button-2>" if platform.system() == 'Darwin' else "<Button-3>"

config = configparser.ConfigParser()
config.read("settings.ini")


class Minesweeper(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Game
        self.controller = controller
        self.ID = "Minesweeper"
    
    def initGame(self):
        if self.controller.mode == "multiplayer":
            # Connect Game
            self.connectGame()
        else:
            # Generate new game
            self.updateSettings()
            
        # Import images
        self.generateImages()

        # Color mode
        self.colorModeDict = themeConfig.colorModeDict

        self.config(bg=self.colorModeDict[COLOR_MODE]["color"])

        # Set up frame
        self.frame = Frame(self, bg=self.colorModeDict[COLOR_MODE]["color"])
        self.frame.pack()

        # ! Run loading animation here!

        self.controller.showFrame(self.controller.loadingScreen)
        self.controller.frames[self.controller.loadingScreen].startLoadingAnimation()

        # Set up labels/UI
        DEFAULT_FONT = {'family': 'Segoe UI', 'size': 9, 'weight': 'normal', 'slant': 'roman', 'underline': False, 'overstrike': False}
        fontConfig = [self.colorModeDict[COLOR_MODE]["font"], DEFAULT_FONT]["TkDefaultFont" in self.colorModeDict[COLOR_MODE]["font"]]

        self.font = Font(family=fontConfig["family"], size=fontConfig["size"], weight=fontConfig["weight"], slant=fontConfig["slant"], underline=fontConfig["underline"], overstrike=fontConfig["overstrike"])

        self.labels = {
            "time": Label(self.frame, text="00:00:00", font=self.font, fg=self.colorModeDict[COLOR_MODE]["text"]["game"], bg=self.colorModeDict[COLOR_MODE]["color"]),
            "mines": Label(self.frame, text="Mines: 0", font=self.font, fg=self.colorModeDict[COLOR_MODE]["text"]["game"], bg=self.colorModeDict[COLOR_MODE]["color"]),
            "flags": Label(self.frame, text="Flags: 0", font=self.font, fg=self.colorModeDict[COLOR_MODE]["text"]["game"], bg=self.colorModeDict[COLOR_MODE]["color"])
        }

        self.labels["time"].grid(row=0, column=0, columnspan=SIZE_Y)  # Top full width
        self.labels["mines"].grid(row=SIZE_X + 1, column=0, columnspan=int(SIZE_Y / 2))  # Bottom left
        self.labels["flags"].grid(row=SIZE_X + 1, column=int(SIZE_Y / 2) - 1, columnspan=int(SIZE_Y / 2))  # Bottom right

        # "Click" button keybind
        for keybind in [config.get("Keybinds", "click").lower(), config.get("Keybinds", "click").upper()]:
            try:
                self.controller.bind(f"<{keybind}>", lambda _ : self.onClick(self.cursorLocations[CURSOR_COLOR], NAMETAG, True))
            except TclError:
                continue

        # "Flag" button keybind
        for keybind in [config.get("Keybinds", "flag").lower(), config.get("Keybinds", "flag").upper()]:
            try:
                self.controller.bind(f"<{keybind}>", lambda _ : self.onRightClick(self.cursorLocations[CURSOR_COLOR], NAMETAG, True))
            except TclError:
                continue

        self.restart()  # Start game
        self.updateTimer()  # Init timer

        if self.controller.mode == "multiplayer":
            # Recieve loop
            threading.Thread(target=connection.recieve, args=(self,)).start()

    def setup(self):
        # Create flag and clicked tile variables
        self.flagCount = 0
        self.correctFlagCount = 0
        self.clickedCount = 0
        self.startTime = GAME_START_TIME
        self.pauseTime = None
        self.paused = False
        self.loading = True
        self.cursorLocations = {}

        # Create buttons
        self.tiles = dict({})
        self.mines = 0

        random.seed(SEED)

        for x in range(0, SIZE_X):
            for y in range(0, SIZE_Y):
                if y == 0:
                    self.tiles[x] = {}

                id = str(x) + "_" + str(y)
                isMine = False

                # Tile image changeable for debug reasons:
                gfx = self.images["plain"]()

                # Currently random amount of mines
                if random.uniform(0.0, 100.0) < MINE_PERCENTAGE:
                    isMine = True
                    self.mines += 1

                tile = {
                    "id": id,
                    "isMine": isMine,
                    "state": STATE_DEFAULT,
                    "coords": {
                        "x": x,
                        "y": y
                    },
                    "button": Button(self.frame, image=gfx, bg=self.colorModeDict[COLOR_MODE]["field"], activebackground=self.colorModeDict[COLOR_MODE]["field"], relief=[SUNKEN, RAISED][ANIMATE_BUTTONS], borderwidth=self.colorModeDict[COLOR_MODE]["border"]*2),
                    "mines": 0  # Calculated after grid is built
                }

                tile["button"].bind(BTN_CLICK, self.onClickWrapper(x, y, True))
                tile["button"].bind(BTN_FLAG, self.onRightClickWrapper(x, y, True))

                tile["button"].bind("<Enter>", self.animationFocusWrapper(x, y))
                tile["button"].bind("<Leave>", self.animationDefocusWrapper(x, y))

                tile["button"].grid(row=x+1, column=y)  # Offset by 1 row for timer

                self.tiles[x][y] = tile
                # // mineIndex += 1

        self.loading = False
        self.windowedScreenSize = (self.controller.winfo_width(), self.controller.winfo_height())
        # // self.calculateMines()

    def generateImages(self):
        # // self.pyimageMap = {}

        imageOrder = ["plain", "clicked", "mine", "flag", "wrong"] + [str(i) for i in range(1, 9)]

        self.normalImageList = [PhotoImage(file=f"images/{COLOR_MODE}/tile_{tile}.png") for tile in imageOrder]

        # // for index, image in enumerate(self.normalImageList):
            # // self.pyimageMap[str(image)] = imageOrder[index]

        self.scaledImageList = []
    
        # * This would be cool, but haven't found a solution to make this work yet
        # // gridPixelX = 1500
        # // gridPixelY = 1000

        # // fieldSizeW = (gridPixelX/max(SIZE_Y/SIZE_X, 1))
        # // fieldSizeH = (gridPixelY/max(SIZE_X/SIZE_Y, 1))

        gridPixelSize = 1000-(SIZE_X+SIZE_Y)

        fieldSizeW = (gridPixelSize/max(SIZE_Y/SIZE_X, 1))
        fieldSizeH = (gridPixelSize/max(SIZE_X/SIZE_Y, 1))

        rescaleSize = ((fieldSizeW/SIZE_X) + (fieldSizeH/SIZE_Y)) / 2

        print(f"[$] Rescale size: {rescaleSize} {(fieldSizeW/SIZE_X, fieldSizeH/SIZE_Y)}")

        for index, image in enumerate(self.normalImageList):
            PILImage = ImageTk.getimage(image).resize((int(rescaleSize), int(rescaleSize)), 0)
            scaledImage = ImageTk.PhotoImage(PILImage)

            # // self.pyimageMap[str(image)] = imageOrder[index]
            self.scaledImageList.append(scaledImage)

        # // print(self.normalPyimageMap, self.scaledPyimageMap)

        self.images = {
            "plain": lambda debug=None: [self.normalImageList[0], self.scaledImageList[0]][self.controller.attributes("-fullscreen")], 
            "clicked": lambda debug=None: [self.normalImageList[1], self.scaledImageList[1]][self.controller.attributes("-fullscreen")],
            "mine": lambda debug=None: [self.normalImageList[2], self.scaledImageList[2]][self.controller.attributes("-fullscreen")],
            "flag": lambda debug=None: [self.normalImageList[3], self.scaledImageList[3]][self.controller.attributes("-fullscreen")],
            "wrong": lambda debug=None: [self.normalImageList[4], self.scaledImageList[4]][self.controller.attributes("-fullscreen")],
            "numbers": lambda mines: [self.normalImageList[4+mines], self.scaledImageList[4+mines]][self.controller.attributes("-fullscreen")]
        }   

    def calculateMines(self):
        # Loop again to find nearby mines and display number on tile
        for x in range(0, SIZE_X):
            for y in range(0, SIZE_Y):
                mc = 0
                for n in self.getNeighbors(x, y):
                    mc += 1 if n["isMine"] else 0
                self.tiles[x][y]["mines"] = mc

    def connectGame(self):
        global NAMETAG

        NAMETAG = config.get("Settings", "name")[:32]
        
        recievedInitString = connection._init_(name=NAMETAG)
        self.updateSettings(initString=recievedInitString)

    def updateSettings(self, initString=""):
        # * [2] 
        # (Swapped, was [3])
        global SEED, SIZE_X, SIZE_Y, MINE_PERCENTAGE, GAME_ID, GAME_START_TIME, COLOR_MODE, CURSOR_COLOR, HIGHLIGHT_SQUARES_LOCALLY, ANIMATE_BUTTONS

        COLOR_MODE = config.get("Settings", "theme").lower()
        CURSOR_COLOR = config.get("Settings", "cursorColor")

        if not "#" in CURSOR_COLOR:
            H = random.SystemRandom().randint(0, 360)  # Hue
            S = random.SystemRandom().uniform(0.5, 1)  # Saturation
            V = random.SystemRandom().uniform(0.85, 1)  # Value
            
            CURSOR_COLOR = color.HSVtoHex(H, S, V)
        
        HIGHLIGHT_SQUARES_LOCALLY = config.getboolean("Settings", "displayCursorLocally")
        ANIMATE_BUTTONS = config.getboolean("Settings", "animateButtons")
        
        # Multiplayer
        if self.controller.mode == "multiplayer":
            SEED = float(initString[0])
            SIZE_X = int(initString[2])  # Swap "SIZE_X" & "SIZE_Y" to generate the board with correct dimensions 
            SIZE_Y = int(initString[1])  # Needed because board generation axies are reversed; {x: 3, y: 2} -> {x: 2, y: 3}
            MINE_PERCENTAGE = float(initString[3])
            GAME_ID = int(initString[4])

            try:
                GAME_START_TIME = datetime.strptime(initString[-1], '%Y-%m-%d %H.%M.%S.%f') if not initString[-1][0] == "N" else None
            except ValueError:
                print(f"[!] {initString}")
                quit()
        # Singleplayer
        elif self.controller.mode == "singleplayer":
            global NAMETAG

            NAMETAG = config.get("Settings", "name")[:32]

            SEED = time.time()
            SIZE_X = config.getint("Game", "gridSizeY")  # Swap "SIZE_X" & "SIZE_Y" to generate the board with correct dimensions 
            SIZE_Y = config.getint("Game", "gridSizeX")  # Needed because board generation axies are reversed; {x: 3, y: 2} -> {x: 2, y: 3}
            MINE_PERCENTAGE = config.getfloat("Game", "minePercentage")
            GAME_ID = 0

            GAME_START_TIME = datetime.now()

    def restart(self):
        # * [3] 
        # (Swapped, was [2])
        self.setup()
        self.refreshLabels()

        # * [4]
        self.controller.attributes("-disabled", False)
        # ! Stop loading animation here:
        self.controller.showFrame(self.controller.minesweeper)
        self.controller.frames[self.controller.loadingScreen].stopLoadingAnimation()

    def startAnimation(self, animation, screen):
        screen.place()
        animation.start()
        screen.lift()
    
    def stopAnimation(self, animation, screen):
        animation.stop()
        animation.reset()
        animation.hide()
        
        screen.lower()
        screen.place_forget()
        
    def refreshLabels(self):
        self.labels["flags"].config(text = "Flags: " + str(self.flagCount))
        self.labels["mines"].config(text = "Mines: " + str(self.mines))

    def killButtons(self):
        for x in range(0, SIZE_X):
            for y in range(0, SIZE_Y):
                self.tiles[x][y]["button"].destroy()

    def gameOver(self, won, player=""):
        for x in range(0, SIZE_X):
            for y in range(0, SIZE_Y):
                if self.tiles[x][y]["isMine"] == False and self.tiles[x][y]["state"] == STATE_FLAGGED:
                    self.tiles[x][y]["button"].config(image = self.images["wrong"](), bg="#ff8888")
                if self.tiles[x][y]["isMine"] == True and self.tiles[x][y]["state"] != STATE_FLAGGED:
                    self.tiles[x][y]["button"].config(image = self.images["mine"]())

        self.pauseTimer()

        self.controller.update()

        msg = "You Win! Play again?" if won else f"\"{player}\" lost the game! Play again?"
        res = tkMessageBox.askyesno("Game Over", msg)
        if res:
            self.controller.attributes("-disabled", True)

            # ! Run loading screen animation here

            self.controller.showFrame(self.controller.loadingScreen)
            self.controller.frames[self.controller.loadingScreen].startLoadingAnimation()

            self.labels["time"].config(text="00:00:00")  # Reset the timer

            self.loading = True
            self.killButtons()
            
            if self.controller.mode == "multiplayer":
                # * [0]
                connection.restart(gameID=GAME_ID)
            else:
                self.updateSettings()
                self.restart()
        else:
            self.tk.quit()

    def windowChanged(self):
        for x in range(0, SIZE_X):
            for y in range(0, SIZE_Y):
                tile = self.tiles[x][y]
                if tile["state"] == STATE_CLICKED:
                    if tile["isMine"] == True:
                        imageID = "mine"
                    elif tile["mines"] > 0:
                        imageID = "numbers"
                    else:
                        imageID = "clicked"
                elif tile["state"] == STATE_FLAGGED:
                    imageID = "flag"
                else:
                    imageID = "plain"
                    
                # // imageID = self.pyimageMap[tile["button"].cget('image')]

                tile["button"].configure(image=self.images[[imageID, "numbers"][imageID.isnumeric()]](tile["mines"]))
        
    def updateTimer(self):
        ts = "00:00:00"
        if self.startTime != None and not self.paused:
            delta = datetime.now() - self.startTime
            ts = str(delta).split('.')[0]  # Drop ms
            if delta.total_seconds() < 36000:
                ts = "0" + ts  # Zero-pad

            self.labels["time"].config(text=ts)
        self.frame.after(100, self.updateTimer)

    def pauseTimer(self):
        if self.paused:
            delta = datetime.now() - self.pauseTime
            self.startTime += delta
            self.paused = False
        elif not self.paused:
            self.pauseTime = datetime.now()
            self.paused = True

    def getNeighbors(self, x, y):
        neighbors = []
        coords = [
            {"x": x-1,  "y": y-1},  # Top right
            {"x": x-1,  "y": y},    # Top middle
            {"x": x-1,  "y": y+1},  # Top left
            {"x": x,    "y": y-1},  # Left
            {"x": x,    "y": y+1},  # Right
            {"x": x+1,  "y": y-1},  # Bottom right
            {"x": x+1,  "y": y},    # Bottom middle
            {"x": x+1,  "y": y+1},  # Bottom left
        ]
        for n in coords:
            try:
                neighbors.append(self.tiles[n["x"]][n["y"]])
            except KeyError:
                pass
        return neighbors

    def onClickWrapper(self, x, y, local):
        return lambda Button: self.onClick(self.tiles[x][y], NAMETAG, local)

    def onRightClickWrapper(self, x, y, local):
        return lambda Button: self.onRightClick(self.tiles[x][y], NAMETAG, local)

    def onClick(self, tile, player, local):
        if local and self.controller.mode == "multiplayer":
            connection.send(0, tile, player)
        # Added check for when "mode == singleplayer" to shorten if-statement since both calls do the same
        elif local == None or self.controller.mode == "singleplayer":
            pass
        # Incase recieving client is in tile generation
        elif self.loading:
            return
        else:
            tile = self.tiles[tile["x"]][tile["y"]]

        if tile["state"] == STATE_FLAGGED:
            return

        if self.startTime == None:
            self.startTime = datetime.now()

        if self.clickedCount == 0:
            if tile["isMine"]:
                tile["isMine"] = False
                self.mines -= 1
    
            tile["mines"] = 0

            for neighborTile in self.getNeighbors(tile["coords"]["x"], tile["coords"]["y"]):
                if neighborTile["isMine"]:
                    neighborTile["isMine"] = False
                    self.mines -= 1
                    
            self.calculateMines()
            self.refreshLabels()

        if local != None:
            tileNeighbors = self.getNeighbors(tile["coords"]["x"], tile["coords"]["y"])
            flaggedNeighboringMines = [i for i in [i for i in tileNeighbors if i["isMine"]] if i["state"] == 2]

            if tile["mines"] == len(flaggedNeighboringMines) and tile["mines"] > 0:
                remainingNeighboringTiles = [i for i in tileNeighbors if i not in flaggedNeighboringMines]
                for remainingTile in remainingNeighboringTiles:
                    if not remainingTile["state"] == STATE_FLAGGED:
                        self.onClick(remainingTile, NAMETAG, None)

            if tile["isMine"] == True:
                # End game
                tile["button"].config(bg="#ff0000")
                self.gameOver(False, player)
                return

        # Change image
        if tile["mines"] == 0:
            tile["button"].config(image=self.images["clicked"]())
            self.clearSurroundingTiles(tile["id"])
        else:
            tile["button"].config(image=self.images["numbers"](tile["mines"]))
        # If not already set as clicked, change state and count
        if tile["state"] != STATE_CLICKED:
            tile["state"] = STATE_CLICKED
            self.clickedCount += 1
        if self.clickedCount == (SIZE_X * SIZE_Y) - self.mines:
            self.gameOver(True)

    def onRightClick(self, tile, player, local):
        if local and self.controller.mode == "multiplayer":
            connection.send(1, tile, player)
        elif self.controller.mode == "singleplayer":
            pass
        # Incase recieving client is in tile generation
        elif self.loading:
            return
        else:
            tile = self.tiles[tile["x"]][tile["y"]]

        # If not clicked
        if tile["state"] == STATE_DEFAULT:
            tile["button"].config(image = self.images["flag"]())
            tile["state"] = STATE_FLAGGED
            tile["button"].unbind(BTN_CLICK)
            """ # ? Why is this code here
            for keybind in [config.get("Keybinds", "click").lower(), config.get("Keybinds", "click").upper()]:
                try:
                    window.bind(f"<{keybind}>", lambda _ : self.onClick(self.cursorLocations[CURSOR_COLOR], NAMETAG, True))
                except TclError:
                    continue
            """
            # If a mine
            if tile["isMine"] == True:
                self.correctFlagCount += 1
            self.flagCount += 1
            self.refreshLabels()
        # If flagged, unflag
        elif tile["state"] == 2:
            tile["button"].config(image = self.images["plain"]())
            tile["state"] = 0
            tile["button"].bind(BTN_CLICK, self.onClickWrapper(tile["coords"]["x"], tile["coords"]["y"], True))
            # If a mine
            if tile["isMine"] == True:
                self.correctFlagCount -= 1
            self.flagCount -= 1
            self.refreshLabels()

    def clearSurroundingTiles(self, id):
        queue = deque([id])

        while len(queue) != 0:
            key = queue.popleft()
            parts = key.split("_")
            x = int(parts[0])
            y = int(parts[1])

            for tile in self.getNeighbors(x, y):
                self.clearTile(tile, queue)

    def clearTile(self, tile, queue):
        if tile["state"] != STATE_DEFAULT:
            return

        if tile["mines"] == 0:
            tile["button"].config(image = self.images["clicked"]())
            queue.append(tile["id"])
        else:
            tile["button"].config(image = self.images["numbers"](tile["mines"]))

        tile["state"] = STATE_CLICKED
        self.clickedCount += 1

    def animationFocusWrapper(self, x, y):
        return lambda Button: self.animationFocus(self.tiles[x][y])

    def animationDefocusWrapper(self, x, y):
        return lambda Button: self.animationDefocus(self.tiles[x][y])

    def animationFocus(self, tile):
        if self.paused:
            return

        # self.cursorLocations[CURSOR_COLOR] = tile["button"]
        self.cursorLocations[CURSOR_COLOR] = tile
        tile["button"].configure(bg=[self.colorModeDict[COLOR_MODE]["field"], CURSOR_COLOR][HIGHLIGHT_SQUARES_LOCALLY])
        
        if self.controller.mode == "multiplayer":
            connection.send(f"focus:{CURSOR_COLOR}", tile, NAMETAG)

    def animationDefocus(self, tile):
        if self.paused:
            return

        localPrevButton = tile["button"]

        # List over all occupied buttons, except the one sending focus-packet
        LANCursorLocations = self.cursorLocations

        try:
            LANCursorLocations.pop(CURSOR_COLOR)
        except KeyError:
            pass

        # Filter through the list to check if there is someone else occupying the previously selected square
        if localPrevButton in list(LANCursorLocations.values()):
            localPrevButton.configure(bg=list(LANCursorLocations.keys())[list(LANCursorLocations.values()).index(localPrevButton)])
        else:
            localPrevButton.configure(bg=self.colorModeDict[COLOR_MODE]["field"])

    def animationPlayerCursor(self, tileID, action):
        # // print("[!] ", end="")
        # // print(self.cursorLocations, end="     ")
        # Incase recieving client is in tile generation
        if self.loading:
            return

        tile = self.tiles[tileID["x"]][tileID["y"]]
        color = action.split(":")[1]
        
        if color in self.cursorLocations:
            prevTile = self.cursorLocations[color]

            # List over all occupied buttons, except the one sending focus-packet
            LANCursorLocations = self.cursorLocations
            LANCursorLocations.pop(color)

            # Filter through the list to check if there is someone else occupying the previously selected square
            if prevTile in list(LANCursorLocations.values()):
                prevTile["button"].configure(bg=list(LANCursorLocations.keys())[list(LANCursorLocations.values()).index(prevTile)])
            else:
                prevTile["button"].configure(bg=self.colorModeDict[COLOR_MODE]["field"])
        
        # self.cursorLocations[color] = tile["button"]
        self.cursorLocations[color] = tile
        tile["button"].configure(bg=color)
        # // print(self.cursorLocations)

### END OF CLASSES ###

"""
def main(root=None, clientObject=None, argvMode="multiplayer"):
    window = root
    client = clientObject
    mode = argvMode
        
    if mode == "multiplayer":
        # Set program title
        windowTitle = "Minesweeper - Connected"
        window.title(windowTitle)

    # Bind keybinds
    window.bind('<FocusIn>', lambda _: window.attributes("-alpha", 1))
    window.bind('<FocusOut>', lambda _: window.attributes("-alpha", 1))
    
    # Create game instance
    minesweeper = Minesweeper(window)

    if mode == "multiplayer":
        threading.Thread(target=connection.recieve, args=(minesweeper,)).start()

    return minesweeper

if __name__ == "__main__":
    print("[!] Running this file is deprecated! Please run \"client.py\"!")
    # main()
"""
