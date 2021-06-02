import sys

if True:
    sys.path.insert(0, 'src')
from fightertwister import (FighterTwister, Encoder, Button, ft_colors, FtBro,
                            heat_color)


ft = FtBro()
# ft = FighterTwister()
with ft:
    input()
