import libs.themeConfig as themeConfig
from PIL import Image, ImageTk
from libs.animation import *
from libs.buttons import *
from tkinter.font import *
from tkinter import *
import configparser
import ctypes


config = configparser.ConfigParser()
config.read("settings.ini")

class Menu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Game
        self.controller = controller
        self.controller.mode = ""
        self.ID = "Menu"

        # Settings
        self.colorModeDict = themeConfig.colorModeDict

        self.COLOR_MODE = config.get("Settings", "theme").lower()
        self.ANIMATE_BUTTONS = config.getboolean("Settings", "animateButtons")

        # Generate Images
        self.generateImages()

        # Font
        fontConfig = {
            'family': 'Square Curved M', 
            'weight': 'normal',
            'slant': 'roman', 
            'underline': False, 
            'overstrike': False
        }

        self.fonts = {
            "normal": Font(family=fontConfig["family"], size=0, weight=fontConfig["weight"], slant=fontConfig["slant"], underline=fontConfig["underline"], overstrike=fontConfig["overstrike"]), 
            "small": Font(family=fontConfig["family"], size=0, weight=fontConfig["weight"], slant=fontConfig["slant"], underline=fontConfig["underline"], overstrike=fontConfig["overstrike"])
        }
        # Menu buttons
        self.singleplayerButton = MenuButton(master=self, image=self.images["singleplayer-button"](), text="Singleplayer", font=self.fonts["normal"], compound="center", anchor=E, fg=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["normal"], activeforeground=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["active"], bg=self.colorModeDict[self.COLOR_MODE]["color"], activebackground=self.colorModeDict[self.COLOR_MODE]["color"], relief=[SUNKEN, RAISED][self.ANIMATE_BUTTONS], borderwidth=self.colorModeDict[self.COLOR_MODE]["border"]*2, command=lambda: self.startGame("singleplayer"))
        self.multiplayerButton = MenuButton(master=self, image=self.images["multiplayer-button-left"](), text="Multiplayer", font=self.fonts["normal"], compound="center", anchor=E, fg=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["normal"], activeforeground=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["active"], bg=self.colorModeDict[self.COLOR_MODE]["color"], activebackground=self.colorModeDict[self.COLOR_MODE]["color"], relief=[SUNKEN, RAISED][self.ANIMATE_BUTTONS], borderwidth=self.colorModeDict[self.COLOR_MODE]["border"]*2, command=lambda: self.startGame("multiplayer"))
        self.settingsButton = MenuButton(master=self, image=self.images["settings-button-left"](), text="Settings", font=self.fonts["normal"], compound="center", anchor=E, fg=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["normal"], activeforeground=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["active"], bg=self.colorModeDict[self.COLOR_MODE]["color"], activebackground=self.colorModeDict[self.COLOR_MODE]["color"], relief=[SUNKEN, RAISED][self.ANIMATE_BUTTONS], borderwidth=self.colorModeDict[self.COLOR_MODE]["border"]*2, command=lambda: self.controller.showFrame(self.controller.settings["settings"]))
        self.quitButton = MenuButton(master=self, image=self.images["short-button"](), text="Quit", font=self.fonts["small"], compound="center", anchor=E, fg=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["normal"], activeforeground=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["active"], bg=self.colorModeDict[self.COLOR_MODE]["color"], activebackground=self.colorModeDict[self.COLOR_MODE]["color"], relief=[SUNKEN, RAISED][self.ANIMATE_BUTTONS], borderwidth=self.colorModeDict[self.COLOR_MODE]["border"]*2, command=lambda: self.controller.destroy())

        self.singleplayerButton.place(relx=0.5, rely=0.4166, anchor=CENTER)
        self.multiplayerButton.place(relx=0.5, rely=0.5462, anchor=CENTER)
        self.settingsButton.place(relx=0.5, rely=0.6759, anchor=CENTER)
        self.quitButton.place(relx=0.14, rely=0.9, anchor=CENTER)

        self.buttons = [self.singleplayerButton, self.multiplayerButton, self.settingsButton, self.quitButton]

        self.config(bg=self.colorModeDict[self.COLOR_MODE]["color"])

        self.windowChanged()

    def generateImages(self):
        self.pyimageMap = {}

        imageOrder = ("singleplayer-button", "multiplayer-button-left", "settings-button-left", "short-button")
        imageSize = ((660, 120), (660, 120), (660, 120), (150, 90))

        self.normalImageList = [PhotoImage(file=f"images/{self.COLOR_MODE}/{button}.png") for button in imageOrder]

        for index, image in enumerate(self.normalImageList):
            self.pyimageMap[str(image)] = imageOrder[index]

        self.scaledImageList = []

        for index, (image, size) in enumerate(zip(self.normalImageList, imageSize)):
            PILImage = ImageTk.getimage(image).resize(size, 0)
            scaledImage = ImageTk.PhotoImage(PILImage)

            self.pyimageMap[str(scaledImage)] = imageOrder[index]
            self.scaledImageList.append(scaledImage)

        self.images = {
            "singleplayer-button": lambda debug=None: [self.normalImageList[0], self.scaledImageList[0]][self.controller.attributes("-fullscreen")], 
            "multiplayer-button-left": lambda debug=None: [self.normalImageList[1], self.scaledImageList[1]][self.controller.attributes("-fullscreen")],
            "settings-button-left": lambda debug=None: [self.normalImageList[2], self.scaledImageList[2]][self.controller.attributes("-fullscreen")],
            "short-button": lambda debug=None: [self.normalImageList[3], self.scaledImageList[3]][self.controller.attributes("-fullscreen")]
        }

    def windowChanged(self):
        for button in self.buttons:
            imageID = self.pyimageMap[button.cget('image')]

            button.configure(image=self.images[imageID]())

        self.fonts["normal"].configure(size=[12, 40][self.controller.attributes("-fullscreen")])
        self.fonts["small"].configure(size=[10, 24][self.controller.attributes("-fullscreen")])

        # Quit button
        if self.controller.attributes("-fullscreen"):
            width, height = self.controller.winfo_width(), self.controller.winfo_height()
            relX, relY = (130)/width, (height - 100)/height, 

            self.quitButton.place(relx=relX, rely=relY, anchor=CENTER)
        else:
            self.quitButton.place(relx=0.14, rely=0.9, anchor=CENTER)
                
    def startGame(self, mode):
        # Set mode
        self.controller.mode = mode

        # Run game
        self.controller.frames[self.controller.minesweeper].initGame()
