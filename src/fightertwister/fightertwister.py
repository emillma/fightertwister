from pygame import midi
import time
import bisect
import numpy as np
import threading
from sortedcontainers import SortedKeyList
from .encoder import Encoder
from .encoder_slice import EncoderSlice
from .utils import Task


class FighterTwister:
    def __init__(self):
        self.encoders = EncoderSlice(
            np.array([Encoder(self, i) for i in range(64)]))

        self.stop = False
        self.prev_timestamp = 0
        self.queue = SortedKeyList([], key=lambda x: x.timestamp)

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

    def parse_input(self, message, timestamp):
        status = message[0]
        if status == 176:
            self.encoders[message[1]]._cb_encoder_base(
                message[2], timestamp)
        if status == 177:
            self.encoders[message[1]]._cb_switch_base(
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
