import libs.themeConfig as themeConfig
from PIL import Image, ImageTk
from libs.buttons import *
from tkinter.font import *
from tkinter import *
import configparser


config = configparser.ConfigParser()
config.read("settings.ini")

class OptionFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Game
        self.controller = controller

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
            "slim": Font(family=fontConfig["family"], size=0, weight=fontConfig["weight"], slant=fontConfig["slant"], underline=fontConfig["underline"], overstrike=fontConfig["overstrike"]),
            "small": Font(family=fontConfig["family"], size=0, weight=fontConfig["weight"], slant=fontConfig["slant"], underline=fontConfig["underline"], overstrike=fontConfig["overstrike"])
        }

        # Setting buttons       
        self.backButton = MenuButton(master=self, image=self.images["short-button"](), text="Back", font=self.fonts["small"], compound="center", anchor=E, fg=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["normal"], activeforeground=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["active"], bg=self.colorModeDict[self.COLOR_MODE]["color"], activebackground=self.colorModeDict[self.COLOR_MODE]["color"], relief=[SUNKEN, RAISED][self.ANIMATE_BUTTONS], borderwidth=self.colorModeDict[self.COLOR_MODE]["border"]*2, command=lambda: self.controller.showFrame(self.controller.settings["settings"])) 
        self.backButton.place(relx=0.1, rely=0.9, anchor=CENTER)

        self.buttons = (self.backButton,)

        self.config(bg=self.colorModeDict[self.COLOR_MODE]["color"])

        self.__windowChanged__()

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

    def __windowChanged__(self):
        for button in self.buttons:
            imageID = self.pyimageMap[button.cget('image')]
            button.configure(image=self.images[imageID]())

        self.fonts["normal"].configure(size=[12, 40][self.controller.attributes("-fullscreen")])
        self.fonts["slim"].configure(size=[9, 30][self.controller.attributes("-fullscreen")])
        self.fonts["small"].configure(size=[10, 24][self.controller.attributes("-fullscreen")])

        if self.controller.attributes("-fullscreen"):
            width, height = self.controller.winfo_width(), self.controller.winfo_height()
            relX, relY = (130)/width, (height - 100)/height, 

            self.backButton.place(relx=relX, rely=relY, anchor=CENTER)
        else:
            self.backButton.place(relx=0.14, rely=0.9, anchor=CENTER)

class GeneralSettings(OptionFrame):
    def __init__(self, parent, controller):
        OptionFrame.__init__(self, parent, controller)

        self.themes = tuple(self.colorModeDict.keys())
        self.themeCycleStartIndex = self.themes.index(self.COLOR_MODE)

        self.themeButton = CycleButton(sequence=self.themes, startIndex=self.themeCycleStartIndex, master=self, image=self.images["slim-button"](), text="Theme: ", font=self.fonts["slim"], compound="center", anchor=E, fg=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["normal"], activeforeground=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["active"], bg=self.colorModeDict[self.COLOR_MODE]["color"], activebackground=self.colorModeDict[self.COLOR_MODE]["color"], relief=[SUNKEN, RAISED][self.ANIMATE_BUTTONS], borderwidth=self.colorModeDict[self.COLOR_MODE]["border"]*2, command=lambda: self.themeButton.updateValue()) 
        self.cursorColorEntry = EntryButton(state=config.get("Settings", "cursorColor"), master=self, image=self.images["slim-button"](), text="Cursor: ", font=self.fonts["slim"], compound="center", anchor=E, fg=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["normal"], activeforeground=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["active"], bg=self.colorModeDict[self.COLOR_MODE]["color"], activebackground=self.colorModeDict[self.COLOR_MODE]["color"], relief=[SUNKEN, RAISED][self.ANIMATE_BUTTONS], borderwidth=self.colorModeDict[self.COLOR_MODE]["border"]*2, command=lambda: self.cursorColorEntry.updateValue())
        self.displayCursorButton = BooleanButton(state=config.getboolean("Settings", "displayCursorLocally"), master=self, image=self.images["slim-button"](), text="Show cursor: ", font=self.fonts["slim"], compound="center", anchor=E, fg=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["normal"], activeforeground=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["active"], bg=self.colorModeDict[self.COLOR_MODE]["color"], activebackground=self.colorModeDict[self.COLOR_MODE]["color"], relief=[SUNKEN, RAISED][self.ANIMATE_BUTTONS], borderwidth=self.colorModeDict[self.COLOR_MODE]["border"]*2, command=lambda: self.displayCursorButton.updateValue())
        self.animateButtonsButton = CycleButton(sequence=("Sturdy", "Animated"), startIndex=self.ANIMATE_BUTTONS, master=self, image=self.images["slim-button"](), text="Buttons: ", font=self.fonts["slim"], compound="center", anchor=E, fg=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["normal"], activeforeground=self.colorModeDict[self.COLOR_MODE]["text"]["menu"]["active"], bg=self.colorModeDict[self.COLOR_MODE]["color"], activebackground=self.colorModeDict[self.COLOR_MODE]["color"], relief=[SUNKEN, RAISED][self.ANIMATE_BUTTONS], borderwidth=self.colorModeDict[self.COLOR_MODE]["border"]*2, command=lambda: self.animateButtonsButton.updateValue())

        self.buttons += (self.themeButton, self.cursorColorEntry, self.displayCursorButton, self.animateButtonsButton)

    def windowChanged(self):
        self.themeButton.place(cnf=[{"relx": 0.5, "rely": 0.23 + 0.0675, "anchor": CENTER}, {"relx": 0.49, "rely": 0.23 + 0.0675, "anchor": E}][self.controller.attributes("-fullscreen")])
        self.cursorColorEntry.place(cnf=[{"relx": 0.5, "rely": 0.335 + 0.0675, "anchor": CENTER}, {"relx": 0.51, "rely": 0.23 + 0.0675, "anchor": W}][self.controller.attributes("-fullscreen")])
        self.displayCursorButton.place(cnf=[{"relx": 0.5, "rely": 0.44 + 0.0675, "anchor": CENTER}, {"relx": 0.49, "rely": 0.335 + 0.0675, "anchor": E}][self.controller.attributes("-fullscreen")])
        self.animateButtonsButton.place(cnf=[{"relx": 0.5, "rely": 0.545 + 0.0675, "anchor": CENTER}, {"relx": 0.51, "rely": 0.335 + 0.0675, "anchor": W}][self.controller.attributes("-fullscreen")])

        self.__windowChanged__()

class VideoSettings(OptionFrame):
    def __init__(self, parent, controller):
        OptionFrame.__init__(self, parent, controller)

    def windowChanged(self):
        self.__windowChanged__()

class InputSettings(OptionFrame):
    def __init__(self, parent, controller):
        OptionFrame.__init__(self, parent, controller)

    def windowChanged(self):
        self.__windowChanged__()

class GameSettings(OptionFrame):
    def __init__(self, parent, controller):
        OptionFrame.__init__(self, parent, controller)

    def windowChanged(self):
        self.__windowChanged__()
