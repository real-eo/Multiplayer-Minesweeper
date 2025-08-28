import ctypes


FR_PRIVATE  = 0x10

def loadFont(fontPath):
    file = ctypes.byref(ctypes.create_unicode_buffer(fontPath))

    flags = FR_PRIVATE

    ctypes.windll.gdi32.AddFontResourceExW(file, flags, 0)

# Font family: "Square Curved M"
loadFont("font/square-curved-m.ttf")

