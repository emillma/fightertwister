import numpy as np
from pygame import midi
from .utils import to7bit, clamp
from .button import Button

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .fightertwister import FighterTwister


class Encoder(Button):
    def __init__(self, fightertwister: 'FighterTwister', idx,
                 delay_hold=400,
                 delay_click=200,
                 delay_dbclick=200):
        super().__init__(fightertwister,
                         delay_hold, delay_click, delay_dbclick)

        self.ft = fightertwister
        self.idx = idx

        self._value = 0
        self.extra_values = np.empty(0, float)
        self.on = 1

        self.ts_prev_encoder = 0
        self._cbs_encoder = set()
        self._cbs_on = set([lambda *_: self.set_indicator_brightness(1)])
        self._cbs_off = set([lambda *_: self.set_indicator_brightness(0.4)])

    @property
    def value(self):
        return self.value * self.on

    def register_cb_encoder(self, callback):
        self._cbs_encoder.add(callback)

    def register_cb_on(self, callback):
        self._cbs_encoder.add(callback)

    def register_cb_off(self, callback):
        self._cbs_encoder.add(callback)

    def _cb_encoder_base(self, value, timestamp):
        self.set_value(round(self._value + (value-64)/1000, 3))
        for cb in self._cbs_encoder:
            cb(self, timestamp)
        self.ts_prev_encoder = timestamp

    def clear_cbs_encoder(self, callback):
        self._cbs_encoder.clear()

    def clear_cbs_on(self, callback):
        self._cbs_on.clear()

    def clear_cbs_off(self, callback):
        self.cbs_off.clear()

    def set_value(self, value):
        self._value = clamp(value, 0, 1)
        self.ft.midi_out.write_short(176, self.idx, to7bit(value))

    def set_extra_values(self, extra_values):
        self.extra_values = extra_values

    def set_on_off(self, on):
        self.on = on
        if self.on:
            for cb in self._cbs_on:
                cb(self, midi.time())
        else:
            for cb in self._cbs_off:
                cb(self, midi.time())

    def set_color(self, color):
        """ 0 to 127"""
        color = int(clamp(color, 0, 127)+0.5)
        self.ft.midi_out.write_short(177, self.idx, color)

    def set_rgb_strobe(self, strobe):
        """ 0 to 8"""
        strobe = int(clamp(strobe, 0, 8) + 0 + 0.5)
        self.ft.midi_out.write_short(178, self.idx, strobe)

    def set_rgb_pulse(self, pulse):
        """ 0 to 7"""
        pulse = int(clamp(pulse, 0, 7) + 9 + 0.5)
        self.ft.midi_out.write_short(178, self.idx, pulse)

    def set_rgb_brightness(self, brightness):
        """ 0. to 1."""
        brightness = int(clamp(brightness, 0, 1)*30+0.5) + 17
        self.ft.midi_out.write_short(178, self.idx, brightness)

    def set_indicator_strobe(self, strobe):
        """ 0 to 8"""
        strobe = int(clamp(strobe, 0, 8) + 48 + 0.5)
        self.ft.midi_out.write_short(178, self.idx, strobe)

    def set_indicator_pulse(self, pulse):
        """ 0 to 8"""
        pulse = int(clamp(pulse, 0, 8) + 56 + 0.5)
        pulse = pulse if pulse != 56 else 48
        self.ft.midi_out.write_short(178, self.idx, pulse)

    def set_indicator_brightness(self, brightness):
        """ 0. to 1."""
        brightness = int(clamp(brightness, 0, 1)*30+0.5) + 65
        self.ft.midi_out.write_short(178, self.idx, brightness)
