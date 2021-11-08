import numpy as np
from fightertwister.utils import to7bit

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from fightertwister.knob import Knob

class Indicator:
    def __init__(self, knob: 'Knob'):
        self.knob = knob
        self._state = 95
        self.indicator_value = 0
        
    def set_strobe(self, strobe):
        """ 0 to 8"""
        self._set_state(int(np.clip(strobe, 0, 8) + 48 + 0.5))

    def set_pulse(self, pulse):
        """ 0 to 8"""
        state = int(np.clip(pulse, 0, 8) + 56 + 0.5)
        state = state if state != 56 else 48
        self._set_state(state)

    def set_brightness(self, brightness):
        """ 0. to 1."""
        self._set_state(int(np.clip(brightness, 0, 1)*30+0.5) + 65)

    def set_value(self, value):
        self.indicator_value = value
        self.knob._send_midi(176, to7bit(np.clip(value, 0, 1)))    

    def _set_state(self, state):
        self.knob._send_midi(178, state)
        self._state = state
