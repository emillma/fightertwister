import sys
import time
if True:
    sys.path.insert(0, 'src')
from fightertwister import (FighterTwister, Encoder, Button, ft_colors,
                            heat_color)
from pygame import midi

ft = FighterTwister()
# ft = FighterTwister()
# ft.sidebuttons.register_cb_press(lambda *_: ft.next_bank())
# sb = Encoder(ft)
# ft.encoder_slots[0, :, 0] = sb

with ft:
    # sb.set_color(ft_colors.cyan)
    # time.sleep(1)
    # ft.encoder_slots[:] = sb
    # for i in range(16):
    #     ft.encoders.ravel()[i].set_color(ft_colors.red)
    #     time.sleep(0.1)
    #     ft.encoders.ravel()[i].set_color(ft_colors.blue)

    # sb.set_color(ft_colors.blue)
    # sb.set_on(1)
    # for i in range(100):
    # print(midi.time())
    # ft.encoder_slots[:].flash_color(ft_colors.red)
    # time.sleep(.01)
    input()
