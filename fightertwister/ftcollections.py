from __future__ import annotations
from functools import reduce
import numpy as np
from collections.abc import Iterator
from operator import mul

from fightertwister.encoder import Encoder
from fightertwister.button import Button
from fightertwister.objectcollection import ObjectCollection
from fightertwister.knob import Knob

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .fightertwister import FighterTwister


class KnobCollection(ObjectCollection, Knob):
    def __init__(self, knobs: np.ndarray):
        ObjectCollection.__init__(self, knobs)

    def __getitem__(self, indices) -> KnobCollection:
        return super().__getitem__(indices)

    def __iter__(self) -> Iterator[KnobCollection]:
        return super().__iter__()
    
    @staticmethod
    def from_shape(shape, ft: FighterTwister):
        knobs = np.array([Knob(ft) for i in range(reduce(mul, shape))]
                         ).reshape(shape)
        return KnobCollection(knobs)
    
class ButtoCollection(ObjectCollection, Button):
    def __init__(self, buttons: np.ndarray):
        ObjectCollection.__init__(self, buttons)

    def __getitem__(self, indices) -> ButtoCollection:
        return super().__getitem__(indices)

    def __iter__(self) -> Iterator[ButtoCollection]:
        return super().__iter__()

    @staticmethod
    def from_shape(shape, ft: FighterTwister):
        buttons = np.array([Knob(ft) for i in range(reduce(mul, shape))]
                         ).reshape(shape)
        return ButtoCollection(buttons)