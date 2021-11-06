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
    red = 85+127
    green = 45+127
    dark_blue = 1+127
    blue = 1+127
    light_blue = 24+127
    cyan = 38+127
    magenta = 105+127
    yellow = 64+127
    bright_orange = 69+127
    orange = 76+127
    purple = 110+127


heat_spline = UnivariateSpline([0, 0.5, 0.6, 1],
                               [ft_colors.blue,
                                ft_colors.green,
                                ft_colors.yellow,
                                ft_colors.red],
                               k=1)


def heat_color(value):
    return int(heat_spline(value)+0.5)


def to_range(value, start, stop):
    return value*(stop-start) + start
