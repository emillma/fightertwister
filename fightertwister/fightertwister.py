from pygame import midi
import time
import numpy as np
import threading
from sortedcontainers import SortedKeyList
from .ftcollections import KnobCollection, ButtoCollection
from .encoder import Encoder
from .button import Button
from .utils import Task
from .slots import KnobSlots, SidebuttonSlots


class FighterTwister:
    def __init__(self):

        self.knobs = KnobCollection.from_shape((4, 4, 4), self)
        self.knob_slots = KnobSlots(self.knobs)

        self.sidebuttons = ButtoCollection.from_shape((4,3,2), self)
        self.sidebutton_slots = SidebuttonSlots(self.sidebuttons)

        self.current_bank = 0

        self._check_connection_delay = 1000
        self._connected = False
        self._running = False
        self._midi_in = None
        self._midi_out = None

        self._queue = SortedKeyList([], key=lambda x: x.timestamp)
        self._stop = False
        self._last_input = 0

    def __enter__(self):
        midi.init()
        self.try_connect()
        self.run()

    def __exit__(self, type, value, traceback):
        self._stop = True
        self._connected = False
        self.thread.join()
        self._midi_in.close()
        self._midi_out.close()
        midi.quit()

    def try_connect(self):
        if self._connected:
            return -1
        midi_objs = [(i, *midi.get_device_info(i))
                     for i in range(midi.get_count())]
        ft_in = [mo for mo in midi_objs if mo[2] == b'Midi Fighter Twister'
                 and mo[3]]
        ft_out = [mo for mo in midi_objs if mo[2] == b'Midi Fighter Twister'
                  and mo[4]]
        if ft_in and ft_out:
            self._midi_in = midi.Input(ft_in[0][0], buffer_size=256)
            self._midi_out = midi.Output(
                ft_out[0][0], buffer_size=256, latency=1)
            self._connected = True
            self.set_bank(self.current_bank)
            return -1

    def set_bank(self, bank):
        self.current_bank = bank
        done = set()
        for encoder in self.knob_slots[bank]:
            if encoder not in done:
                encoder.show()
            done.add(encoder)
        self._midi_out.write_short(179, self.current_bank, 127)

    def next_bank(self):
        self.set_bank((self.current_bank+1) % 4)

    def prev_bank(self):
        self.set_bank((self.current_bank-1) % 4)

    def parse_input(self, message, timestamp):
        self._last_input = timestamp
        status = message[0]
        if status == 176:
            self.knob_slots.get_address(message[1]).enc._cb_encoder_base(
                message[2], timestamp)

        elif status == 177:
            self.knob_slots.get_address(message[1]).but._cb_button_base(
                message[2], timestamp)

        elif status == 179:
            self.sidebutton_slots.get_address(message[1])._cb_button_base(
                message[2], timestamp)
        else:
            print(message)

    def do_task_at(self, timestamp, function, *args, **kwargs):
        task = Task(timestamp, function, args, kwargs)
        self._queue.add(task)

    def do_task_delay(self, delay, function, *args, **kwargs):
        now = midi.time() if midi.get_init() else 0
        self.do_task_at(now+delay, function, *args, **kwargs)
        
    def _send_midi(self, channel, address, message, timestamp=None):
        if self._midi_out is None or not midi.get_init():
            return
        try:
            if address//16 != self.current_bank:  # skip if not visible
                return
            if timestamp is None:
                self._midi_out.write_short(channel, address, message)
            else:
                self._midi_out.write(
                    [[channel, address, message], timestamp])
        except midi.MidiException:
            pass
            
    def loop(self):
        """
        TODO: set rate limit, rgb and indicator brightness
        """
        while not self._stop:
            while self._connected and self._midi_in.poll():
                message, timestamp = self._midi_in.read(1)[0]
                self.do_task_at(timestamp, self.parse_input,
                                *[message, timestamp])
            while self._queue and self._queue[0].timestamp < midi.time():
                task = self._queue.pop(0)
                task.execute()

            if midi.time() - self._last_input > 20000:
                self._last_input = midi.time()
                midi.quit()
                midi.init()
                # print(midi.time())
                self._connected = False
                self._midi_in.close()
                self._midi_out.close()
                self.try_connect()
                if not self._connected:
                    time.sleep(20)
            # Store messages and parse them here
            time.sleep(0.01)

    def run(self):
        self._running = True
        self.thread = threading.Thread(target=self.loop)
        self.thread.start()
