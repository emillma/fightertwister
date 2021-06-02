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
        self.value = 0
        self.ts_prev_encoder = 0

        self._cbs_encoder = set()

    def register_cb_encoder(self, callback):
        self._cbs_encoder.add(callback)

    def _cb_encoder_base(self, value, timestamp):
        self.set_value(round(self.value + (value-64)/1000, 3))
        for cb in self._cbs_encoder:
            cb(self, timestamp)
        self.ts_prev_encoder = timestamp

    def clear_cbs_encoder(self, callback):
        self._cbs_encoder.clear()

    def set_value(self, value):
        self.value = clamp(value, 0, 1)
        self.ft.midi_out.write_short(176, self.idx, to7bit(value))

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
