from scipy.interpolate import UnivariateSpline


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

    def __repr__(self) -> str:
        return f"Task: {self.function.__name__}, {self.args}, {self.kwargs}"


class ft_colors:
    red = 85
    green = 45
    dark_blue = 1
    blue = 1
    light_blue = 24
    cyan = 38
    magenta = 105
    yellow = 64
    bright_orange = 69
    orange = 76
    purple = 110


heat_spline = UnivariateSpline([0, 0.5, 0.6, 1],
                               [ft_colors.blue,
                                ft_colors.green,
                                ft_colors.yellow,
                                ft_colors.red],
                               k=1)


def heat_color(value):
    return int(heat_spline(value)+0.5)


def to_range(value, start, stop):
    return value/(stop-start) + start
