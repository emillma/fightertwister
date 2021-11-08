import numpy as np
from fightertwister.button import Button
from fightertwister.knob import Knob
from fightertwister.ftcollections import KnobCollection, ButtoCollection


class KnobSlots:
    def __init__(self, encoders: KnobCollection):
        self._encoders = encoders
        self._addresses = np.arange(64).reshape(4, 4, 4)
        self._mapping = dict(zip(self._addresses.ravel(),
                                 self._encoders.ravel()))
        self._encoders.add_address(self._addresses)

    def get_address(self, address) -> Knob:
        return self._mapping[address]

    def __getitem__(self, indices) -> Knob:
        return self._encoders[indices]

    def __setitem__(self, indices, items):
        self._encoders[indices].remove_address(self._addresses[indices])
        self._encoders[indices] = items
        self._encoders[indices].add_address(self._addresses[indices])
        self._mapping = dict(zip(self._addresses.ravel(),
                                 self._encoders.ravel()))
        done = set()
        for encoder in self._encoders[indices]:
            if encoder not in done:
                encoder.show()
            done.add(encoder)


class SidebuttonSlots:
    def __init__(self, sidebuttons: ButtoCollection):
        self._sidebuttons = sidebuttons
        self._addresses = np.arange(8, 32).reshape(4, 2, 3).transpose(0, 2, 1)
        self._mapping = dict(zip(self._addresses.ravel(),
                                 self._sidebuttons.ravel()))

    def get_address(self, address) -> Button:
        return self._mapping[address]

    def __getitem__(self, indices) -> Button:
        return self._sidebuttons[indices]

    def __setitem__(self, indices, items):
        self._sidebuttons[indices] = items
