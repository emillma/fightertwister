import numpy as np
import sys
import time
if True:
    sys.path.insert(0, 'src')
from fightertwister import FighterTwister


ft = FighterTwister()
layer1 = ft.encoders[:16]
with ft:
    ft.encoders.set_value(0)
    values = np.zeros(64)
    for i in range(1000):
        values = (values + 10*np.random.random(64)) % 127
        ft.encoders.set_color(values)
        time.sleep(0.1)
    input()
