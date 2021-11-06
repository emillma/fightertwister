from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .fightertwister import FighterTwister


class Button:
    def __init__(self, fightertwister: 'FighterTwister',
                 delay_hold=300,
                 delay_click=200,
                 delay_dbclick=200):

        self.pressed = 0

        self._ft = fightertwister

        self._ts_prev_press = 0
        self._ts_prev_release = 0

        self._delay_hold = delay_hold
        self._delay_click = delay_click
        self._delay_dbclick = delay_dbclick
        self._prev_press_was_dbclick = False

        self._cbs_press = set()
        self._cbs_release = set()
        self._cbs_hold = set()
        self._cbs_click = set()
        self._cbs_slowclick = set()
        self._cbs_dbclick = set()

    def set_delay_hold(self, delay):
        self._delay_hold = delay

    def set_delay_click(self, delay):
        self._delay_click = delay

    def set_delay_dbclick(self, delay):
        self._delay_dbclick = delay

    def register_cb_press(self, callback):
        self._cbs_press.add(callback)

    def register_cb_release(self, callback):
        self._cbs_release.add(callback)

    def register_cb_hold(self, callback):
        def _cb_hold(self: Button, ts_eval):
            if (self.pressed
                    and self._ts_prev_release < ts_eval - self._delay_hold):
                callback(self, ts_eval)
        self._cbs_hold.add(_cb_hold)

    def register_cb_click(self, callback):
        self._cbs_click.add(callback)

    def register_cb_slowclick(self, callback):
        self._cbs_slowclick.add(callback)

    def register_cb_dbclick(self, callback):
        self._cbs_dbclick.add(callback)

    def clear_cbs_button_press(self):
        self._cbs_press.clear()

    def clear_cbs_button_release(self):
        self._cbs_release.clear()

    def clear_cbs_button_hold(self):
        self._cbs_hold.clear()

    def clear_cbs_button_click(self):
        self._cbs_click.clear()

    def clear_cbs_button_slowclick(self):
        self._cbs_slowclick.clear()

    def clear_cbs_button_dbclick(self):
        self._cbs_dbclick.clear()

    def _cb_button_base(self, value, timestamp):
        self.last_sent_button = timestamp
        if value:
            self.pressed = 1
            for cb in self._cbs_press:
                cb(self, timestamp)

            if self._ts_prev_press > timestamp - self._delay_dbclick:
                for cb in self._cbs_dbclick:
                    cb(self, timestamp)
                self._prev_press_was_dbclick = True
            ts_eval_hold = timestamp + self._delay_hold
            for cb in self._cbs_hold:
                self._ft.do_task_at(ts_eval_hold, cb, *[self, ts_eval_hold])

            self._ts_prev_press = timestamp
        else:
            self.pressed = 0
            for cb in self._cbs_release:
                cb(self, timestamp)
            if not self._prev_press_was_dbclick:
                if self._ts_prev_press > timestamp - self._delay_click:
                    for cb in self._cbs_click:
                        cb(self, timestamp)
                else:
                    for cb in self._cbs_slowclick:
                        cb(self, timestamp)
            self._ts_prev_release = timestamp
            self._prev_press_was_dbclick = False
