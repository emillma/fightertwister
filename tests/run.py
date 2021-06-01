import numpy as np
import sys
import time

if True:
    sys.path.insert(0, 'src')
from fightertwister import FighterTwister, Encoder, ft_colors


ft = FighterTwister()
layer1 = ft.encoders[:16]


def cb_on(self: Encoder, timestamp):
    self.set_color(ft_colors.magenta)


def cb_off(self: Encoder, timestamp):
    if timestamp < self.ts_prev_on + 1000:
        self.set_color(ft_colors.green)
    else:
        self.set_color(ft_colors.orange)


layer1.register_cb_switch_on(cb_on)
layer1.register_cb_switch_off(cb_off)

with ft:
    ft.encoders.set_value(0)
    values = np.zeros(64)
    # for i in range(1000):
    # ft.encoders.set_color(values)
    # time.sleep(0.1)
    input()
