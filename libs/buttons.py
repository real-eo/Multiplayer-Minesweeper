from tkinter import *
import itertools
import keyboard


class MenuButton(Button):
    def __init__(self, master, **kw):
        Button.__init__(self, master=master, **kw)
        
        self.defaultForeground = self["foreground"]

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self['foreground'] = self['activeforeground']

    def on_leave(self, event):
        self['foreground'] = self.defaultForeground

class BooleanButton(MenuButton):
    def __init__(self, state: bool, master, **kw):
        MenuButton.__init__(self, master=master, **kw)
        
        self.state = bool(state)
        self.baseString = self.cget("text")
        self.config(text="%s%s" % (self.baseString, str(self.state)))

    def updateValue(self):
        self.state = bool(self.state ^ 1)
        self.config(text="%s%s" % (self.baseString, str(self.state)))

class CycleButton(MenuButton):
    def __init__(self, sequence: list | tuple, startIndex: int, master, **kw):
        MenuButton.__init__(self, master=master, **kw)

        self.state = str(sequence[startIndex])
        self.baseString = self.cget("text")
        self.cycleSequence = itertools.islice(itertools.cycle(sequence), startIndex, None)

        self.updateValue()  

    def updateValue(self):
        self.state = str(next(self.cycleSequence))
        self.config(text="%s%s" % (self.baseString, self.state.capitalize()))

class InputButton(MenuButton):
    def __init__(self, state: str, master, **kw):
        MenuButton.__init__(self, master=master, **kw)

        self.state = state
        self.baseString = str(self.cget("text"))
        
        self.config(text="%s%s" % (self.baseString, self.state.upper()))

    def updateValue(self):
        self.config(text="<Key>")
        
        self.state = str(keyboard.read_key())
        self.config(text="%s%s" % (self.baseString, self.state.upper()))

# TODO: A lot of changes needs to be done here
class EntryButton(MenuButton):
    def __init__(self, state: str, master, **kw):
        MenuButton.__init__(self, master=master, **kw)

        self.state = state
        self.baseString = self.cget("text")
        self.config(text="%s%s" % (self.baseString, self.state))

    def updateValue(self):
        pass
