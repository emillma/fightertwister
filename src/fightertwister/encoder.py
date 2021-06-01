
from .utils import to7bit, clamp


class Encoder:
    def __init__(self, fightertwister, idx):
        self.ft = fightertwister
        self.idx = idx
        self.pressed = 0
        self.value = 0

        self.ts_prev_encoder = 0
        self.ts_prev_on = 0
        self.ts_prev_off = 0

        self.cb_encoder = lambda self, timestamp: None
        self.cb_switch_off = lambda selfcoder, timestamp: None
        self.cb_switch_on = lambda self, timestamp: None

    def register_cb_encoder(self, encoder_cb):
        self.encoder_cb = encoder_cb

    def register_cb_switch_off(self, switch_off_cb):
        self.cb_switch_off = switch_off_cb

    def register_cb_switch_on(self, switch_on_cb):
        self.cb_switch_on = switch_on_cb

    def cb_encoder_base(self, value, timestamp):
        self.set_value(self.value + (value-64)/1000)
        self.cb_encoder(self, timestamp)
        self.ts_prev_encoder = timestamp

    def cb_switch_base(self, value, timestamp):
        self.last_sent_switch = timestamp
        if value:
            self.pressed = 1
            self.cb_switch_on(self, timestamp)
            self.ts_prev_on = timestamp
        else:
            self.pressed = 0
            self.cb_switch_off(self, timestamp)
            self.ts_prev_off = timestamp

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
