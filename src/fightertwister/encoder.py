import numpy as np
from pygame import midi
from collections.abc import Iterable
from copy import copy

from .utils import ft_colors, to7bit, clamp
from .button import Button

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .fightertwister import FighterTwister


class Encoder(Button):

    def __init__(self, fightertwister: 'FighterTwister',
                 on_brightness=1,
                 off_brightness=0.3,
                 delay_hold=250,
                 delay_click=200,
                 delay_dbclick=200):
        super().__init__(fightertwister,
                         delay_hold, delay_click, delay_dbclick)

        self._ft = fightertwister

        self._addresses = set([])

        self._default_color = ft_colors.blue

        self._follow_value = True
        self._on_brightness = on_brightness
        self._off_brightness = off_brightness
        self._on = 1

        self._value = 0
        self._color = 1
        self._rgb_strobe = 0
        self._rgb_pulse = 0
        self._rgb_brightness = 1
        self._indicator_strobe = 0
        self._indicator_pulse = 0
        self._indicator_brightness = 1
        self._state = 0

        self._rgb_state = 47
        self._indicator_state = 95

        self._properties = dict()
        self._visible_property_keys = set([
            '_value', '_color', '_rgb_strobe', '_rgb_pulse', '_rgb_brightness',
            '_indicator_strobe', '_indicator_pulse', '_indicator_brightness'])

        self._setable_propery_keys = set([key[3:] for key in dir(self)
                                          if callable(getattr(self, key))
                                          and key.startswith('set_')
                                          and key[3:] in vars(self)])

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
    def on(self):
        return self._on

    def set_property(self, key, value):
        self._properties[key] = value

    def set_state(self, state):
        self._state = state

    def get_property(self, key):
        return self._properties.get(key)

    def set_value(self, value):
        self._value = float(clamp(value, 0, 1))
        if self._follow_value:
            self.show_value(self._value)

    def set_follow_value(self, follow_value):
        self._follow_value = bool(follow_value)

    def set_extra_values(self, extra_values):
        self._extra_values = extra_values

    def set_on(self, on):
        self._on = on
        if self.on:
            for cb in self._cbs_on:
                cb(self, midi.time() if midi.get_init() else 0)
        else:
            for cb in self._cbs_off:
                cb(self, midi.time() if midi.get_init() else 0)

    def set_on_brightness(self, brightenss):
        self._on_brightness = float(brightenss)

    def set_off_brightness(self, brightenss):
        self._off_brightness = float(brightenss)

    def set_color(self, color):
        self._color = int(color)
        """ 0 to 127"""
        self.show_color(color)

    def set_default_color(self, color, show=False):
        self._default_color = int(color)
        if show:
            self.set_color(color)

    def set_rgb_strobe(self, strobe):
        self._rgb_strobe = strobe
        self._rgb_pulse = 0
        """ 0 to 8"""
        message = int(clamp(strobe, 0, 8) + 0 + 0.5)
        self._send_midi(178, message)
        self._rgb_state = message

    def set_rgb_pulse(self, pulse):
        self._rgb_pulse = pulse
        self._rgb_strobe = 0
        """ 0 to 7"""
        message = int(clamp(pulse, 0, 7) + 9 + 0.5)
        self._send_midi(178, message)
        self._rgb_state = message

    def set_rgb_brightness(self, brightness):
        self._rgb_brightness = brightness
        """ 0. to 1."""
        message = int(clamp(brightness, 0, 1)*30+0.5) + 17
        self._send_midi(178, message)
        self._rgb_state = message

    def set_indicator_strobe(self, strobe):
        self._indicator_strobe = strobe
        self._indicator_pulse = 0
        """ 0 to 8"""
        message = int(clamp(strobe, 0, 8) + 48 + 0.5)
        self._send_midi(178, message)
        self._indicator_state = message

    def set_indicator_pulse(self, pulse):
        """ 0 to 8"""
        self._indicator_pulse = pulse
        message = int(clamp(pulse, 0, 8) + 56 + 0.5)
        message = message if message != 56 else 48
        self._send_midi(178, message)
        self._indicator_state = message

    def set_indicator_brightness(self, brightness):
        """ 0. to 1."""
        self._indicator_brightness = brightness
        message = int(clamp(brightness, 0, 1)*30+0.5) + 65
        self._send_midi(178, message)
        self._indicator_state = message

    def register_cb_encoder(self, callback):
        self._cbs_encoder.add(callback)

    def register_cb_on(self, callback):
        self._cbs_encoder.add(callback)

    def register_cb_off(self, callback):
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
        self.set_value(round(self._value + (value-64)/1000, 3))
        for cb in self._cbs_encoder:
            cb(self, timestamp)
        self._ts_prev_encoder = timestamp

    def _send_midi(self, channel, message, timestamp=None):
        if self._ft._midi_out is None or not midi.get_init():
            return
        for address in self._addresses or []:
            # print(address//16)
            if address//16 != self._ft.current_bank:  # skip stuff not visible
                continue
            if timestamp is None:
                self._ft._midi_out.write_short(channel, address, message)
            else:
                self._ft._midi_out.write(
                    [[channel, address, message], timestamp])

    def _add_address(self, address):
        self._addresses.add(address)

    def _remove_address(self, address):
        self._addresses.remove(address)

    def _show_properties(self):
        self.show_value(self._value)
        self.show_color(self._color)

        self._send_midi(178, self._rgb_state)
        self._send_midi(178, self._indicator_state)

    def copy(self):
        output = Encoder(self._ft)
        for key in vars(self):
            if key not in ['_ft', '_addresses']:
                setattr(output, key, copy(getattr(self, key)))
        return output

    def __repr__(self):
        return f'Encoder connected to {self._addresses}'
