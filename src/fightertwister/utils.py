

def clamp(value, minimum, maximum):
    return min(maximum, max(minimum, value))


def to7bit(value):
    return int(value*127+0.5)


class ft_colors:
    red = 84
    green = 45
    blue = 1
    lightblue = 30
    cyan = 40
    magenta = 105
    yellow = 68
    orange = 75
    purple = 110
