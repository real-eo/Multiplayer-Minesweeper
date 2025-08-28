def HSVtoRGB(H, S, V, format="decimal"):
    # H: Hue
    # S: Saturation
    # V: Value

    chroma = S * V  # Chroma

    mHue = H / 60  # Main color component 
    x = chroma * (1 - abs(mHue % 2 - 1))  # Second largest component for a color

    RGBcolorMatrix = [
        [chroma, x, 0],
        [x, chroma, 0],
        [0, chroma, x],
        [0, x, chroma],
        [x, 0, chroma],
        [chroma, 0, x],
        [chroma, 0, x]  # Debug: In case "Hue" is set to 360; since "360/60" > [0, 5]
    ]

    mValue = V - chroma  # Color match value

    rgb = map(lambda color: [(color + mValue), int((color + mValue)*255)]["numeric" in format], RGBcolorMatrix[int(mHue)])  # (R, G, B)

    return list(rgb)


def HSVtoHex(H, S, V):
    R, G, B, = HSVtoRGB(H, S, V, format="numerical")
    
    return f"#{['', '0'][R < 16]}{str(hex(R))[2:]}{['', '0'][G < 16]}{str(hex(G))[2:]}{['', '0'][B < 16]}{str(hex(B))[2:]}"
