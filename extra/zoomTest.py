from ..libs import color
from tkinter import *
import threading
import random


window = Tk()

window.geometry("1000x1000")
window.attributes('-topmost', 1)

gridX = 50
gridY = 50

gridSubdivision = 5

gridSize = 1000

fieldSizeW = (gridSize/max(gridY/gridX, 1))
fieldSizeH = (gridSize/max(gridX/gridY, 1))

topFrame = Frame(master=window, bg="green", width=fieldSizeW, height=fieldSizeH)
topFrame.place(relx=0.5, rely=0.5, anchor=CENTER,)

btnFrame = Frame(master=topFrame, bg="red")
btnFrame.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)

btnImg = PhotoImage(file="images/tile_1.gif")

def populateGrid(xOffset, yOffset):
    for y in range(int(gridY/gridSubdivision)):
        for x in range(int(gridX/gridSubdivision)):
            # bg=f"#{str(hex(int(255/int(gridX/gridSubdivision)) * (x + 1)))[2:]}00{str(hex(int(255/int(gridX/gridSubdivision)) * (y + 1)))[2:]}"
            # image=btnImg
            # bg=f"#{str(hex(int(redNum)))[2:]}{str(hex(int(greenNum)))[2:]}{str(hex(int(blueNum)))[2:]}"
            H = random.randint(0, 360)   # Hue
            S = random.uniform(0.5, 1)   # Saturation
            V = random.uniform(0.85, 1)  # Value

            btn = Button(master=btnFrame, bg=color.HSVtoHex(H, S, V))
            btn.place(relx=(1/gridX)*(x+xOffset), rely=(1/gridY)*((y+yOffset)), relwidth=1/gridX, relheight=1/gridY)

frameIndex = 0
for y in range(gridSubdivision):
    for x in range(gridSubdivision):
        threading.Thread(target=(populateGrid), args=((gridX/gridSubdivision)*(x), (gridY/gridSubdivision)*(y))).start()
        frameIndex += 1

def zoom(event):
    factor = 1.001 ** event.delta
    posX, posY = float(event.widget.place_info()["relx"])+(event.x/fieldSizeW), float(event.widget.place_info()["rely"])+(event.y/fieldSizeH)

    relWidth = max(float(btnFrame.place_info()["relwidth"])*factor, 1)
    relHeight = max(float(btnFrame.place_info()["relheight"])*factor, 1)
    relX = max(min(posX-(posX*2-1), relWidth/2), abs((relHeight/2)-1))
    relY = max(min(posY-(posY*2-1), relHeight/2), abs((relHeight/2)-1))
    
    btnFrame.place(relx=relX, rely=relY, relwidth=relWidth, relheight=relHeight)

"""def drag(event):
    posX, posY = float(event.widget.place_info()["relx"])+(event.x/fieldSizeW), float(event.widget.place_info()["rely"])+(event.y/fieldSizeH)
    
    relWidth = float(btnFrame.place_info()["relwidth"])
    relHeight = float(btnFrame.place_info()["relheight"])
    relX = max(min(posX, relWidth/2), abs((relHeight/2)-1))
    relY = max(min(posY, relHeight/2), abs((relHeight/2)-1))

    btnFrame.place(relx=relX, rely=relY)"""

def click(event):
    global posXo, posYo

    posXo, posYo = float(event.widget.place_info()["relx"])+(event.x/fieldSizeW), float(event.widget.place_info()["rely"])+(event.y/fieldSizeH)

def release(event):
    posX, posY = float(event.widget.place_info()["relx"])+(event.x/fieldSizeW), float(event.widget.place_info()["rely"])+(event.y/fieldSizeH)

    relWidth = float(btnFrame.place_info()["relwidth"])
    relHeight = float(btnFrame.place_info()["relheight"])
    relX = max(min(float(btnFrame.place_info()["relx"]) + (posX-posXo), relWidth/2), abs((relHeight/2)-1))
    relY = max(min(float(btnFrame.place_info()["rely"]) + (posY-posYo), relHeight/2), abs((relHeight/2)-1))

    btnFrame.place(relx=relX, rely=relY)


window.bind("<MouseWheel>", lambda event: threading.Thread(target=zoom, args=(event,)).start())
# window.bind("<B1-Motion>", lambda event: threading.Thread(target=drag, args=(event,)).start())
window.bind("<ButtonPress-1>", lambda event: threading.Thread(target=click, args=(event,)).start())
window.bind("<ButtonRelease-1>", lambda event: threading.Thread(target=release, args=(event,)).start())

window.mainloop()
