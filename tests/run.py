import numpy as np
import sys
import time
from pygame import midi
if True:
    sys.path.insert(0, 'src')
from fightertwister import FighterTwister, Encoder, ft_colors


ft = FighterTwister()

subselection = ft.encoders[:1]


def myfunction(self: Encoder, timestamp):
    colors = np.zeros(subselection.shape)
    colors[:] = ft_colors.blue
    colors[subselection.get_idx(self)] = ft_colors.green
    subselection.set_color(colors)


subselection.register_cb_hold(myfunction)


def hold(self: Encoder, timesamp):
    print('hold')


def click(self: Encoder, timestamp):
    print('click')


def slowclick(self: Encoder, timestamp):
    print('slowclick')


def dbclick(self: Encoder, timestamp):
    print('dbclick')


def press(self: Encoder, timestamp):
    print('press')


def release(self: Encoder, timestamp):
    print('release')


ft.encoders.register_cb_press(press)
ft.encoders.register_cb_release(release)
ft.encoders.register_cb_hold(hold)
ft.encoders.register_cb_click(click)
ft.encoders.register_cb_slowclick(slowclick)
ft.encoders.register_cb_dbclick(dbclick)
with ft:
    ft.encoders.set_value(0)
    ft.encoders.set_color(ft_colors.blue)
    input()
