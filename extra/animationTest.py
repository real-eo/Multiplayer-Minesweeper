from libs.animation import *
from tkinter import *


root = Tk()
root.geometry("300x300")
 
backgroundColor = "#4b4b4b"

display_frame = Frame(root, bg=backgroundColor)
display_frame.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)

display = Label(display_frame, bg=backgroundColor)
display.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)

# a = Label(root, bg="#aaaaaa")
# a.place(relx=0.5, rely=0.5, relwidth=0.1, relheight=0.1, anchor=CENTER)

animation = Animation(root, display, animationtype=ANIMATION_SEQUENCE, frameduration=50, filelocation="images/heist/loading/", framename="loading", frames=21, imagesize=(200, 200), resizealgorithm=0)

animation.start()
    
def windowChanged(event):
    global animation

    root.attributes("-fullscreen", (root.attributes("-fullscreen") + 1) % 2)

    if root.attributes("-fullscreen"):
        animation.imagesize((100, 100))
        
        width, height = root.winfo_width(), root.winfo_height()
        relX, relY = (width - 100)/width, (height - 100)/height, 

        display.place(relx=relX, rely=relY, relwidth=1, relheight=1, anchor=CENTER)
    else:
        animation.imagesize((200, 200))

        display.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=CENTER)

def startAnimation(event):
    if animation.animationRunning:
        animation.stop()
            
    animation.start()
    display_frame.lift()

def stopAnimation(event):
    display_frame.lower()
    animation.stop()
    animation.reset()

root.bind('<space>', lambda event: [animation.start, animation.stop][animation.animationRunning]())
root.bind("<r>", lambda event: animation.reset())
root.bind("<h>", lambda event: animation.hide())

# root.bind("<a>", startAnimation)
# root.bind("<s>", stopAnimation)

root.bind("<F11>", windowChanged)

# threading.Thread(target=run_animation, args=(1,)).start()

root.mainloop()
