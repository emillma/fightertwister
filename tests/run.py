import sys
import time
if True:
    sys.path.insert(0, 'src')
from fightertwister import (FighterTwister, Encoder, Button, ft_colors, FtBro,
                            heat_color)


ft = FtBro()
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
    # sb.set_on_off(1)
    input()
