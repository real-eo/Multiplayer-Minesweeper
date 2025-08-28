import libs.themeConfig as themeConfig
from PIL import Image, ImageTk
from libs.animation import *
from tkinter import *
import configparser
import ctypes


config = configparser.ConfigParser()
config.read("settings.ini")

class LoadingScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Game
        self.controller = controller
        self.ID = "LoadingScreen"

        # Settings
        self.colorModeDict = themeConfig.colorModeDict

        self.COLOR_MODE = config.get("Settings", "theme").lower()
        self.config(bg=self.colorModeDict[self.COLOR_MODE]["color"])

        # Loading screen
        self.loadingScreen = Frame(self, bg=self.colorModeDict[self.COLOR_MODE]["color"])
        self.loadingScreen.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)

        self.animationWidget = Label(self.loadingScreen, bg=self.colorModeDict[self.COLOR_MODE]["color"])
        self.animationWidget.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)

        self.loadingAnimation = Animation(self, self.animationWidget, animationtype=ANIMATION_SEQUENCE, frameduration=self.colorModeDict[self.COLOR_MODE]["animation"]["loading"]["duration"], filelocation=f"images/{self.COLOR_MODE}/loading/", framename="loading", frames=self.colorModeDict[self.COLOR_MODE]["animation"]["loading"]["frames"], imagesize=(200, 200), resizealgorithm=0)

        self.windowChanged()

    def windowChanged(self):
        if self.controller.attributes("-fullscreen"):
            self.loadingAnimation.imagesize((100, 100))
            
            width, height = self.controller.winfo_width(), self.controller.winfo_height()
            relX, relY = (width - 100)/width, (height - 100)/height, 

            self.animationWidget.place(relx=relX, rely=relY, relwidth=1, relheight=1, anchor=CENTER)
        else:
            self.loadingAnimation.imagesize((200, 200))
            self.animationWidget.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)
    
    def startLoadingAnimation(self):
        self.loadingAnimation.start()
    
    def stopLoadingAnimation(self):
        self.loadingAnimation.stop()
        self.loadingAnimation.reset()
        self.loadingAnimation.hide()
        