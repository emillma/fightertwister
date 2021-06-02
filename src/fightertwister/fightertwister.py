from pygame import midi
import time
import bisect
import numpy as np
import threading
from sortedcontainers import SortedKeyList
from .encoder import Encoder
from .button import Button
from .ftcollections import EncoderCollection, ButtoCollection
from .utils import Task


class FighterTwister:
    def __init__(self):
        encoders = np.array([Encoder(self, i) for i in range(64)])
        self.encoders = EncoderCollection(encoders.reshape(4, 4, 4))

        sidebuttons = np.array([Button(self) for i in range(8, 32)])
        self.sidebuttons = ButtoCollection(sidebuttons.reshape(4, 3, 2))
        self.current_bank = 0
        self.queue = SortedKeyList([], key=lambda x: x.timestamp)
        self.stop = False

    def __enter__(self):
        midi.init()
        self.midi_in = midi.Input(1, buffer_size=256)
        self.midi_out = midi.Output(3, buffer_size=256, latency=1)
        self.run()

    def __exit__(self, type, value, traceback):
        self.stop = True
        self.thread.join()
        self.midi_in.close()
        self.midi_out.close()
        midi.quit()

    def set_bank(self, bank):
        self.current_bank = bank
        # self.midi_out.write_short(179, self.current_bank, 127)
        self.midi_out.write_short(179, self.current_bank, 127)

    def next_bank(self):
        self.set_bank((self.current_bank+1) % 4)

    def prev_bank(self):
        self.set_bank((self.current_bank-1) % 4)

    def parse_input(self, message, timestamp):
        # print(message)
        status = message[0]
        if status == 176:
            enc_idx = np.unravel_index(message[1], self.encoders.shape)
            self.encoders[enc_idx]._cb_encoder_base(
                message[2], timestamp)

        if status == 177:
            enc_idx = np.unravel_index(message[1], self.encoders.shape)
            self.encoders[enc_idx]._cb_button_base(
                message[2], timestamp)

        if status == 179:
            enc_idx = np.unravel_index(message[1]-8, (4, 2, 3))
            enc_idx = (enc_idx[0], enc_idx[2], enc_idx[1])
            self.sidebuttons[enc_idx]._cb_button_base(
                message[2], timestamp)

    def add_task_at(self, timestamp, function, args=[], kwargs={}):
        task = Task(timestamp, function, args, kwargs)
        self.queue.add(task)

    def add_task_delay(self, delay, function, args=[], kwargs={}):
        self.add_task_at(midi.time()+delay, function, args, kwargs)

    def loop(self):
        while not self.stop:
            while self.midi_in.poll():
                message, timestamp = self.midi_in.read(1)[0]
                self.add_task_at(timestamp, self.parse_input,
                                 [message, timestamp])

            while self.queue and self.queue[0].timestamp < midi.time():
                task = self.queue.pop(0)
                task.execute()

            time.sleep(0.01)

    def run(self):
        self.thread = threading.Thread(target=self.loop)
        self.thread.start()
