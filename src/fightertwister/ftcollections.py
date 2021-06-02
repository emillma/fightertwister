import numpy as np
from .encoder import Encoder
from .button import Button
from .objectcollection import ObjectCollection


class EncoderCollection(ObjectCollection, Encoder):
    def __init__(self, encoders: np.ndarray):
        ObjectCollection.__init__(self, encoders)


class ButtoCollection(ObjectCollection, Button):
    def __init__(self, buttons: np.ndarray):
        ObjectCollection.__init__(self, buttons)
