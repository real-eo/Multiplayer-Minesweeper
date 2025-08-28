from PIL import Image, ImageTk, ImageSequence
import itertools


class Animation:
    def __init__(self, root, widget, **kwargs):
        self.root = root
        self.widget = widget

        self.animationRunning = False
        self.animationHidden = False

        self.animationType, self.frameDuration = kwargs["animationtype"], kwargs["frameduration"]

        self.settings = {"root": self.root, "widget": self.widget, "duration": self.frameDuration}

        if self.animationType == ANIMATION_SEQUENCE:
            self.settings["location"] = kwargs["filelocation"] if kwargs["filelocation"][-1] == "/" else kwargs["filelocation"] + "/"
            self.settings["name"] = kwargs["framename"]
            self.settings["frames"] = kwargs["frames"]

            self.settings["separator"] = kwargs["frameseparator"] if "frameseparator" in kwargs else "-"
            self.settings["imageType"] = kwargs["filetype"] if "filetype" in kwargs else "png"
            self.settings["resizeAlgorithm"] = kwargs["resizealgorithm"] if "resizealgorithm" in kwargs else 0

            self.settings["modifier"] = lambda frame: frame.resize(kwargs["imagesize"], self.settings["resizeAlgorithm"]) if "imagesize" in kwargs else lambda frame: frame
        else:
            self.settings["file"] = kwargs["file"]
        
        self.__generate_frames__()

    def __generate_frames__(self, startIndex=0):
        # Create an infinite cycle of PIL ImageTk images for display on label
        self.frameList = []

        if self.animationType == ANIMATION_SEQUENCE:
            for frameIndex in range(self.settings["frames"]):
                frame = Image.open(f"{self.settings['location']}{self.settings['name']}{self.settings['separator']}{frameIndex}.{self.settings['imageType']}")
                self.frameList.append(self.settings['modifier'](frame))
        else:
            PILImage = Image.open(self.settings["file"])
            
            # // Get frame duration, assuming all frame durations are the same
            # // self.duration = PILImage.info.get('duration', None)   # None for WEBP

            if self.frameDuration == None:
                with open(self.settings['file'], 'rb') as binfile:
                    data = binfile.read()

                pos = data.find(b'ANMF')  # Extract duration for WEBP sequences

                self.duration = int.from_bytes(data[pos+12:pos+15], byteorder='big')

            for frame in ImageSequence.Iterator(PILImage):
                cp = frame.copy()
                self.frameList.append(cp)

        self.tkframeList = [ImageTk.PhotoImage(image=frame) for frame in self.frameList]
        self.tkframeSequence = itertools.islice(itertools.cycle(enumerate(self.tkframeList)), startIndex, None)
        self.tkframeIterator = iter(self.tkframeList)

        if not self.animationHidden:
           self.__init_animation__()

    def __update_settings__(self, setting, value):
        self.settings[setting] = value

        self.__generate_frames__(startIndex=int(str(next(self.tkframeSequence)[0]-1).replace("-1", str(len(self.tkframeList) - 1))))


    def imagesize(self, size):
        self.__update_settings__("modifier", lambda frame: frame.resize(size, self.settings["resizeAlgorithm"]))


    def __init_animation__(self):
        self.animationHidden = False
        img = next(self.tkframeSequence)
        self.widget.config(image=img[1])

    def __show_animation__(self):
        self.animationHidden = False
        self.afterID = self.root.after(self.frameDuration, self.__show_animation__)
        img = next(self.tkframeSequence)
        self.widget.config(image=img[1])


    def start(self):        
        self.animationRunning = True
        self.__show_animation__()

    def reset(self):
        self.tkframeSequence = itertools.islice(itertools.cycle(enumerate(self.tkframeList)), 0, None)

        self.__init_animation__()

    def hide(self):
        self.animationHidden = True
        self.widget.config(image="")

    def stop(self):
        self.animationRunning = False
        self.root.after_cancel(self.afterID)


if not __name__ == "__main__":
    ANIMATED_FILE = "single"
    ANIMATION_SEQUENCE = "sequence"
