import numpy as np

from fightertwister.utils import ft_colors

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from fightertwister.knob import Knob

class RGBLight:
    def __init__(self, knob: 'Knob'):
        self.knob = knob
        self._state = 47
        self.color = ft_colors.blue
        
    def set_color(self, color):
        """ 0 to 127"""
        self.color = color
        self.knob._send_midi(177, color)
        
    def set_rgb_strobe(self, strobe):
        """ 0 to 8"""
        self._set_state(int(np.clip(strobe, 0, 8) + 0 + 0.5))

    def set_rgb_pulse(self, pulse):
        """ 0 to 7"""
        self._set_state(int(np.clip(pulse, 0, 7) + 9 + 0.5))

    def set_rgb_brightness(self, brightness):
        """ 0. to 1."""
        self._set_state(int(np.clip(brightness, 0, 1)*30+0.5) + 17)

    def _set_state(self, state):
        self._state = state
        self.knob._send_midi(178, state)
        