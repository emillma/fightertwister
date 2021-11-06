import numpy as np
from pygame import midi
from collections.abc import Iterable
from copy import copy

from fightertwister.utils import ft_colors, to7bit, clamp

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .fightertwister import FighterTwister


class Encoder:

    def __init__(self, knob):
        self.knob = knob
        self._value = 0
        self._ts_prev_encoder = 0

        self._cbs_encoder = set()

    @ property
    def value(self):
        return self._value * self.on

  



    def set_value(self, value):
        self._value = float(clamp(value, 0, 1))
        if self._follow_value:
            self.show_value(self._value)

    def register_cb_encoder(self, callback):
        self._cbs_encoder.add(callback)

    def clear_cbs_encoder(self, callback):
        self._cbs_encoder.clear()

    def clear_cbs_on(self, callback):
        self._cbs_on.clear()

    def clear_cbs_off(self, callback):
        self._cbs_off.clear()

    def show_value(self, value):
        self._send_midi(176, to7bit(clamp(value, 0, 1)))

    def show_color(self, color):
        message = int(clamp(color, 0, 127)+0.5)
        self._send_midi(177, message)

    def flash_color(self, color, duration=100):
        self.show_color(color)
        self._ft.do_task_delay(
            duration, lambda: self.set_color(self._color))

    def _cb_encoder_base(self, value, timestamp):
        step = (value-64)
        print(self.value)
        self.set_value(round(self._value + step/1000, 4))
        for cb in self._cbs_encoder:
            cb(self, timestamp)
        self._ts_prev_encoder = timestamp

    def _add_address(self, address):
        self._addresses.add(address)

    def _remove_address(self, address):
        self._addresses.remove(address)



