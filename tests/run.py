from fightertwister import (FighterTwister, Encoder, Button, ft_colors,
                            heat_color)
from pygame import midi

ft = FighterTwister()
# ft = FighterTwister()
# ft.sidebuttons.register_cb_press(lambda *_: ft.next_bank())
# sb = Encoder(ft)
# ft.encoder_slots[0, :, 0] = sb

with ft:
    input('enter to quit')
