import numpy as np
import inspect
from collections.abc import Iterable
from .encoder import Encoder


def num_params(callable):
    return len(inspect.signature(callable).parameters)


class EncoderSlice:
    def __init__(self, encoders: np.ndarray):
        self.encoders = encoders
        self.encoders_raveled = encoders.ravel()
        self.shape = self.encoders.shape
        self.idx_table = dict(
            zip(self,
                map(tuple, np.indices(self.encoders.shape).reshape(2, -1))))

    def __getitem__(self, indices):
        item = self.encoders[indices]
        if isinstance(item, Encoder):
            return item
        else:
            return EncoderSlice(item)

    def __iter__(self):
        return iter(self.encoders_raveled)

    @ property
    def values(self):
        values = np.array([enc.value for enc in self])
        return values.reshape(self.shape)

    def get_idx(self, encoder):
        self.idx_table[encoder]

    def __getattribute__(self, name: str):
        if (hasattr(Encoder, name) and callable(getattr(Encoder, name))
                and num_params(getattr(Encoder, name)) in (1, 2)):

            def multicall(param):
                encoders, params = np.broadcast_arrays(self.encoders, param)
                for enc, param in zip(self, params.ravel()):
                    if isinstance(enc, Encoder):
                        getattr(enc, name)(param)
                    else:
                        getattr(EncoderSlice(enc), name)(param)
            return multicall
        else:
            return object.__getattribute__(self, name)
