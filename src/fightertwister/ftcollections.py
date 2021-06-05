from __future__ import annotations
import numpy as np
from collections.abc import Iterator

from .encoder import Encoder
from .button import Button
from .objectcollection import ObjectCollection


class EncoderCollection(ObjectCollection, Encoder):
    def __init__(self, encoders: np.ndarray):
        ObjectCollection.__init__(self, encoders)

    def __getitem__(self, indices) -> EncoderCollection:
        return super().__getitem__(indices)

    def __iter__(self) -> Iterator[EncoderCollection]:
        return super().__iter__()


class ButtoCollection(ObjectCollection, Button):
    def __init__(self, buttons: np.ndarray):
        ObjectCollection.__init__(self, buttons)

    def __getitem__(self, indices) -> ButtoCollection:
        return super().__getitem__(indices)

    def __iter__(self) -> Iterator[ButtoCollection]:
        return super().__iter__()
