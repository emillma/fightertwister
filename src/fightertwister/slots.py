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
        if isinstance(items, ObjectCollection):
            self._objects[indices] = items._objects
        else:
            self._objects[indices] = items

        self._mapping = dict(zip(self._addresses.ravel(),
                                 self._objects.ravel()))


class EncoderSlots(Slots):
    def __init__(self, objects=None):
        super().__init__(np.empty((4, 4, 4), object),
                         np.arange(64).reshape(4, 4, 4))
        if objects:
            self._objects = objects

    def get_address(self, address) -> Encoder:
        return super().get_address(address)

    def __getitem__(self, indices) -> Encoder:
        return super().__getitem__(indices)

    def __setitem__(self, indices, items):
        iterator = zip(self._objects[indices].ravel(),
                       self._addresses[indices].ravel())
        for object, address in iterator:
            if isinstance(object, Encoder):
                object._addresses.remove(address)

        super().__setitem__(indices, items)

        iterator = zip(self._objects[indices].ravel(),
                       self._addresses[indices].ravel())
        for object, address in iterator:
            if isinstance(object, Encoder):
                object._addresses.add(address)


class SidebuttonSlots(Slots):
    def __init__(self, objects=None):
        super().__init__(np.empty((4, 3, 2), object),
                         np.arange(24).reshape(4, 2, 3).transpose(0, 2, 1))
        if objects:
            self._objects = objects

    def get_address(self, address) -> Button:
        return super().get_address(address)

    def __getitem__(self, indices) -> Button:
        return super().__getitem__(indices)
