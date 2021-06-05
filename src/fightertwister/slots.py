from typing import Iterable
import numpy as np
from fightertwister.button import Button

from fightertwister.encoder import Encoder
from .ftcollections import EncoderCollection, ButtoCollection
from .objectcollection import ObjectCollection


class Slots:
    def __init__(self, objects, addresses):
        self._objects = objects
        self._addresses = addresses
        self._mapping = dict(zip(self._addresses.ravel(),
                                 self._objects.ravel()))

        self._shape = self._objects.shape

    def get_address(self, address):
        return self._mapping[address]

    def __getitem__(self, indices):
        return self._objects[indices]

    def __setitem__(self, indices, items):
        self._objects[indices]


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
        self._encoders[indices]._remove_address[self._addresses[indices]]
        self._encoders[indices] = items
        self._encoders[indices]._add_address[self._addresses[indices]]


class SidebuttonSlots(Slots):
    def __init__(self, sidebuttons):
        super().__init__(sidebuttons,
                         np.arange(8, 32).reshape(4, 2, 3).transpose(0, 2, 1))

    def get_address(self, address) -> Button:
        return super().get_address(address)

    def __getitem__(self, indices) -> Button:
        return super().__getitem__(indices)
