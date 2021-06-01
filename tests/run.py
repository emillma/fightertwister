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


def foo(self: Encoder, timestamp):
    # self.set_color(self.value*125+1)
    print(self.value)


ft.encoders.register_cb_encoder(foo)


def hold(self: Encoder, timesamp):
    print('hold')


def click(self: Encoder, timestamp):
    # print('click')
    print(round(self.value*125+1))


def slowclick(self: Encoder, timestamp):
    print('slowclick')


def dbclick(self: Encoder, timestamp):
    print('dbclick')


def press(self: Encoder, timestamp):
    print('press')


def release(self: Encoder, timestamp):
    print('release')


# ft.encoders.register_cb_press(press)
# ft.encoders.register_cb_release(release)
# ft.encoders.register_cb_hold(hold)
ft.encoders.register_cb_click(click)
# ft.encoders.register_cb_slowclick(slowclick)
# ft.encoders.register_cb_dbclick(dbclick)
with ft:
    ft.encoders.set_value(0)
    ft.encoders.set_color(ft_colors.blue)
    # ft.encoders[:, ::2, ::2].set_color(ft_colors.cyan)
    # ft.encoders[0, 0, [0, 1, 2]].set_color(
    #     [ft_colors.yellow, ft_colors.orange, ft_colors.red])
    input()
