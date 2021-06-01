
from .utils import to7bit, clamp
from pygame import midi


class Encoder:
    def __init__(self, fightertwister, idx):
        self.ft = fightertwister
        self.idx = idx
        self.pressed = 0
        self.value = 0

        self.ts_prev_encoder = 0
        self.ts_prev_press = 0
        self.ts_prev_release = 0

        self._cb_encoder = lambda self, timestamp: None
        self._cb_switch_release = lambda selfcoder, timestamp: None
        self._cb_switch_press = lambda self, timestamp: None

        self._delay_hold = 500
        self._delay_click = 200
        self._delay_dbclick = 300
        self._cb_hold = lambda self, ts_eval: None
        self._cb_click = lambda self, ts_eval: None
        self._cb_dbclick = lambda self, ts_eval: None

    def register_cb_encoder(self, callback):
        self.encoder_cb = callback

    def register_cb_switch_release(self, callback):
        self._cb_switch_release = callback

    def register_cb_switch_press(self, callback):
        self._cb_switch_press = callback

    def register_cb_hold(self, callback):
        def _cb_hold(self, ts_eval):
            if (self.pressed
                    and self.ts_prev_release < ts_eval - self._delay_hold):
                callback(self)
        self._cb_hold = _cb_hold

    def register_cb_click(self, callback):
        self._cb_click = callback

    def register_cb_dbclick(self, callback):
        self._cb_dbclick = callback

    def _cb_encoder_base(self, value, timestamp):
        self.set_value(self.value + (value-64)/1000)
        self._cb_encoder(self, timestamp)
        self.ts_prev_encoder = timestamp

    def _cb_switch_base(self, value, timestamp):
        self.last_sent_switch = timestamp
        if value:
            self.pressed = 1
            self._cb_switch_press(self, timestamp)

            if self.ts_prev_press > timestamp - self._delay_dbclick:
                self._cb_dbclick(self, timestamp)

            ts_eval_hold = timestamp + self._delay_hold
            self.ft.add_task_at(ts_eval_hold, self._cb_hold,
                                [self, ts_eval_hold])

            self.ts_prev_press = timestamp
        else:
            self.pressed = 0
            self._cb_switch_release(self, timestamp)
            if self.ts_prev_press > timestamp - self._delay_click:
                self._cb_click(self, timestamp)

            self.ts_prev_release = timestamp

    def set_value(self, value):
        self.value = clamp(value, 0, 1)
        self.ft.midi_out.write_short(176, self.idx, to7bit(value))

    def set_on(self, value):
        self.pressed = 1 if value else 0

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
