class Button:
    def __init__(self, fightertwister,
                 delay_hold=500,
                 delay_click=200,
                 delay_dbclick=300):
        self.ft = fightertwister
        self.pressed = 0

        self.ts_prev_press = 0
        self.ts_prev_release = 0
        self._delay_hold = delay_hold
        self._delay_click = delay_click
        self._delay_dbclick = delay_dbclick

        self._cb_button_press = lambda self, timestamp: None
        self._cb_button_release = lambda selfcoder, timestamp: None

        self._cb_hold = lambda self, ts_eval: None

        self._cb_click = lambda self, ts_eval: None
        self._cb_slowclick = lambda self, ts_eval: None

        self._cb_dbclick = lambda self, ts_eval: None

    def register_cb_encoder(self, callback):
        self.encoder_cb = callback

    def register_cb_button_press(self, callback):
        self._cb_button_press = callback

    def register_cb_button_release(self, callback):
        self._cb_button_release = callback

    def register_cb_hold(self, callback):
        def _cb_hold(self, ts_eval):
            if (self.pressed
                    and self.ts_prev_release < ts_eval - self._delay_hold):
                callback(self)
        self._cb_hold = _cb_hold

    def register_cb_click(self, callback):
        self._cb_click = callback

    def register_cb_slowclick(self, callback):
        self._cb_slowclick = callback

    def register_cb_dbclick(self, callback):
        self._cb_dbclick = callback

    def _cb_button_base(self, value, timestamp):
        self.last_sent_button = timestamp
        if value:
            self.pressed = 1
            self._cb_button_press(self, timestamp)

            if self.ts_prev_press > timestamp - self._delay_dbclick:
                self._cb_dbclick(self, timestamp)

            ts_eval_hold = timestamp + self._delay_hold
            self.ft.add_task_at(ts_eval_hold, self._cb_hold,
                                [self, ts_eval_hold])

            self.ts_prev_press = timestamp
        else:
            self.pressed = 0
            self._cb_button_release(self, timestamp)
            if self.ts_prev_press > timestamp - self._delay_click:
                self._cb_click(self, timestamp)
            else:
                self._cb_slowclick(self, timestamp)
            self.ts_prev_release = timestamp
