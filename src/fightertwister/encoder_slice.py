import numpy as np
import inspect
from collections.abc import Iterable
from .encoder import Encoder


def num_params(callable):
    return len(inspect.signature(callable).parameters)


class EncoderSlice(Encoder):
    def __init__(self, encoders: np.ndarray):
        self.encoders = encoders
        self.shape = self.encoders.shape
        indices = map(tuple, np.indices(self.encoders.shape).reshape(
            self.encoders.ndim, -1).T)
        self.idx_table = dict(zip(self, map(tuple, indices)))

    def __getitem__(self, indices):
        item = self.encoders[indices]
        if isinstance(item, Encoder):
            return item
        else:
            return EncoderSlice(item)

    def __iter__(self):
        return (i.item() for i in np.nditer(self.encoders, ["refs_ok"]))

    @ property
    def value(self):
        values = np.array([enc.value for enc in self])
        return values.reshape(self.shape)

    def get_idx(self, encoder):
        return self.idx_table[encoder]

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
