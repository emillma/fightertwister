import numpy as np
import inspect
from collections.abc import Iterable
from .encoder import Encoder


class EncoderSlice:
    def __init__(self, encoders: np.ndarray):
        self.encoders = encoders
        self.shape = self.encoders.shape

    def __getitem__(self, indices):
        item = self.encoders[indices]
        if isinstance(item, Encoder):
            return item
        else:
            return EncoderSlice(item)

    def to_iterable(self, value):
        if isinstance(value, Iterable):
            return value
        else:
            return [value]*self.encoders.size

    def toarray(self, iter):
        return np.array(iter).reshape(self.encoders.shape)

    def __getattribute__(self, name: str):
        if (hasattr(Encoder, name) and callable(getattr(Encoder, name))
                and num_params(getattr(Encoder, name)) == 2):

            def multicall(param):

                params = self.to_iterable(param)
                for enc, param in zip(self.encoders, params):
                    getattr(enc, name)(param)
            return multicall
        else:
            return object.__getattribute__(self, name)


def num_params(callable):
    return len(inspect.signature(callable).parameters)
