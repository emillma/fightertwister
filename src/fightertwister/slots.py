from typing import Iterable
import numpy as np
from fightertwister.button import Button

from fightertwister.encoder import Encoder
from .ftcollections import EncoderCollection, ButtoCollection
from .objectcollection import ObjectCollection


class EncoderSlots:
    def __init__(self, encoders: EncoderCollection):
        self._encoders = encoders
        self._addresses = np.arange(64).reshape(4, 4, 4)
        self._mapping = dict(zip(self._addresses.ravel(),
                                 self._encoders.ravel()))
        self._encoders._add_address(self._addresses)

    def get_address(self, address) -> Encoder:
        return self._mapping[address]

    def __getitem__(self, indices) -> Encoder:
        return self._encoders[indices]

    def __setitem__(self, indices, items):
        self._encoders[indices]._remove_address(self._addresses[indices])
        self._encoders[indices] = items
        self._encoders[indices]._add_address(self._addresses[indices])
        self._mapping = dict(zip(self._addresses.ravel(),
                                 self._encoders.ravel()))
        done = set()
        for encoder in self._encoders[indices]:
            if encoder not in done:
                encoder._show_properties()
            done.add(encoder)


class SidebuttonSlots:
    def __init__(self, sidebuttons):
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
