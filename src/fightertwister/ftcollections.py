from __future__ import annotations
from functools import reduce
import numpy as np
from collections.abc import Iterator
from operator import mul

from .encoder import Encoder
from .button import Button
from .objectcollection import ObjectCollection

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .fightertwister import FighterTwister


class EncoderCollection(ObjectCollection, Encoder):
    def __init__(self, encoders: np.ndarray,
                 fightertwister: FighterTwister = None):

        if isinstance(encoders, tuple) and fightertwister is not None:
            encoders = np.array([Encoder(fightertwister)
                                 for i in range(reduce(mul, encoders))]
                                ).reshape(encoders)

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
