import numpy as np
import sys
if True:
    sys.path.insert(0, 'src')
from fightertwister import FighterTwister, Encoder, Button, ft_colors, FtBro

ft = FtBro()


def show_encoder_pos(self: Encoder, timesamp):
    print(ft.encoders.get_idx(self))


def show_sidebutton_pos(self: Encoder, timesamp):
    print(ft.sidebuttons.get_idx(self))


ft.encoders.register_cb_press(show_encoder_pos)
ft.sidebuttons.register_cb_press(show_sidebutton_pos)
with ft:
    ft.encoders.set_value(0)
    ft.encoders.set_color(np.array([[np.linspace(1, 126, 4)]]).T)
    input()
