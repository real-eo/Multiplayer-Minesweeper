import itertools


# List for sequence generation
Inputlist = {1, 2, 3}

# Calling the function Cycle from
# itertools and passing list as
# an argument and the function
# returns the iterator object
ListBuffer = itertools.islice(itertools.cycle(Inputlist), 0, None)

print(next(ListBuffer))
print(Inputlist[1])


"""
import random
import color


startHue = 251  # 204
startSaturation = 0.32  # 0.49
startValue = 1.0  # 0.89

endHue = 349
endSaturation = 0.75
endValue = 0.87

step = 7

for i in range(step+1):
    H = startHue + ((endHue - startHue)/step) * i  # Hue
    S = startSaturation + ((endSaturation - startSaturation)/step) * i  # Saturation
    V = startValue + ((endValue - startValue)/step) * i  # Value

    hexColor = color.HSVtoHex(H, S, V)

    print(f"{i + 1}: {hexColor}")

# """
