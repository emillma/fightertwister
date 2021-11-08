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
        self.value = 0
        self._ts_prev_encoder = 0
        self._cbs_encoder = set()

    def set_value(self, value):
        self.value = float(np.clip(value, 0, 1))

    def register_cb(self, callback):
        self._cbs_encoder.add(callback)

    def clear_cbs_encoder(self, callback):
        self._cbs_encoder.clear()

    def _cb_encoder_base(self, value, timestamp):
        step = (value-64)
        self.set_value(round(self.value + step/100, 4))
        for cb in self._cbs_encoder:
            cb(self, timestamp)
        self._ts_prev_encoder = timestamp



