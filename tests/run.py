import numpy as np
import sys
import time
from pygame import midi
if True:
    sys.path.insert(0, 'src')
from fightertwister import FighterTwister, Encoder, ft_colors


ft = FighterTwister()
layer1 = ft.encoders[:16]


def hold(self: Encoder):
    print('hold')
    # self.set_color(ft_colors.red)


def click(self: Encoder, timestamp):
    print('click')


def dbclick(self: Encoder, timestamp):
    print('dbclick')


def press(self: Encoder, timestamp):
    print('press')


def release(self: Encoder, timestamp):
    print('release')


layer1.register_cb_switch_press(press)
layer1.register_cb_switch_release(release)
layer1.register_cb_hold(hold)
layer1.register_cb_click(click)
layer1.register_cb_dbclick(dbclick)
with ft:
    ft.encoders.set_value(0)
    ft.encoders.set_color(ft_colors.blue)

    input()
