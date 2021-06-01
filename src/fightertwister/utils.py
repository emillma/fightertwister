

def clamp(value, minimum, maximum):
    return min(maximum, max(minimum, value))


def to7bit(value):
    return int(value*127+0.5)


class Task:
    def __init__(self, timestamp, function, args=[], kwargs={}):
        self.timestamp = timestamp
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        return self.function(*self.args, **self.kwargs)


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
