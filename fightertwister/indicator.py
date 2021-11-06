import numpy as np
from fightertwister.utils import to7bit

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    ... #TODO

class Indicator:
    def __init__(self, knob):
        self.knob = knob
        self.state = 95
        self.value = 0
        
    def set_indicator_strobe(self, strobe):
        """ 0 to 8"""
        self._set_indicator_state(int(np.clip(strobe, 0, 8) + 48 + 0.5))

    def set_indicator_pulse(self, pulse):
        """ 0 to 8"""
        state = int(np.clip(pulse, 0, 8) + 56 + 0.5)
        state = state if state != 56 else 48
        self._set_indicator_state(state)

    def set_indicator_brightness(self, brightness):
        """ 0. to 1."""
        self._set_indicator_state(int(np.clip(brightness, 0, 1)*30+0.5) + 65)

    def _set_indicator_state(self, state):
        self.knob.ft._send_midi(178, state)
        self.state = state

    def show_value(self, value):
        self.value
        self.knob.ft._send_midi(176, to7bit(np.clip(value, 0, 1)))    

