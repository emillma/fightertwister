import numpy as np
from pygame import midi
from .utils import to7bit, clamp
from .button import Button

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .fightertwister import FighterTwister


class Encoder(Button):
    def __init__(self, fightertwister: 'FighterTwister', address,
                 delay_hold=300,
                 delay_click=200,
                 delay_dbclick=200):
        super().__init__(fightertwister,
                         delay_hold, delay_click, delay_dbclick)

        self.on = 1

        self._ft = fightertwister
        self._address = address

        self._value = 0
        self._extra_values = np.empty(0, float)

        self._on_brightness = 1
        self._off_brightness = 0.3

        self._follow_value = True
        self._ts_prev_encoder = 0

        self._cbs_encoder = set()
        self._cbs_on = set(
            [lambda *_: self.set_indicator_brightness(self._on_brightness)])
        self._cbs_off = set(
            [lambda *_: self.set_indicator_brightness(self._off_brightness)])

    @ property
    def value(self):
        return self._value * self.on

    @ property
    def extra_values(self):
        if callable(self._extra_values):
            return self._extra_values()
        else:
            return self._extra_values

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
        self._ts_prev_encoder = timestamp

    def clear_cbs_encoder(self, callback):
        self._cbs_encoder.clear()

    def clear_cbs_on(self, callback):
        self._cbs_on.clear()

    def clear_cbs_off(self, callback):
        self._cbs_off.clear()

    def set_value(self, value):
        self._value = clamp(value, 0, 1)
        if self._follow_value:
            self.show_value(self._value)

    def set_follow_value(self, follow_value):
        self._follow_value = follow_value

    def show_value(self, value):
        self._ft.midi_out.write_short(
            176, self._address, to7bit(clamp(value, 0, 1)))

    def set_extra_values(self, extra_values):
        self._extra_values = extra_values

    def set_on_off(self, on):
        self.on = on
        if self.on:
            for cb in self._cbs_on:
                cb(self, midi.time())
        else:
            for cb in self._cbs_off:
                cb(self, midi.time())

    def set_on_brightness(self, brightenss):
        self.on_brightenss = brightenss

    def set_off_brightness(self, brightenss):
        self.off_brightenss = brightenss

    def set_color(self, color):
        """ 0 to 127"""
        color = int(clamp(color, 0, 127)+0.5)
        self._ft.midi_out.write_short(177, self._address, color)

    def set_rgb_strobe(self, strobe):
        """ 0 to 8"""
        strobe = int(clamp(strobe, 0, 8) + 0 + 0.5)
        self._ft.midi_out.write_short(178, self._address, strobe)

    def set_rgb_pulse(self, pulse):
        """ 0 to 7"""
        pulse = int(clamp(pulse, 0, 7) + 9 + 0.5)
        self._ft.midi_out.write_short(178, self._address, pulse)

    def set_rgb_brightness(self, brightness):
        """ 0. to 1."""
        brightness = int(clamp(brightness, 0, 1)*30+0.5) + 17
        self._ft.midi_out.write_short(178, self._address, brightness)

    def set_indicator_strobe(self, strobe):
        """ 0 to 8"""
        strobe = int(clamp(strobe, 0, 8) + 48 + 0.5)
        self._ft.midi_out.write_short(178, self._address, strobe)

    def set_indicator_pulse(self, pulse):
        """ 0 to 8"""
        pulse = int(clamp(pulse, 0, 8) + 56 + 0.5)
        pulse = pulse if pulse != 56 else 48
        self._ft.midi_out.write_short(178, self._address, pulse)

    def set_indicator_brightness(self, brightness):
        """ 0. to 1."""
        brightness = int(clamp(brightness, 0, 1)*30+0.5) + 65
        self._ft.midi_out.write_short(178, self._address, brightness)
