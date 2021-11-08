from fightertwister.encoder import Encoder
from fightertwister.button import Button
from fightertwister.rgblight import RGBLight
from fightertwister.indicator import Indicator

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .fightertwister import FighterTwister


class Knob:
    def __init__(self, fightertwister: 'FighterTwister'):
        super().__init__()
        self._ft = fightertwister
        self._addresses = set([])
        
        self.enc = Encoder(self)
        self.set_value = self.enc.set_value
        
        self.but = Button(self)
        self.rgb = RGBLight(self)
        self.ind = Indicator(self)
        
        self._follow_value = True
        
        def follow_cb(enc: Encoder, ts):
            if self._follow_value:
                self.ind.set_value(enc.value)
        self.enc.register_cb(follow_cb)
        
    @ property
    def value(self):
        return self.enc.value
        
    def add_address(self, address):
        self._addresses.add(address)

    def remove_address(self, address):
        self._addresses.remove(address)

    def show(self):
        self.ind.set_value(self.value)
        self.ind._set_state(self.ind._state)
        self.rgb.set_color(self.rgb.color)
        self.rgb._set_state(self.rgb._state)

    def _send_midi(self, channel, message, ts=None):
        for address in self._addresses:
            self._ft._send_midi(channel, address, message, ts)
            
    def __repr__(self):
        return f'Encoder connected to {self._addresses}'
    
    def __str__(self):
        return self.__repr__()
    
    