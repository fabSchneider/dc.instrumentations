import math

# clamps a vector to be within the unit circle
def clamp_to_unit(x, y):
    mag = math.sqrt(pow(x, 2) + pow(y, 2))

    if (mag > 0) :
        x = x / mag * min(mag, 1)
        y = y / mag * min(mag, 1)
    
    return x, y