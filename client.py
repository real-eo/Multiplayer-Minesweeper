from options import GeneralSettings, VideoSettings, InputSettings, GameSettings
from minesweeper import Minesweeper
from loading import LoadingScreen
from settings import Settings
from tkinter import *
from menu import Menu
import configparser
import connection
import ctypes


class Game(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
        # * Window settings
        self.attributes('-topmost', 1)

        self.tk.call("tk", "scaling", config.getfloat("Settings", "scale"))

        self.resizable(False, False)
        self.minsize(300, 300)

        windowTitle = "Minesweeper"
        self.title(windowTitle)

        # * Font
        loadFont("font/square-curved-m.ttf")

        # * Frames
        self.menu = Menu
        self.settings = {"settings": Settings, "general": GeneralSettings, "video": VideoSettings, "input": InputSettings, "game": GameSettings}
        self.minesweeper = Minesweeper
        self.loadingScreen = LoadingScreen

        # Creating a frame and assigning it to container
        windowContainer = Frame(self)
        # Specifying the region where the frame is packed in root
        windowContainer.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)
        # // windowContainer.pack(fill=BOTH)

        self.mode = ""
        self.loadRequest = ""

        # * Global Events
        for keybind in [config.get("Keybinds", "fullscreen").lower(), config.get("Keybinds", "fullscreen").upper()]:
            try:
                self.bind(f"<{keybind}>", self.windowChanged)
            except TclError:
                continue

        # * Frames
        # Create a dictionary for the frames
        self.frames = {}

        # We'll create the frames themselves later but let's add the components to the dictionary.
        for FRAME in (Menu, Minesweeper, LoadingScreen, Settings, GeneralSettings, VideoSettings, InputSettings, GameSettings):
            frame = FRAME(windowContainer, self)

            # The windows class acts as the root window for the frames.
            self.frames[FRAME] = frame
            frame.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)

        # Using a method to switch frames
        self.showFrame(self.menu)

    def showFrame(self, frame):
        self.activeFrame = self.frames[frame]
        self.activeFrame.tkraise()

        self.windowChanged("frameUpdate")

    def runAction(actions=[]):
        for action in actions:
            action()

    def windowChanged(self, event):
        if not event == "frameUpdate":
            self.attributes("-fullscreen", (self.attributes("-fullscreen") + 1) % 2)

        self.activeFrame.windowChanged()

    
def loadFont(fontPath):
    file = ctypes.byref(ctypes.create_unicode_buffer(fontPath))

    flags = (FR_PRIVATE:=0x10)

    ctypes.windll.gdi32.AddFontResourceExW(file, flags, 0)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("settings.ini")

    game = Game()
    game.mainloop()

    if game.mode == "multiplayer":
        connection.exit(exitCode=1)
