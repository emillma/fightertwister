import numpy as np
from .encoder import Encoder
from .objectcollection import ObjectCollection


class EncoderSlice(ObjectCollection, Encoder):
    def __init__(self, encoders: np.ndarray):
        ObjectCollection.__init__(self, encoders)
        self.encoders = self.objects
