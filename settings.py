import libs.themeConfig as themeConfig
from libs.buttons import MenuButton
from PIL import Image, ImageTk
from tkinter.font import *
from tkinter import *
import configparser
import ctypes


config = configparser.ConfigParser()
config.read("settings.ini")

class Settings(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Game
        self.controller = controller
        self.ID = "Settings"

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

        # Setting buttons
        self.generalButton = MenuButton(master=self, image=self.images["normal-button"](), text="General", font=self.fonts["normal"], compound="center", anchor=E, fg=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["normal"], activeforeground=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["active"], bg=self.colorModeDict[self.COLOR_MODE]["color"], activebackground=self.colorModeDict[self.COLOR_MODE]["color"], relief=[SUNKEN, RAISED][self.ANIMATE_BUTTONS], borderwidth=self.colorModeDict[self.COLOR_MODE]["border"]*2, command=lambda: self.controller.showFrame(self.controller.settings["general"]))
        self.videoButton = MenuButton(master=self, image=self.images["normal-button"](), text="Video", font=self.fonts["normal"], compound="center", anchor=E, fg=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["normal"], activeforeground=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["active"], bg=self.colorModeDict[self.COLOR_MODE]["color"], activebackground=self.colorModeDict[self.COLOR_MODE]["color"], relief=[SUNKEN, RAISED][self.ANIMATE_BUTTONS], borderwidth=self.colorModeDict[self.COLOR_MODE]["border"]*2, command=lambda: self.controller.showFrame(self.controller.settings["video"]))
        self.inputButton = MenuButton(master=self, image=self.images["normal-button"](), text="Controls", font=self.fonts["normal"], compound="center", anchor=E, fg=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["normal"], activeforeground=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["active"], bg=self.colorModeDict[self.COLOR_MODE]["color"], activebackground=self.colorModeDict[self.COLOR_MODE]["color"], relief=[SUNKEN, RAISED][self.ANIMATE_BUTTONS], borderwidth=self.colorModeDict[self.COLOR_MODE]["border"]*2, command=lambda: self.controller.showFrame(self.controller.settings["input"]))
        self.gameButton = MenuButton(master=self, image=self.images["normal-button"](), text="Game", font=self.fonts["normal"], compound="center", anchor=E, fg=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["normal"], activeforeground=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["active"], bg=self.colorModeDict[self.COLOR_MODE]["color"], activebackground=self.colorModeDict[self.COLOR_MODE]["color"], relief=[SUNKEN, RAISED][self.ANIMATE_BUTTONS], borderwidth=self.colorModeDict[self.COLOR_MODE]["border"]*2, command=lambda: self.controller.showFrame(self.controller.settings["game"]))

        self.backButton = MenuButton(master=self, image=self.images["short-button"](), text="Back", font=self.fonts["small"], compound="center", anchor=E, fg=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["normal"], activeforeground=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["active"], bg=self.colorModeDict[self.COLOR_MODE]["color"], activebackground=self.colorModeDict[self.COLOR_MODE]["color"], relief=[SUNKEN, RAISED][self.ANIMATE_BUTTONS], borderwidth=self.colorModeDict[self.COLOR_MODE]["border"]*2, command=lambda: self.controller.showFrame(self.controller.menu)) 

        self.generalButton.place(relx=0.5, rely=0.23 + 0.0675, anchor=CENTER)
        self.videoButton.place(relx=0.5, rely=0.365 + 0.0675, anchor=CENTER)
        self.inputButton.place(relx=0.5, rely=0.5 + 0.0675, anchor=CENTER)
        self.gameButton.place(relx=0.5, rely=0.635 + 0.0675, anchor=CENTER)

        self.backButton.place(relx=0.1, rely=0.9, anchor=CENTER)

        self.buttons = (self.generalButton, self.videoButton, self.inputButton, self.gameButton, self.backButton)

        self.config(bg=self.colorModeDict[self.COLOR_MODE]["color"])

        self.windowChanged()

    def generateImages(self):
        self.pyimageMap = {}

        imageOrder = ("normal-button", "slim-button", "short-button")
        imageSize = ((660, 120), (660, 90), (150, 90))

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
            "normal-button": lambda debug=None: [self.normalImageList[0], self.scaledImageList[0]][self.controller.attributes("-fullscreen")],
            "slim-button": lambda debug=None: [self.normalImageList[1], self.scaledImageList[1]][self.controller.attributes("-fullscreen")],
            "short-button": lambda debug=None: [self.normalImageList[2], self.scaledImageList[2]][self.controller.attributes("-fullscreen")], 
        }

    def windowChanged(self):
        for button in self.buttons:
            imageID = self.pyimageMap[button.cget('image')]
            button.configure(image=self.images[imageID]())

        self.fonts["normal"].configure(size=[12, 40][self.controller.attributes("-fullscreen")])
        self.fonts["small"].configure(size=[10, 24][self.controller.attributes("-fullscreen")])

        if self.controller.attributes("-fullscreen"):
            width, height = self.controller.winfo_width(), self.controller.winfo_height()
            relX, relY = (130)/width, (height - 100)/height, 

            self.backButton.place(relx=relX, rely=relY, anchor=CENTER)
        else:
            self.backButton.place(relx=0.14, rely=0.9, anchor=CENTER)

    def updateSetting(self, setting):
        print(setting)
