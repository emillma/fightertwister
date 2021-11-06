import numpy as np

from fightertwister.utils import ft_colors

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ... #TODO

class RGBLight:
    def __init__(self, knob):
        self.knob = knob
        self.state = 47
        self.color = ft_colors.blue
        
    def set_color(self, color):
        """ 0 to 127"""
        self.color = color
        self.knob.ft._send_midi(177, color)
        
    def set_rgb_strobe(self, strobe):
        """ 0 to 8"""
        self.set_rgb_state(int(np.clip(strobe, 0, 8) + 0 + 0.5))

    def set_rgb_pulse(self, pulse):
        """ 0 to 7"""
        self.set_rgb_state(int(np.clip(pulse, 0, 7) + 9 + 0.5))

    def set_rgb_brightness(self, brightness):
        """ 0. to 1."""
        self.set_rgb_state(int(np.clip(brightness, 0, 1)*30+0.5) + 17)

    def set_rgb_state(self, state):
        self.state = state
        self.knob.ft._send_midi(178, state)
        