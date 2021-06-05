import sys

if True:
    sys.path.insert(0, 'src')
from fightertwister import (FighterTwister, Encoder, Button, ft_colors, FtBro,
                            heat_color)


# ft = FtBro()
ft = FighterTwister()
sb = Encoder(ft)
ft.encoder_slots[0, :] = sb


with ft:
    input()
