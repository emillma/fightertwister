import numpy as np
import inspect
from collections.abc import Iterable
from .encoder import Encoder


def num_params(callable):
    return len(inspect.signature(callable).parameters)


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

    def toarray(self, iter):
        return np.array(iter).reshape(self.encoders.shape)

    def __getattribute__(self, name: str):
        if (hasattr(Encoder, name) and callable(getattr(Encoder, name))
                and num_params(getattr(Encoder, name)) == 2):

            def multicall(param):
                encoders, params = np.broadcast_arrays(self.encoders, param)
                for enc, param in zip(encoders.ravel(), params.ravel()):
                    if isinstance(enc, Encoder):
                        getattr(enc, name)(param)
                    else:
                        getattr(EncoderSlice(enc), name)(param)
            return multicall
        else:
            return object.__getattribute__(self, name)
