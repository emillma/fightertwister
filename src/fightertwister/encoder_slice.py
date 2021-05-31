import numpy as np
from collections.abc import Iterable
from .encoder import Encoder


class EncoderSlice:
    def __init__(self, encoders: np.ndarray):
        self.encoders = encoders

    def __getitem__(self, indices):
        item = self.encoders[indices]
        if isinstance(item, Encoder):
            return item
        else:
            return EncoderSlice(item)

    def to_iterable(self, value):
        if isinstance(value, Iterable):
            return value
        else:
            return [value]*self.encoders.size

    def toarray(self, iter):
        return np.array(iter).reshape(self.encoders.shape)

    def set_value(self, value):
        return self.toarray(
            [enc.set_value(val)
             for enc, val in zip(self.encoders, self.to_iterable(value))])

    def set_color(self, color):
        """ 0 to 127"""
        return self.toarray(
            [enc.set_color(val)
             for enc, val in zip(self.encoders, self.to_iterable(color))])

    def set_rgb_strobe(self, strobe):
        """ 0 to 8"""
        return self.toarray(
            [enc.set_rgb_strobe(val)
             for enc, val in zip(self.encoders, self.to_iterable(strobe))])

    def set_rgb_pulse(self, pulse):
        """ 0 to 7"""
        return self.toarray(
            [enc.set_rgb_pulse(val)
             for enc, val in zip(self.encoders, self.to_iterable(pulse))])

    def set_rgb_brightnes(self, brightness):
        """ 0. to 1."""
        return self.toarray(
            [enc.set_rgb_brightnes(val)
             for enc, val in zip(self.encoders, self.to_iterable(brightness))])

    def set_indicator_strobe(self, strobe):
        """ 0 to 8"""
        return self.toarray(
            [enc.set_indicator_strobe(val)
             for enc, val in zip(self.encoders, self.to_iterable(strobe))])

    def set_indicator_pulse(self, pulse):
        """ 0 to 8"""
        return self.toarray(
            [enc.set_indicator_pulse(val)
             for enc, val in zip(self.encoders, self.to_iterable(pulse))])

    def set_indicator_brightness(self, brightness):
        """ 0. to 1."""
        return self.toarray(
            [enc.set_indicator_brightness(val)
             for enc, val in zip(self.encoders, self.to_iterable(brightness))])
