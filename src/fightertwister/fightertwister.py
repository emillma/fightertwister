from pygame import midi
import time
import threading
from .encoder import Encoder


class FighterTwister:
    def __init__(self):
        self.knobs = [Encoder(self, i) for i in range(64)]

        self.stop = False
        self.prev_timestamp = 0

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
            self.knobs[message[1]].callback_encoder_base(message[2], timestamp)
        if status == 177:
            self.knobs[message[1]].callback_switch_base(message[2], timestamp)

    def loop(self):
        while not self.stop:
            data = []
            while self.midi_in.poll():
                message, timestamp = self.midi_in.read(1)[0]
                data.append([message, timestamp])

            for message, timestamp in data:
                self.parse_input(message, timestamp)
            time.sleep(0.01)

    def run(self):
        self.thread = threading.Thread(target=self.loop)
        self.thread.start()


if __name__ == '__main__':
    ft = FighterTwister()
    with ft:
        input()
